from typing import Dict, List
from . import mcpo_uobject
import subprocess

class MCPModel:

    def __init__(self):
        self._manager = mcpo_uobject.MCPManager()
        self._subprocess_container: Dict = {}
        self._config_path_container: List[str] = []
    
    @property
    def uobject(self) -> mcpo_uobject.MCPManager:
        return self._manager

    def init(self):
        for i in dir(mcpo_uobject.MCPManager):
            try:
                self._subprocess_container[i] = None
            except Exception as e:
                pass
    
    def update_container(self, name: str, in_subprecess: subprocess.Popen):
        self._subprocess_container[name] = in_subprecess
    
    def get_value(self, name: str) -> subprocess.Popen:
        return self._manager.get_editor_property(name)

    def get_subprocess(self, name: str) -> subprocess.Popen:
        return self._subprocess_container.get(name)
    
    def add_config_path(self, path: str):
        self._config_path_container.append(path)

