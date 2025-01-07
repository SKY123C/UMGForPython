import unreal

def main():
    from ToolShelf import shelf_start;
    shelf_start.start(False)
    section_name = 'ToolShelf'
    se_command = 'from ToolShelf import shelf_start;shelf_start.start()'
    label = 'ToolShelf Gallery'
    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu('LevelEditor.LevelEditorToolBar.PlayToolBar')
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(label)
    entry.set_icon('UMGForPythonStyleSet', 'UMGForPython.Icon', 'UMGForPython.Icon')
    entry.set_tool_tip("UMGForPython Gallery")
    entry.set_string_command(
        type=unreal.ToolMenuStringCommandType.PYTHON,
        custom_type=unreal.Name(''),
        string=se_command
    )
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()
main()