import unreal
from .... import shelf_core
import random
from .. import gallery_class


class GallaryButton(gallery_class.GallaryWidgetFactory):

    def with_content(self):
        return "Button"
    
    def on_click(self, button: unreal.Button):
        
        def on_click1():
            color = [random.random(), random.random(), random.random(), 1]
            button.set_background_color(unreal.LinearColor(*color))
            print(color)
            #button.set_color_and_opacity(unreal.LinearColor(*color, 1))
        return on_click1

    def create(self):
        icon_path = unreal.Paths.combine([unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_plugins_dir()), "UMGForPython/Resources/Icon128.png"])
        button = shelf_core.create_button("Button", icon_path)
        button.on_clicked.add_callable(self.on_click(button))
        return button


