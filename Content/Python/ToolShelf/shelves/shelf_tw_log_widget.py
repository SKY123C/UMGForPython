from .. import (shelf_core,
                )
import base_controll
import logging
import unreal



class LogToolHandle(shelf_core.StackWidgetHandle):
    
    instance = True
    order = 0.1
    support_tool = ["日志"]
    
    def __init__(self, entity):
        self.background_color = unreal.LinearColor()
        self.text_box_map = {
            logging.WARNING: unreal.EditorUtilityMultiLineEditableTextBox(),
            logging.ERROR: unreal.EditorUtilityMultiLineEditableTextBox()
        }
        self.text_color_map = {
            logging.WARNING: unreal.SlateColor(unreal.LinearColor(1,1,0,1)),
            logging.ERROR: unreal.SlateColor(unreal.LinearColor(1,0,0,1))
        }
        super().__init__(entity)
        self.__expand_area_map = {
            ""
        }
        base_controll.create_logger("ToolShelf", self)
    
    def setup(self):
        self._root_widget = unreal.VerticalBox()
        for log_type, text_box in self.text_box_map.items():
            expand_area = unreal.PythonExpandableArea()
            text = unreal.TextBlock()
            text.set_text(logging.getLevelName(log_type))
            text.font.size = 10
            expand_area.set_expandable_area_head(text)
            expand_area.set_expandable_area_body(text_box)
            text_box.widget_style.text_style.color_and_opacity = self.text_color_map.get(log_type)
            self._root_widget.add_child_to_vertical_box(expand_area)
    
    def write(self, log_type, text):
        text_box = self.text_box_map.get(log_type)
        if text_box:
            src_text = text_box.get_text()
            text_box.set_text(str(src_text) + "\n" + text)