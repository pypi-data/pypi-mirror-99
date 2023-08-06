import os
from typing import List


class FileUtil:
    @staticmethod
    def query_directory(
        directory: str, include_extensions: List[str]
    ) -> List[str]:
        """
        Returns a list of file paths in the given directory and any
        of its containing sub directories
        """
        result: List[str] = []

        path = os.path.abspath(directory)

        for item in os.listdir(path):
            for ext in include_extensions:
                if item.endswith(ext):
                    result.append(path + "/" + item)
                    break
            if os.path.isdir(path + "/" + item):
                result.extend(
                    FileUtil.query_directory(
                        path + "/" + item + "/", include_extensions
                    )
                )

        return result
