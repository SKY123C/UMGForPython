
from ... import shelf_core, shelf_utl
#from .gallery_widgets import gallery_button
import unreal
import os
import threading
import time
import importlib
import pathlib


import sys
sys.modules
class GalleryHandle(shelf_core.StackWidgetHandle):
    
    instance = True
    order = 0.1
    support_tool = ["Gallery"]
    fill = True
    
    
    def __init__(self, entity):
        super().__init__(entity)
    
    def setup(self):
        self._root_widget = unreal.VerticalBox()
        for widget_file in pathlib.Path(__file__).parent.joinpath("gallery_widgets").iterdir():
            if widget_file.is_file():
                module = importlib.import_module(f".gallery_widgets.{widget_file.stem}", __package__)
                if shelf_utl.get_is_debug():
                    importlib.reload(module)
                if hasattr(module, "create"):
                    widget = module.create()
                    self._root_widget.add_child_to_vertical_box(widget)
            #__import__(f"gallery_widgets.{widget_file.stem}", level=2)
            
            #importlib.import_module(f".gallery_widgets.gallery_button", "ToolShelf")
        