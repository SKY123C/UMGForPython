import os
import sys
import unreal
import pathlib

# project_dir = unreal.SystemLibrary.get_project_directory()
# python_dir = os.path.join(project_dir, r"TA")
# lib_dir = os.path.join(project_dir, r"TA/TAPython/Lib/site-packages")
# sys.path.extend([python_dir, lib_dir])

def init():
    major_ver = sys.version_info.major
    minor_ver = sys.version_info.minor
    root_path = unreal.SystemLibrary.get_project_directory()
    current_file_path = os.path.dirname(__file__)
    if major_ver == 3 and minor_ver == 9:
        import pip._vendor.tomli as tomllib
    elif major_ver == 3 and minor_ver > 9:
        import tomllib
    else:
        return

    config = None
    tool_shelf_path = ""
    _config_path = os.path.join(current_file_path, "config.toml")
    if os.path.exists(_config_path):
        with open(os.path.join(current_file_path, "config.toml"), "rb") as f:
            config = tomllib.load(f)

    if not config:
        tool_shelf_path = os.path.join(root_path, "TA")
    else:
        # init root path
        root = config.get("path", {}).get("root", "")
        if root:
            root_path = root

        # append site-packages
        for i in config.get("site-packages", {}).items():
            key, value = i
            if key == "root":
                for j in value.items():
                    key1, value1 = j
                    t_path = os.path.join(root_path, value1)
                    if key1 == "start":
                        if not value1:
                            t_path = os.path.join(root_path, "TA")
                        tool_shelf_path = t_path
                    sys.path.append(t_path)
            else:
                sys.path.append(value)
    if not tool_shelf_path:
        tool_shelf_path = os.path.join(root_path, "TA")
    if not os.path.exists(tool_shelf_path):
        os.makedirs(tool_shelf_path, exist_ok=True)

    # copy template
    for i in pathlib.Path(tool_shelf_path).iterdir():
        if i.is_dir() and i.name == "ToolShelf":
            break
    else:
        import shutil
        shutil.copytree(os.path.join(current_file_path, "Template"), os.path.join(tool_shelf_path, "ToolShelf"))

def main():

    section_name = 'ToolShelf'
    se_command = 'from ToolShelf import shelf_start;shelf_start.start(True)'
    label = 'ToolShelf Gallery'
    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(label)
    entry.set_icon('UMGForPythonStyleSet', 'UMGForPython.Icon', 'UMGForPython.Icon')
    entry.set_tool_tip("ToolShelf")
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()

try:
    init()
    from ToolShelf import shelf_start
    shelf_start.start(False)
    main()
except Exception as e:
    unreal.log_error(e)