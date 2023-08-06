from pencil_pusher.configs.manager import ConfigManager
from typing import Any, final
from sd_utils.plugins.plugin_base import PluginBase


class ConfigParamBase(PluginBase):
    def __init__(self):
        self._is_defined = False

    @final
    def on_find(self, data: Any) -> Any:
        # return super().on_find(data=data)
        if not self._is_defined:
            return None
        return data["contents"][data["name"]]

    def on_iterate(self, data: Any):
        """
        This is the validate function
        """
        if data["type"] == ConfigManager.VALIDATE:
            self._validate(data["contents"])
            self.set_defined()

    def _validate(self, contents: dict) -> bool:
        """
        method for validating this specific config given
        the entire config file as a dict
        """
        raise NotImplementedError

    def set_defined(self):
        """
        Sets this config parameter to having
        been defined.

        It is assumed that a config errors and
        is marked not valid if it is required
        but not defined
        """
        self._is_defined = True
