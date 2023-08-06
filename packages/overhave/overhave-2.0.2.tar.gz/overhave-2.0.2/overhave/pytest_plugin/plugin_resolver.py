import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

from overhave.entities import OverhaveFileSettings

logger = logging.getLogger(__name__)


class PluginResolver:
    """ Class for custom pytest-bdd steps modules resolution. """

    def __init__(self, file_settings: OverhaveFileSettings):
        self._file_settings = file_settings
        self._plugins = self._resolve_plugins(directory=self._file_settings.steps_dir)
        logger.debug("Available Overhave pytest plugin modules: %s", self._plugins)

    @staticmethod
    def _check_dir_compliance(path: Path) -> bool:
        return all((path.is_dir(), not path.name.startswith("."), not path.name.startswith("_")))

    @staticmethod
    def _check_module_compliance(path: Path) -> bool:
        return all(
            (not path.is_dir(), path.name.endswith(".py"), not path.name.startswith("."), not path.name.startswith("_"))
        )

    @classmethod
    def _extract_recursively(cls, folder: Path) -> List[Path]:
        modules = []
        for path in folder.iterdir():
            if cls._check_dir_compliance(path):
                submodules = cls._extract_recursively(path)
                modules.extend(submodules)
                continue
            if not cls._check_module_compliance(path):
                continue
            modules.append(path)
        return modules

    @classmethod
    def _resolve_plugins(cls, directory: Path) -> Dict[str, List[Path]]:
        plugin_folders = [d for d in directory.iterdir() if cls._check_dir_compliance(d)]
        plugin_dict = {folder.name: cls._extract_recursively(folder) for folder in plugin_folders}

        plugin_modules = [m for m in directory.iterdir() if cls._check_module_compliance(m)]
        for folder in plugin_dict:
            plugin_dict[folder].extend(plugin_modules)
        return plugin_dict

    def _format_path(self, path: Path) -> str:
        relative_path = path.relative_to(self._file_settings.work_dir).as_posix()
        return relative_path.replace("/", ".").rstrip(".py")

    def get_plugins(self, plugin_type: Optional[str] = None) -> List[str]:
        if isinstance(plugin_type, str):
            if self._plugins.get(plugin_type) is None:
                raise KeyError(f"Specified plugin type '{plugin_type}' does not exist!")
            plugins = [self._format_path(x) for x in self._plugins[plugin_type]]
            logger.debug("Return plugins by plugin_type='%s': %s", plugin_type, plugins)
            return plugins

        joined_modules: Set[str] = set()
        for key in self._plugins:
            joined_modules.update(set(self.get_plugins(key)))
        modules_list = list(joined_modules)
        logger.debug("Return all existing plugins: %s", modules_list)
        return modules_list
