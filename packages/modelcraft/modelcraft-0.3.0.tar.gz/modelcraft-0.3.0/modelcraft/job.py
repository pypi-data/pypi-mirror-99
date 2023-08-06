import abc
import os
import distutils.spawn
import shutil
import subprocess
import time
import uuid
from .pipeline import Pipeline


class Job(abc.ABC):
    def __init__(self, executable: str):
        self._executable = executable
        self._args = []
        self._stdin = []
        self._environ = {}
        self._directory = None

    def run(self, pipeline: Pipeline = None):
        if distutils.spawn.find_executable(self._executable) is None:
            raise ValueError("Executable '%s' not found" % self._executable)
        if pipeline is None:
            self._directory = str(uuid.uuid4())
        else:
            self._directory = pipeline.next_job_directory(self._executable)
        os.mkdir(self._directory)
        self._setup()
        with open(self._path("script.sh"), "w") as stream:
            stream.write(self._script())
        os.chmod(self._path("script.sh"), 0o755)
        start_time = time.time()
        self._run_subprocess()
        seconds = time.time() - start_time
        result = self._result()
        if pipeline is None:
            self._remove_files()
        else:
            pipeline.seconds[self._executable] += seconds
            if not pipeline.keep_jobs:
                self._remove_files(keep_logs=pipeline.keep_logs)
        return result

    def _path(self, *paths: str) -> str:
        return os.path.join(self._directory, *paths)

    @abc.abstractmethod
    def _setup(self) -> None:
        pass

    @abc.abstractmethod
    def _result(self):
        pass

    def _run_subprocess(self):
        with open(self._path("stdout.txt"), "w") as out_stream:
            with open(self._path("stderr.txt"), "w") as err_stream:
                process = subprocess.Popen(
                    args=[self._executable] + self._args,
                    stdin=subprocess.PIPE if self._stdin else None,
                    stdout=out_stream,
                    stderr=err_stream,
                    encoding="utf8",
                    env={**os.environ, **self._environ},
                    cwd=self._directory,
                )
        if self._stdin:
            for line in self._stdin:
                process.stdin.write(line + "\n")
            process.stdin.close()
        process.wait()

    def _script(self) -> str:
        script = "#!/usr/bin/env bash\n\n"
        if self._environ:
            for variable, value in self._environ.items():
                script += f"export {variable}={value}\n"
            script += "\n"
        script += self._executable
        script += f" {' '.join(self._args)} \\\n> stdout.txt 2> stderr.txt"
        if self._stdin:
            script += " << EOF\n"
            for line in self._stdin:
                script += f"{line}\n"
            script += "EOF\n"
        else:
            script += "\n"
        return script

    def _remove_files(self, keep_logs: bool = False) -> None:
        if keep_logs:
            os.makedirs("modelcraft-logs", exist_ok=True)
            for filename in ("stdout.txt", "stderr.txt", "script.sh"):
                src = self._path(filename)
                dst = os.path.join("modelcraft-logs", f"{self._directory}_{filename}")
                os.rename(src, dst)
        shutil.rmtree(self._directory, ignore_errors=True)
