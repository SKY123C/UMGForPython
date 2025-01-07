import unreal
import pathlib
import os
import logging
from enum import Enum

@unreal.uclass()
class CGTeamWorkImportOptions(unreal.Object):
    
    task = unreal.uproperty(str, meta={"DisplayName": "任务名称", "GetOptions": "get_all_task", "Category": "参 数"})
    stage = unreal.uproperty(str, meta={"DisplayName": "环 节", "GetOptions": "get_all_stage", "Category": "参 数"})
    shot = unreal.uproperty(str, meta={"DisplayName": "镜 头", "GetOptions": "get_all_shots", "Category": "参 数"})
    ani = unreal.uproperty(str, meta={"DisplayName": "场 次", "GetOptions": "get_all_ani", "Category": "参 数"})
    project = unreal.uproperty(str, meta={"DisplayName": "项 目", "GetOptions": "get_all_projects", "Category": "参 数"})
    
    @unreal.ufunction(ret=unreal.Array(str))
    def get_all_projects(self):
        result = unreal.Array(str)
        
        return result
    
    @unreal.ufunction(ret=unreal.Array(str))
    def get_all_ani(self):
        result = unreal.Array(str)
        return result
    
    @unreal.ufunction(ret=unreal.Array(str))
    def get_all_shots(self):
        result = unreal.Array(str)
        return result
    
    @unreal.ufunction(ret=unreal.Array(str))
    def get_all_stage(self):
        result = unreal.Array(str)
        return result
    
    @unreal.ufunction(ret=unreal.Array(str))
    def get_all_task(self):
        result = unreal.Array(str)
        return result


@unreal.uclass()
class CGTeamWorkFbxImportOptions(unreal.Object):
    
    skeleton = unreal.uproperty(unreal.Skeleton, meta={"DisplayName": "骨 骼", "Category": "参 数"})
    out_directory = unreal.uproperty(unreal.DirectoryPath, meta={"DisplayName": "目标路径", "ContentDir": "", "Category": "参 数"})
    in_directory = unreal.uproperty(unreal.DirectoryPath, meta={"DisplayName": "Fbx文件夹路径", "RelativePath": "", "BlueprintReadOnly": "", "Category": "参 数"})


class ToolShelfLogger:
    
    logger_list = []
    default_output = None
    
    class LoggerState(Enum):
        
        START = 0
        END = 1
    
    @staticmethod
    def create_logger(logger_name, logger_output=None):
        print(ToolShelfLogger.default_output)
        if not logger_output and ToolShelfLogger.default_output:
            logger_output = ToolShelfLogger.default_output
        result = ToolShelfLogger(logger_name, logger_output)
        ToolShelfLogger.logger_list.append(result)
        return result

    @staticmethod
    def set_default_output(logger_output):
        ToolShelfLogger.default_output = logger_output
    def __init__(self, name, out_object):
        self._logger = logging.getLogger(name)
        if self._logger.hasHandlers():
            for i in self._logger.handlers:
                self._logger.removeHandler(i)
        logger_handle = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                        '-%(levelname)s-[日志信息]: %(message)s',
                                        datefmt='%d-%m-%Y')
        self.log_str = ""
        self.warning_str= ""
        logger_handle.setFormatter(formatter)
        logger_handle.setStream(self)
        self._logger.addHandler(logger_handle)
        self.out_object = out_object
        self.__tmp_error_str = ""
        self.__tmp_warning_str = ""
        self.__logger_state = ToolShelfLogger.LoggerState.END
    
    def begin(self):
        self.__tmp_error_str = ""
        self.__tmp_warning_str = ""
        if self.__logger_state == ToolShelfLogger.LoggerState.START:
            raise
        self.__logger_state = ToolShelfLogger.LoggerState.START
    
    def end(self):
        self.__logger_state = ToolShelfLogger.LoggerState.END

    @property
    def logger(self):
        return self._logger
    
    def write(self, text, *args, **kwargs):
        log_type = None
        if "-WARNING-" in text:
            self.warning_str += text + "\n"
            log_type = logging.WARNING
            if self.__logger_state == ToolShelfLogger.LoggerState.START:
                self.__tmp_warning_str += text + "\n"
                
        elif "-ERROR-" in text:
            self.log_str += text + "\n"
            log_type = logging.ERROR
            if self.__logger_state == ToolShelfLogger.LoggerState.START:
                self.__tmp_error_str += text + "\n"
        
        if self.out_object:
            self.out_object.write(log_type, text)
        
    def get_section_log(self, log_type):
        result = None
        if log_type == logging.WARNING:
            result = self.__tmp_warning_str
        elif log_type == logging.ERROR:
            result = self.__tmp_error_str
        return result
        
        
class BaseHandle:
    
    support_tool = []
    order = 0
    
    def __init__(self, handle_id=""):
        self._root_widget = None
        self._handle_id = handle_id if handle_id else type(self).__name__
        self.__logger: ToolShelfLogger = None
        self.__create_logger()
        self.setup()
    
    def __create_logger(self):
        self.__logger = ToolShelfLogger.create_logger(type(self).__name__)
    
    @property
    def logger(self):
        return self.__logger
    
    @property
    def bind_tool(self):
        return self._support_tool
    
    def get_bind_tool(self):
        return self._support_tool
    
    def set_bind_tool(self, result: list):
        self._support_tool = result
    
    def export_widget(self) -> unreal.Widget:
        return self._root_widget
    
    def setup(self):
        ...


class SideEntity:
    
    def __init__(self, display_name="", icon_path="", tool_tip="", entity_id=None, bottom=True):
        self.display_name = display_name
        self.icon_path = icon_path
        self.tool_tip = tool_tip if tool_tip else display_name
        self.entity_id = entity_id if entity_id else display_name
        
        
class StackWidgetHandle(BaseHandle):

    instance = False
    fill = False
    
    def __init__(self, entity: SideEntity, handle_id=""):
        self.entity = entity
        super().__init__(handle_id)
        
    def get_handle_id(self):
        return self._handle_id
    ...
    def on_active_changed(self, in_entity: SideEntity, **kwargs):
        ...
    
    def get_logger(self):
        
        ...

        
class Utl:
    
    @staticmethod
    def get_full_icon_path(image_name):
        res_path = pathlib.Path(__file__).parent.joinpath("resources")
        return res_path.joinpath(image_name).as_posix()


def create_size_wrapper(widget):
    size_box = unreal.SizeBox()
    size_box.add_child(widget)
    return size_box

def create_button(text="", icon_path="", size=None):
    layout = unreal.HorizontalBox()
    image = None
    if icon_path and pathlib.Path(icon_path).exists():
        image = unreal.Image()
        texture = unreal.PythonWidgetExtendLib.create_texture2d_from_file(icon_path)
        image.set_brush_from_texture(texture)
    button = unreal.Button()
    if image:
        size_box = create_size_wrapper(image)
        size_box.set_width_override(25)
        size_box.set_height_override(25)
        slot = layout.add_child_to_horizontal_box(size_box)
        slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_CENTER)
        slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
        slot.set_padding(unreal.Margin(3, 0, 0, 0))
    button_text = unreal.TextBlock()
    button_text.font.size = 10
    button_text.set_text(text)
    slot = layout.add_child_to_horizontal_box(button_text)
    slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_RIGHT)
    slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
    slot.set_padding(unreal.Margin(10, 0, 0, 0))
    button.set_content(layout)
    button.set_tool_tip_text(text)
    return button
    
    
    
def create_side_button_with_text(text="", tool_tip="", icon_path="", button_type=unreal.Button.static_class(), display=True) -> unreal.Button:
    layout = unreal.HorizontalBox()
    image = None
    if icon_path and pathlib.Path(icon_path).exists():
        image = unreal.Image()
        texture = unreal.PythonWidgetExtendLib.create_texture2d_from_file(icon_path)
        image.set_brush_from_texture(texture)
        ...
    if button_type == unreal.CheckBox.static_class():
        checked_hover_color = unreal.SlateColor(unreal.LinearColor(0, 0.2, 0.7, 1 if display else int(display)))
        hover_color = unreal.SlateColor(unreal.LinearColor(0, 0.2, 1, 0.8 if display else int(display)))
        press_color = unreal.SlateColor(unreal.LinearColor(0.43, 0.43, 0.43, 1))
        unchecked_color = unreal.SlateColor(unreal.LinearColor(1, 1, 1, 0))
        button = unreal.CheckBox()
        widget_style: unreal.CheckBoxStyle = button.get_editor_property("widget_style")
        widget_style.check_box_type = unreal.SlateCheckBoxType.TOGGLE_BUTTON
        brush = unreal.SlateBrush()
        
        widget_style.checked_hovered_image = brush
        widget_style.checked_image = brush
        widget_style.checked_pressed_image = brush
        # widget_style.checked_hovered_image.set_editor_property("resource_name", "")
        # widget_style.checked_image.set_editor_property("resource_name", "")
        # widget_style.checked_pressed_image.set_editor_property("resource_name", "")
        widget_style.checked_hovered_image.tint_color = press_color if not display else checked_hover_color
        widget_style.checked_image.tint_color = hover_color
        widget_style.checked_pressed_image.tint_color = hover_color
        widget_style.unchecked_pressed_image.tint_color = press_color
        widget_style.unchecked_image.tint_color = unchecked_color
        widget_style.unchecked_hovered_image.tint_color = press_color
        widget_style.unchecked_hovered_image.draw_as = unreal.SlateBrushDrawType.IMAGE
    else:
        button = unreal.Button()
    
    if image:
        size_box = create_size_wrapper(image)
        size_box.set_width_override(25)
        size_box.set_height_override(25)
        slot = layout.add_child_to_horizontal_box(size_box)
        slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_CENTER)
        slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
        slot.set_padding(unreal.Margin(3, 0, 0, 0))
    button_text = unreal.TextBlock()
    button_text.font.size = 10
    button_text.set_text(text)
    #size_box = create_size_wrapper(button_text)
    slot = layout.add_child_to_horizontal_box(button_text)
    slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_RIGHT)
    slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
    slot.set_padding(unreal.Margin(10, 0, 0, 0))
    button.set_content(layout)
    button.set_tool_tip_text(tool_tip)
    return button