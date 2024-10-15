import unreal
from ToolShelf import shelf_core

EXPORTABLE = True

def on_click(button, context_menu: unreal.MenuAnchor):
    def on_click1():
        button
        context_menu.open(True)
    return on_click1

def create_menu():
    layout = unreal.VerticalBox()
    for i in range(10):
        btn = unreal.EditorUtilityCheckBox()
        text = unreal.TextBlock()
        text.set_text(str(i))
        text.font.size = 10
        btn.add_child(text)
        layout.add_child_to_vertical_box(btn)
    return layout

def create():
    layout1 = unreal.VerticalBox()
    context_menu = unreal.MenuAnchor()
    layout = unreal.VerticalBox()
    icon_path = unreal.Paths.combine([unreal.Paths.project_plugins_dir(), "UMGForPython/Resources/toolbar.png"])
    button = shelf_core.create_button("Context Menu", icon_path)
    button.on_clicked.add_callable(on_click(button, context_menu))
    context_menu.get_editor_property("on_get_menu_content_event").bind_callable(create_menu)
    layout.add_child_to_vertical_box(button)
    context_menu.set_content(layout)
    layout1.add_child_to_vertical_box(context_menu)
    return layout1
