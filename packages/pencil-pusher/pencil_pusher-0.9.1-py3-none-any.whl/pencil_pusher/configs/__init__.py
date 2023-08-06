from sd_utils.plugins.plugin_collector import collect_plugins
from pencil_pusher.configs.base import ConfigParamBase
from pencil_pusher.configs.manager import ConfigManager


config_manager = ConfigManager()

__all__ = collect_plugins(
    __file__, __name__, ConfigParamBase, ["base", "manager"]
)
