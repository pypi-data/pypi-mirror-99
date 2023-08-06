import json
from typing import Any
from sd_utils.plugins.plugin_manager import PluginManager


class ConfigManager(PluginManager):

    VALIDATE = "validate"
    GET = "get"

    def __init__(self):
        self._config_file_contents = None
        super().__init__()

    def validate(self):
        """
        """
        if self._config_file_contents is None:
            raise ValueError("Config file was not loaded")

        self.iterate_all(
            {
                "type": ConfigManager.VALIDATE,
                "contents": self._config_file_contents,
            },
        )

    def get(self, name: str):
        """
        """
        if self._config_file_contents is None:
            raise ValueError("Config file was not loaded")

        return self.run(
            name,
            on_find_params={
                "type": ConfigManager.GET,
                "contents": self._config_file_contents,
            },
        )

    def load_config_file(self, file_path: str):
        """
        """
        with open(file_path, "r") as fp:
            self._config_file_contents = json.load(fp)

    def get_on_search_params(self, name: str, **kwargs) -> Any:
        # return super().get_on_search_params(name, **kwargs)
        return {"name": name, **kwargs}

    def get_on_find_params(self, name: str, **kwargs) -> Any:
        # return super().get_on_find_params(name, **kwargs)
        return {"name": name, **kwargs}
