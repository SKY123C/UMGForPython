from . import gallery_class
from . import shelf_gallery_widget
import importlib
from ... import shelf_utl
if shelf_utl.get_is_debug():
    importlib.reload(gallery_class)
    importlib.reload(shelf_gallery_widget)