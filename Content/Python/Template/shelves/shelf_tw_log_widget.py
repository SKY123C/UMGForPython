from .. import (shelf_core
                )
import logging
import unreal

@unreal.uclass()
class LogWidget(unreal.VerticalBox):

    edit_box = unreal.uproperty(unreal.PythonMultiLineEditableTextBox)

    def _post_init(self):
        filter_layout = unreal.HorizontalBox()
        filter_menu = unreal.MenuAnchor()
        #self.filter_menu.get_editor_property("on_get_menu_content_event").bind_callable(self.init_filter_menu)
        filter_btn = shelf_core.create_button("Filter", icon_path=shelf_core.Utl.get_full_icon_path("filter.png"))
        filter_btn.set_background_color(unreal.LinearColor())
        #self.filter_btn.widget_style.normal.outline_settings.width = 0
        filter_menu.set_content(filter_btn)
        filter_layout.add_child_to_horizontal_box(filter_menu)
        self.edit_box = unreal.PythonMultiLineEditableTextBox()
        self.edit_box.read_only = True
        self.add_child_to_vertical_box(filter_layout)
        slot = self.add_child_to_vertical_box(self.edit_box)
        slot.size.size_rule = unreal.SlateSizeRule.FILL

    def write(self, log_type, text):
        if log_type == logging.WARNING:
            R = G = 1
            B = 0
        elif log_type == logging.ERROR:
            R = 1
            B = G = 0
        else:
            R = G = B = 1
        if text and text[-1] == "\n":
            text = text[0:-1]
        text = f"<PythonRichText FontColor=\"R={R} G={G} B={B}\">{text}</>"
        self.edit_box.set_text(str(self.edit_box.get_text()) + "\n" + text)

class LogToolHandle(shelf_core.StackWidgetHandle):
    
    instance = True
    order = 0
    support_tool = ["日志"]
    fill = True
    
    def __init__(self, entity):
        self.background_color = unreal.LinearColor()
        super().__init__(entity)
        self.__expand_area_map = {
            ""
        }
        #base_controll.create_logger("ToolShelf", self)
    
    def setup(self):
        self._root_widget = LogWidget()
        shelf_core.ToolShelfLogger.set_default_output(self._root_widget)
        shelf_core.ToolShelfLogger.create_logger("ToolShelf")
    