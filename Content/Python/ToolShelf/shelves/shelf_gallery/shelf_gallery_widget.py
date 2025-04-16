
from ... import shelf_core, shelf_utl
from . import gallery_class
import unreal
import importlib
import pathlib
import gc
gc.collect()

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
                    module = importlib.reload(module)
                
        for i in gallery_class.GallaryWidgetFactory.__subclasses__():
            c = i()
            widget = c.create()
            expand_area = unreal.PythonExpandableArea()
            expand_area.set_expandable_area_body(widget)
            text = unreal.TextBlock()
            text.font.size = 10
            text.set_text(c.with_content())
            expand_area.set_expandable_area_head(text)
            slot: unreal.VerticalBoxSlot = self._root_widget.add_child_to_vertical_box(expand_area)
            slot.set_padding(unreal.Margin(0, 0, 0, 5))
        else:
            slot.size.size_rule = unreal.SlateSizeRule.FILL

        