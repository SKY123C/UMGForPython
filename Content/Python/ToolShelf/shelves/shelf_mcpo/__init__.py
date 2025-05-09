from . import (shelf_mcpo_widget, shelf_mcpo_interface, mcpo_uobject, shelf_mcpo_model)
import importlib

from ... import shelf_utl
if shelf_utl.get_is_debug():
    importlib.reload(mcpo_uobject)
    importlib.reload(shelf_mcpo_model)
    importlib.reload(shelf_mcpo_interface)
    importlib.reload(shelf_mcpo_widget)
    
