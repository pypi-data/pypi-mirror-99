import argparse
import functools
import math
import os
import re
import sys
import time
import requests
from ..contents import AsuContents, Carb, Ligand, Polymer, PolymerType
from ..environ import setup_environ


def _add_smiles(contents: AsuContents) -> None:
    codes = contents.monomer_codes()
    codes = {code for code in codes if not _in_library(code)}
    for code in sorted(codes):
        path = os.path.join(os.environ["CLIBD_MON"], code[0].lower(), code + ".cif")
        if not os.path.exists(path):
            contents.smiles[code] = _smiles(code)


@functools.lru_cache(maxsize=None)
def _buffers() -> set:
    path = os.path.join(os.environ["CCP4"], "share", "pisa", "agents.dat")
    agents = set()
    with open(path) as stream:
        for line in stream:
            if line[0] != "#" and "," in line:
                code = line.split(",")[0]
                agents.add(code)
    return agents


def _carb_codes(entry: str) -> dict:
    url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"
    query = "pdb_id:" + entry
    filter_list = "carb_compound_id_entity"
    request_data = {"q": query, "fl": filter_list, "wt": "json"}
    print("Requesting carbohydrate details for", entry)
    time.sleep(2)
    response = requests.post(url, data=request_data)
    if response.status_code != 200:
        raise ConnectionError(response.text)
    docs = response.json()["response"]["docs"]
    codes = {}
    for doc in docs:
        for line in doc["carb_compound_id_entity"]:
            match = re.match(r"(.+)\((\d+)\)_(\d+)", line)
            code, copies, entity = match.groups()
            codes.setdefault(int(entity), {})[code] = int(copies)
    return codes


def _carb_from_pdbe_molecule_dict(mol: dict) -> Carb:
    codes = mol["carb_codes"]
    length = sum(codes.values())
    copies = mol["number_of_copies"] // length
    return Carb(codes=codes, copies=copies)


def _divide_copies(contents: AsuContents):
    copies = []
    for item in (
        contents.proteins
        + contents.rnas
        + contents.dnas
        + contents.carbs
        + contents.ligands
    ):
        if item.copies is not None:
            copies.append(item.copies)
    divisor = copies[0] if len(copies) == 1 else functools.reduce(math.gcd, copies)
    contents.copies *= divisor
    for item in (
        contents.proteins
        + contents.rnas
        + contents.dnas
        + contents.carbs
        + contents.ligands
    ):
        item.copies //= divisor


def _entry_contents(entry: str) -> AsuContents:
    contents = AsuContents()
    contents.copies = 1
    for mol in _pdbe_molecules(entry):
        if "sequence" in mol:
            polymer = _polymer_from_pdbe_molecule_dict(mol)
            contents.add_polymer(polymer)
        if mol["molecule_type"] == "carbohydrate polymer":
            carb = _carb_from_pdbe_molecule_dict(mol)
            contents.carbs.append(carb)
        if mol["molecule_type"] == "bound":
            ligand = _ligand_from_pdbe_molecule_dict(mol)
            if _is_buffer(ligand.code):
                contents.buffers.append(ligand.code)
            elif ligand.code not in ("UNL", "UNX"):
                contents.ligands.append(ligand)
    _divide_copies(contents)
    _add_smiles(contents)
    return contents


@functools.lru_cache(maxsize=None)
def _in_library(code: str) -> bool:
    path = os.path.join(os.environ["CLIBD_MON"], code[0].lower(), code + ".cif")
    return os.path.exists(path)


@functools.lru_cache(maxsize=None)
def _is_buffer(code: str) -> float:
    return code.upper() in _buffers()


def _ligand_from_pdbe_molecule_dict(mol: dict) -> Ligand:
    return Ligand(code=mol["chem_comp_ids"][0], copies=mol["number_of_copies"])


def _modifications_in_pdbe_molecule_dict(mol: dict) -> list:
    indices = {}
    for index, mod in mol["pdb_sequence_indices_with_multiple_residues"].items():
        code1 = mod["one_letter_code"]
        code3 = mod["three_letter_code"]
        if code3 not in ("DA", "DC", "DG", "DT"):
            key = code1, code3
            indices.setdefault(key, []).append(index)
    modifications = []
    for key in indices:
        code1, code3 = key
        total = mol["sequence"].count(code1)
        if code1 == "M" and mol["sequence"][0] == "M":
            total -= 1
        if len(indices[key]) >= total:
            modifications.append(f"{code1}->{code3}")
        else:
            modifications.extend(f"{index}->{code3}" for index in indices[key])
    return modifications


def _pdbe_molecules(entry: str) -> list:
    entry = entry.lower()
    url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/" + entry
    print("Requesting PDBe molecule data for", entry)
    time.sleep(2)
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(response.text)
    mols = response.json()[entry]
    if any(mol["molecule_type"] == "carbohydrate polymer" for mol in mols):
        codes = _carb_codes(entry)
        for mol in mols:
            mol["carb_codes"] = codes.get(mol["entity_id"])
    return mols


def _polymer_from_pdbe_molecule_dict(mol: dict) -> Polymer:
    polymer_type = {
        "polypeptide(l)": PolymerType.PROTEIN,
        "polyribonucleotide": PolymerType.RNA,
        "polydeoxyribonucleotide": PolymerType.DNA,
    }[mol["molecule_type"].lower()]
    return Polymer(
        sequence=mol["sequence"],
        copies=mol["number_of_copies"],
        polymer_type=polymer_type,
        modifications=_modifications_in_pdbe_molecule_dict(mol),
    )


@functools.lru_cache(maxsize=None)
def _smiles(code: str) -> str:
    query = (
        "{\n"
        '  chem_comp(comp_id: "%s") {\n'
        "    pdbx_chem_comp_descriptor {\n"
        "      comp_id\n"
        "      descriptor\n"
        "      program\n"
        "      program_version\n"
        "      type\n"
        "    }\n"
        "  }\n"
        "}" % code
    )
    url = "https://data.rcsb.org/graphql?query=" + requests.utils.quote(query)
    print("Requesting SMILES for", code)
    time.sleep(2)
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Could not get SMILES from RCSB for " + code)
    descriptors = response.json()["data"]["chem_comp"]["pdbx_chem_comp_descriptor"]
    canonical = None
    smiles = None
    for descriptor in descriptors:
        if descriptor["type"] == "SMILES_CANONICAL":
            if descriptor["program"] == "OpenEye OEToolkits":
                return descriptor["descriptor"]
            else:
                canonical = descriptor["descriptor"]
        elif descriptor["type"] == "SMILES":
            smiles = descriptor["descriptor"]
    if canonical is not None:
        return canonical
    if smiles is None:
        raise RuntimeError("Could not get SMILES from RCSB for " + code)
    return smiles


def main(argument_list=None):
    setup_environ()
    if argument_list is None:
        argument_list = sys.argv[1:]
    description = "Create a contents JSON file for a PDB entry"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("entry", help="PDB entry ID")
    parser.add_argument("contents", help="Path for the contents JSON")
    args = parser.parse_args(argument_list)
    contents = _entry_contents(entry=args.entry)
    contents.write_json_file(args.contents)


if __name__ == "__main__":
    main()
