import unreal
from ToolShelf import shelf_core
from .. import gallery_class


def on_click(button, context_menu: unreal.MenuAnchor):
    def on_click1():
        button
        context_menu.open(True)
    return on_click1

class GallaryContextMenu(gallery_class.GallaryWidgetFactory):


    def create_menu(self):
        layout = unreal.VerticalBox()
        for i in range(10):
            btn = unreal.EditorUtilityCheckBox()
            text = unreal.TextBlock()
            text.set_text(str(i))
            text.font.size = 10
            btn.add_child(text)
            layout.add_child_to_vertical_box(btn)
        return layout

    def create(self):
        layout1 = unreal.VerticalBox()
        context_menu = unreal.MenuAnchor()
        layout = unreal.VerticalBox()
        icon_path = unreal.Paths.combine([unreal.Paths.project_plugins_dir(), "UMGForPython/Resources/Icon128.png"])
        button = shelf_core.create_button("Context Menu", icon_path)
        button.on_clicked.add_callable(on_click(button, context_menu))
        context_menu.get_editor_property("on_get_menu_content_event").bind_callable(self.create_menu)
        layout.add_child_to_vertical_box(button)
        context_menu.set_content(layout)
        layout1.add_child_to_vertical_box(context_menu)
        return layout1
