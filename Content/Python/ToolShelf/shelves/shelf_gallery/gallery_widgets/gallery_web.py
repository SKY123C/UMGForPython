import unreal
from ToolShelf import shelf_core
from .. import gallery_class
import os


class GalleryWeb(gallery_class.GallaryWidgetFactory):

    def create(self):   

        widget = unreal.WebBrowser()
        # load_url 未将url传递给initoal_url
        widget.set_editor_property("initial_url", "https://github.com/SKY123C/UMGForPython/tree/main")
        return widget
        
