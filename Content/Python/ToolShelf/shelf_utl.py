import logging
from . import shelf_core
import pathlib
import importlib
import os
import unreal

logger = logging.getLogger("ToolShelf")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

logger_list = [
    
]

def register_all_stack_handle(reload=False):
    '''
    dadsada
    '''
    def check_py(in_path: pathlib.Path):
        return in_path.is_file() and in_path.suffix.lower() == ".py" and not in_path.stem.startswith("__")
    root = "ToolShelf"
    shelf_name = "shelves"
    for x in pathlib.Path(__file__).parent.joinpath(shelf_name).iterdir():
        if check_py(x) and x.stem.startswith("shelf_"):
            module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
            if reload:
                importlib.reload(module_obj)
        elif x.is_dir():
            for x1 in x.iterdir():
                if check_py(x1) and x1.stem.startswith("shelf_"):
                    module_obj = importlib.import_module(f".{shelf_name}.{x.stem}.{x1.stem}", root)
                    if reload:
                        importlib.reload(module_obj)

def get_is_debug():
    tw_debug = os.environ.get("tw_debug")
    result = False
    if tw_debug is not None:
        result = False if os.environ.get("tw_debug") == "False" else True
    return result

class CustomLogger:
    def __init__(self, name, out_object=None) -> None:
        self._logger = logging.getLogger(name)
        if self._logger.hasHandlers():
            for i in self._logger.handlers:
                self._logger.removeHandler(i)
        logger_handle = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                        '-%(levelname)s-[日志信息]: %(message)s',
                                        datefmt='%d-%m-%Y')
        self.log_str = ""
        self.warning_str= ""
        logger_handle.setFormatter(formatter)
        logger_handle.setStream(self)
        self._logger.addHandler(logger_handle)
        self.out_object = out_object
    
    @property
    def logger(self):
        return self._logger
    
    def write(self, text, *args, **kwargs):
        log_type = None
        if "-WARNING-" in text:
            ...
            self.warning_str += text + "\n"
            log_type = logging.WARNING
        elif "-ERROR-" in text:
            self.log_str += text + "\n"
            log_type = logging.ERROR
        
        if self.out_object:
            self.out_object.write(log_type, text)
    
def create_logger(name, out_object=None):
    logger = CustomLogger(name, out_object)
    return logger.logger