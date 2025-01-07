import logging
import pathlib
import importlib
import os
import unreal

logger_output = None
root_logger = logging.getLogger("ToolShelf")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
log_id_map = {}

logger_list = [
    
]


def set_logger_output(i):
    global logger_output
    logger_output = i
    
    
def register_all_stack_handle(reload=False):
    def check_py(in_path: pathlib.Path):
        return in_path.is_file() and in_path.suffix.lower() == ".py" and not in_path.stem.startswith("__")
    root = "ToolShelf"
    shelf_name = "shelves"
    for x in pathlib.Path(__file__).parent.joinpath(shelf_name).iterdir():
        module_obj = None
        if check_py(x) and x.stem.startswith("shelf_"):
            module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
        elif x.is_dir() and not x.stem.startswith("__"):
            module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
        if reload and module_obj:
            importlib.reload(module_obj)

def get_is_debug():
    tw_debug = os.environ.get("tw_debug")
    result = False
    if tw_debug is not None:
        result = False if os.environ.get("tw_debug") == "False" else True
    return result


def create_logger(logger_name):
    custom_logger = logging.getLogger(logger_name)
    logger_list.append(custom_logger)

def write(log_id, log_type, text):
    ...
'''
    being

    end

'''