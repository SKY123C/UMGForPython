import unreal
from .... import shelf_core
import pathlib
import random

def on_click(button: unreal.Button):
    
    def on_click1():
        color = [random.random(), random.random(), random.random(), 1]
        button.set_background_color(unreal.LinearColor(*color))
        print(color)
        #button.set_color_and_opacity(unreal.LinearColor(*color, 1))
    return on_click1

def create():
    icon_path = unreal.Paths.combine([unreal.Paths.project_plugins_dir(), "UMGForPython/Resources/toobar.png"])
    unreal.Paths.project_plugins_dir()
    button = shelf_core.create_button("Button", icon_path)
    
    button.on_clicked.add_callable(on_click(button))
    return button