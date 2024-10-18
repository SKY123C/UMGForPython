from .. import (shelf_core, shelf_utl
                )
import logging
import unreal



class LogToolHandle(shelf_core.StackWidgetHandle):
    
    instance = True
    order = 0.1
    support_tool = ["日志"]
    fill = True
    
    def __init__(self, entity):
        self.background_color = unreal.LinearColor()
        super().__init__(entity)
        self.__expand_area_map = {
            ""
        }
        shelf_core.ToolShelfLogger.set_default_output(self)
        shelf_core.ToolShelfLogger.create_logger("ToolShelf")
        #base_controll.create_logger("ToolShelf", self)
    
    def setup(self):
        self._root_widget = unreal.VerticalBox()
        filter_layout = unreal.HorizontalBox()
        self.filter_menu = unreal.MenuAnchor()
        self.filter_menu.get_editor_property("on_get_menu_content_event").bind_callable(self.init_filter_menu)
        self.filter_btn = shelf_core.create_button("Filter", icon_path=shelf_core.Utl.get_full_icon_path("filter.png"))
        self.filter_btn.set_background_color(unreal.LinearColor())
        #self.filter_btn.widget_style.normal.outline_settings.width = 0
        self.filter_menu.set_content(self.filter_btn)
        filter_layout.add_child_to_horizontal_box(self.filter_menu)
        self.edit_box = unreal.PythonMultiLineEditableTextBox()
        self.edit_box.read_only = True
        self._root_widget.add_child_to_vertical_box(filter_layout)
        slot = self._root_widget.add_child_to_vertical_box(self.edit_box)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
    
    def __create_root_logger(self):
        
        
        ...
    def init_filter_menu(self):
        layout = unreal.VerticalBox()

    def write(self, log_type, text):
        if log_type == logging.WARNING:
            R = G = 1
            B = 0
        elif log_type == logging.ERROR:
            R = 1
            B = G = 0
        else:
            R = G = B = 1
        text = f"<PythonRichText FontColor=\"R={R} G={G} B={B}\">{text[0:-1]}</>"
        self.edit_box.set_text(str(self.edit_box.get_text()) + "\n" + text)