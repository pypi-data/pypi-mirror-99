import json
from typing import Any, List, Tuple
from sd_utils.plugins.plugin_manager import PluginManager


class ConfigManager(PluginManager):

    VALIDATE = "validate"
    GET = "get"
    PROCESS_LANG_FILE = "process_lang_file"

    def __init__(self):
        self._config_file_contents = None
        self._languages = {}
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

    def process_lang_file(self, file_path: str) -> Tuple[bool, str]:
        """
        processes a language file based on defined configurations

        Returns:
            Tuple[bool, str]: the first value is if the file should be included,
                the second value is the new name of the file if it should be
                included.
        """
        ext = file_path[file_path.index(".") + 1 :]
        lang_name = ""
        for lang, exts in self._languages.items():
            for dext in exts:
                if ext == dext:
                    lang_name = lang
                    break
        return self.run(
            lang_name,
            on_find_params={
                "type": ConfigManager.PROCESS_LANG_FILE,
                "contents": self._config_file_contents,
                "file_path": file_path,
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

    def get_on_register_params(self, name: str, **kwargs) -> Any:
        return {"manager": self}

    def add_lang(self, lang_name: str, extensions: List[str]):
        """
        """
        self._languages[lang_name] = extensions

    def get_langs(self):
        return self._languages
