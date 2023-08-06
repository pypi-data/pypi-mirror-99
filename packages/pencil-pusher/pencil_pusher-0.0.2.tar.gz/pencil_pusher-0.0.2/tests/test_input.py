from unittest import mock
from pencil_pusher.input import InputManager
import os


@mock.patch(
    "pencil_pusher.input.environ",
    {
        "INPUT_OWNER_NAME": "o_n",
        "INPUT_REPOSITORY_NAME": "r_n",
        "INPUT_PERSONAL_ACCESS_TOKEN": "p_a_t",
        "INPUT_CONFIG_FILE": "c_f",
    },
)
def test_input_manager():
    """
    Validates that this method is working correctly
    """
    im = InputManager()
    im.define(os.environ["GH_PAT"])

    assert im.validate()

    assert im.get("owner_name") == "o_n"
    assert im.get("repository_name") == "r_n"
    assert im.get("personal_access_token") == "p_a_t"
    assert im.get("config_file") == "c_f"
