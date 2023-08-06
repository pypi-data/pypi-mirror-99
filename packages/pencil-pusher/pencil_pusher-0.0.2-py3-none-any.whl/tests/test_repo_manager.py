import os
import logging
from pencil_pusher.file_util import FileUtil
from pencil_pusher.documenter import Documenter
from pencil_pusher.github_api import GithubAPI
from pencil_pusher.repo_manager import RepoManager

logger = logging.getLogger("ghapi")
logger.addHandler(logging.FileHandler("ghapi.log"))
logger.setLevel(logging.INFO)


def test_repo_manager_simple_config():
    """
    Tests running the repo manager with the
    most basic config that can be provided
    """
    Documenter.install()

    owner = "biit-407"
    repo = "biit-server"
    ghapi = GithubAPI(os.environ["GH_PAT"])
    rm = RepoManager(owner, repo, ghapi)

    rm.setup()

    rm.install()

    rm.document(sources=["biit_server/"])
    # no publish, just testing

    files_to_check = FileUtil.query_directory(
        "../biit-server/biit_server/", [".py"]
    )
    files_found = FileUtil.query_directory("../biit-server-wiki/", [".md"])

    for fc in files_to_check:
        fc_name = fc[fc.index("biit_server") : -3]
        fc_name = fc_name.replace("/", ".")
        found = False
        for ff in files_found:
            if fc_name in ff:
                found = True
                break
        assert found, f"could not find [{fc_name}]"

    rm.cleanup()
