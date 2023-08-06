import subprocess
from typing import List


class ProcessUtil:
    """
    """

    @staticmethod
    def execute(
        command: List[str], cwd: str = "./", stdout: int = subprocess.PIPE
    ) -> int:
        """
        runs a given command to completion using subprocess then
        returns the return code
        """
        process = subprocess.Popen(
            command, cwd=cwd, stdout=stdout, stderr=subprocess.PIPE
        )
        process.communicate()
        return process.returncode
