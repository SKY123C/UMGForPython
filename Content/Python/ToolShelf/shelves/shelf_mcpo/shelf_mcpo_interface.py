import pathlib
import json
from typing import Dict, List, Union, Tuple
from . import shelf_mcpo_model, shelf_mcpo_utl
import subprocess
import os


mcpo_model = shelf_mcpo_model.MCPModel()

def get_mcp_config() -> Dict:
    """Get the mcpo config path."""
    with open(pathlib.Path(__file__).parent.joinpath("mcp_servers", "mcp_info.json"), "r") as f:
        config = json.load(f)
    return config

def get_mcpo_config_path() -> str:
    """Get the mcpo config path."""
    return pathlib.Path(__file__).parent.joinpath("mcp_config").as_posix()

def get_server_path() -> List[str]:
    result = []
    for i in pathlib.Path(__file__).parent.joinpath("mcp_servers").iterdir():
        print(i)
        if not i.is_dir():
            continue
        

def get_all_mcp_files() -> List[pathlib.Path]:
    """Get all mcp files."""
    mcp_files = []

    root_dir = pathlib.Path(__file__).parent.joinpath("mcp_servers")
    for i,j in get_mcp_config().items():
        if not j.get("enable"):
            continue
        mcp_files.append(root_dir.joinpath(i, j.get("file")))
    return mcp_files

def get_unreal_config_path() -> str:
    """Get the unreal config path."""
    return pathlib.Path(__file__).parent.joinpath("mcp_config", "unreal_mcp.json").as_posix()

def refresh_enable_state(name):
    mcpo_path = pathlib.Path(shelf_mcpo_utl.get_interpreter_executable_path()).parent.joinpath("Scripts", "mcpo.exe")
    if not mcpo_path.exists():

        ...
    
    if mcpo_model.get_value(name):
        popen = subprocess.Popen([mcpo_path.as_posix(), "--config", get_unreal_config_path()])
        print([mcpo_path, "--config", get_unreal_config_path()])
    else:
        mcpo_model.get_subprocess(name).terminate()
        popen = None

    mcpo_model.update_container(name, popen)

def create_config():
    mcp_server_files = get_all_mcp_files()
    #for i in mcp_server_files:
    dir_path = get_mcpo_config_path()
    if not os.path.exists(dir_path):
        #os.makedirs(dir_path)
        ...
    for i in mcp_server_files:

        config_path = os.path.join(dir_path, i.stem + ".json")
        with open(config_path, "w") as f:
            result = \
            {
                "mcpServers": 
                {   
                    i.stem: {
                    "command": shelf_mcpo_utl.get_interpreter_executable_path(),
                    "args": [
                    i.as_posix()
                    ]
                }
                }
            }
            json.dump(result, f, indent=5)
        mcpo_model.add_config_path(config_path)
