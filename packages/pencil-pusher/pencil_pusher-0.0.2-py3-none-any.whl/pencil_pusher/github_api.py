"""
Wrapper class for managing complex github commands needed to be
executed for this action
"""
from pencil_pusher.process_util import ProcessUtil
from github import Github
from github.ContentFile import ContentFile
from github.Repository import Repository
import logging


logger = logging.getLogger("ghapi")
logger.addHandler(logging.FileHandler("ghapi.log"))
logger.setLevel(logging.INFO)


class GithubAPI:
    def __init__(self, personal_access_token: str = ""):
        """
        """
        self._has_token = personal_access_token != ""
        self._pat = personal_access_token
        if self._has_token:
            self._Github = Github(personal_access_token)
        else:
            self._Github = Github()

    def clone_repo(self, owner: str, repo: str, local_path: str = ""):
        """
        """
        url = f"https://github.com/{owner}/{repo}.git"
        if self._has_token:
            url = f"https://{owner}:{self._pat}@github.com/{owner}/{repo}.git"

        ProcessUtil.execute(["git", "clone", f"{url}", f"{local_path}"])

    def full_update(self, owner: str, repo: str, path: str):
        """
        stages, commits and pushes all changes to a git repo
        in the given directory
        """
        ProcessUtil.execute(
            [
                "git",
                "remote",
                "set-url",
                "origin",
                f"https://{owner}:{self._pat}@github.com/{owner}/{repo}.git",
            ],
            cwd=path,
        )

        ProcessUtil.execute(["git", "config", "user.name", "ghapd"], cwd=path)

        ProcessUtil.execute(["git", "config", "user.email", "<>"], cwd=path)

        ProcessUtil.execute(["git", "add", "."], cwd=path)

        returncode: int = ProcessUtil.execute(
            ["git", "commit", "-m", '"Auto commit by ghapd"'], cwd=path
        )
        if returncode == 1:
            print("all docs are up to date")
            return

        ProcessUtil.execute(["git", "push"], cwd=path)

    @staticmethod
    def get_public_file(
        owner: str, repo: str, file_path: str, personal_access_token: str = ""
    ) -> str:
        """
        Gets a file from a public repo
        """
        g = (
            Github()
            if personal_access_token == ""
            else Github(personal_access_token)
        )
        repo: Repository = g.get_repo(f"{owner}/{repo}")
        response: ContentFile = repo.get_contents(file_path)
        return str(response.decoded_content, "utf-8")

    def _require_token(self):
        """
        """
        if not self._has_token:
            raise ValueError(
                "The selected operation requires that a token be provided"
            )
