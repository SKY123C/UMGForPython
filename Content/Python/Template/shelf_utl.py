import logging
import pathlib
import importlib
import os
import unreal
import mimetypes
import requests
import sys
import traceback
from . import shelf_core

root_logger = logging.getLogger("ToolShelf")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry: unreal.AssetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()

if unreal.SystemLibrary.get_engine_version().startswith("4"):
    asset_system = unreal.EditorAssetLibrary
else:
    asset_system = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
    
def register_all_stack_handle(reload=False):
    def check_py(in_path: pathlib.Path):
        return in_path.is_file() and in_path.suffix.lower() == ".py" and not in_path.stem.startswith("__")
    root = "ToolShelf"
    shelf_name = "shelves"
    for x in pathlib.Path(__file__).parent.joinpath(shelf_name).iterdir():
        try:
            module_obj = None
            if check_py(x) and x.stem.startswith("shelf_"):
                module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
            elif x.is_dir() and not x.stem.startswith("__"):
                module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
        except Exception as e:
            unreal.log_error(traceback.format_exc())

        if reload and module_obj:
            importlib.reload(module_obj)

def get_is_debug():
    tw_debug = os.environ.get("tw_debug")
    result = False
    if tw_debug is not None:
        result = False if os.environ.get("tw_debug") == "False" else True
    return result

def useful_interchanged():
    result = False
    try:
        result = unreal.SystemLibrary.get_console_variable_bool_value('Interchange.FeatureFlags.Import.FBX')
    except Exception as e:
        ...
    return result


def send_log_to_confluence(token="", page_id="", file_name="", comment=""):
    ...

def extend_python_path():
    sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))



def find_handle(handle_name):
    for i in shelf_core.UMGWIDGET.iter_handle():
        if i.__class__.__name__ == handle_name:
            return i
    return