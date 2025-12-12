import unreal
import pathlib
import os
import logging
import logging.handlers
import abc
from enum import Enum
import tempfile
from typing import Union
import traceback
import contextlib


@unreal.uclass()
class CGTeamWorkFbxImportOptions(unreal.Object):
    
    skeleton = unreal.uproperty(unreal.Skeleton, meta={"DisplayName": "骨 骼", "Category": "参 数"})
    out_directory = unreal.uproperty(unreal.DirectoryPath, meta={"DisplayName": "目标路径", "ContentDir": "", "Category": "参 数"})
    in_directory = unreal.uproperty(unreal.DirectoryPath, meta={"DisplayName": "Fbx文件夹路径", "RelativePath": "", "BlueprintReadOnly": "", "Category": "参 数"})


class HandleType(Enum):
    WIDGET = 0
    COMMAND = 1


class ToolShelfLogger:
    
    logger_list = []
    default_output = None
    
    class LoggerState(Enum):
        
        START = 0
        END = 1
    
    @staticmethod
    def create_logger(logger_name, logger_output=None):
        if not logger_output and ToolShelfLogger.default_output:
            logger_output = ToolShelfLogger.default_output
        result = ToolShelfLogger(logger_name, logger_output)
        ToolShelfLogger.logger_list.append(result)
        return result

    @staticmethod
    def set_default_output(logger_output):
        ToolShelfLogger.default_output = logger_output
    
    def __enter__(self):
        self.begin()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def __init__(self, name, out_object):
        self._logger = logging.getLogger(name)
        if self._logger.hasHandlers():
            for i in self._logger.handlers:
                i.close()
            self._logger.handlers.clear()
        logger_handle = logging.StreamHandler()
        formatter = logging.Formatter('%(filename)s-[line:%(lineno)d]'
                                        '-%(levelname)s-[日志信息]: %(message)s',
                                        datefmt='%Y-%m-%d')
        self.log_str = ""
        self.warning_str= ""
        logger_handle.setFormatter(formatter)
        logger_handle.setStream(self)
        temp_dir = os.path.join(os.path.dirname(__file__), "logs")
        log_path = temp_dir
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        log_name = os.path.join(log_path, f"{self._logger.name}.log")
        fh = logging.handlers.TimedRotatingFileHandler(log_name, when="midnight", interval=1, encoding="utf-8", backupCount=30)
        fh.suffix = "%Y-%m-%d_%H-%M-%S.log"
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                            '-%(levelname)s-[日志信息]: %(message)s',
                                            datefmt='%a, %d %b %Y %H:%M:%S')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
    
        self._logger.addHandler(fh)
        self._logger.addHandler(logger_handle)
        self.out_object = out_object
        self.__tmp_str = ""
        self.__tmp_error_str = ""
        self.__tmp_warning_str = ""
        self.__logger_state = ToolShelfLogger.LoggerState.END
    
    def get_log_path(self):
        temp_dir = tempfile.gettempdir()
        log_path = os.path.join(temp_dir, "ToolShelf")
        
        return os.path.join(log_path, f"{self._logger.name}.log")
    
    def begin(self):
        if self.__logger_state == ToolShelfLogger.LoggerState.START:
            raise SystemError("尚未使用log end")
        self.__tmp_error_str = ""
        self.__tmp_warning_str = ""
        self.__logger_state = ToolShelfLogger.LoggerState.START
        ...
    
    def end(self):
        self.__tmp_str = ""
        self.__logger_state = ToolShelfLogger.LoggerState.END
        ...
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
            for i in text.split("\n"):
                self.out_object.write(log_type, i)

    def get_section_log(self, log_type):
        result = None
        if log_type == logging.WARNING:
            result = self.__tmp_warning_str
        elif log_type == logging.ERROR:
            result = self.__tmp_error_str
        return result

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)


class BaseHandle:
    
    support_tool = []
    padding = [0,0,0,0]
    order = 0
    valid = True
    handle_type = HandleType.WIDGET
    dep = []

    def __init__(self, handle_id=""):
        self._root_widget = None
        self._handle_id = handle_id if handle_id else type(self).__name__
        self.__logger: ToolShelfLogger = None
        self.__create_logger()
    
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
    
    @abc.abstractmethod
    def setup(self):
        ...
    
    def release_reference(self):
        ...
    
    def set_root_widget(self, widget: unreal.Widget):
        self._root_widget = widget


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
        self.entity = [entity]
        super().__init__(handle_id)
        
    def get_handle_id(self):
        return self._handle_id

    def on_active_changed(self, in_entity: SideEntity, **kwargs):
        ...
    
    def get_logger(self):
        
        ...
    def append_entity(self, entity: SideEntity):
        self.entity.append(entity)
        
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


@unreal.uclass()
class LoggerUObject(unreal.Object):

    logger = unreal.uproperty(unreal.PythonObjectHandle)

    def set_logger(self, logger: ToolShelfLogger):
        """
        设置日志记录器
        """
        self.logger = unreal.create_python_object_handle(logger)
        
    def get_logger(self) -> ToolShelfLogger:
        return unreal.resolve_python_object_handle(self.logger)
    

@contextlib.contextmanager
def check_status_scope(in_logger: ToolShelfLogger, message="发生错误，请查看日志"):

    try:
        in_logger.begin()
        yield()
    finally:
        in_logger.end()
    error_message = in_logger.get_section_log(logging.ERROR)
    warning_message = in_logger.get_section_log(logging.WARNING)
    if error_message:
        unreal.EditorDialog.show_message("错误", f"{message}\n{error_message}", unreal.AppMsgType.OK)
    elif warning_message:
        unreal.EditorDialog.show_message("成功", f"操作成功,但存在一些警告\n{warning_message}", unreal.AppMsgType.OK)
    else:
        unreal.EditorDialog.show_message("成功", "操作成功", unreal.AppMsgType.OK)

def check_status(message="发生错误，请查看日志"):
    def wrapper(func):
        def wrapper2(instance: Union[StackWidgetHandle, unreal.Object], *args, **kwargs):
            try:
                t_logger = None

                if isinstance(instance, StackWidgetHandle):
                    t_logger = instance.logger
                elif isinstance(instance, unreal.Object):
                    if not hasattr(instance, "logger"):
                        raise AttributeError("实例没有logger属性")
                    if isinstance(instance.logger, ToolShelfLogger):
                        t_logger = instance.logger
                    elif isinstance(instance.logger, LoggerUObject):
                        t_logger = instance.logger.get_logger()
                    elif isinstance(instance.logger, unreal.PythonObjectHandle):
                        t_logger = unreal.resolve_python_object_handle(instance.logger)
                        ...
                elif hasattr(instance, "logger"):
                    if isinstance(instance.logger, ToolShelfLogger):
                        t_logger = instance.logger
                else:
                    raise TypeError("实例类型不正确")
                t_logger.begin()
                try:
                    func(instance, *args, **kwargs)
                except Exception as e:
                    t_logger.error(traceback.format_exc())
                t_logger.end()
                error_message = t_logger.get_section_log(logging.ERROR)
                warning_message = t_logger.get_section_log(logging.WARNING)
                if error_message:
                    unreal.EditorDialog.show_message("错误", f"{message}\n{error_message}", unreal.AppMsgType.OK)
                elif warning_message:
                    unreal.EditorDialog.show_message("成功", f"操作成功,但存在一些警告\n{warning_message}", unreal.AppMsgType.OK)
                else:
                    unreal.EditorDialog.show_message("成功", "操作成功", unreal.AppMsgType.OK)
            except Exception as e:
                unreal.EditorDialog.show_message("错误", f"执行装饰器失败: {traceback.format_exc()}", unreal.AppMsgType.OK)
        return wrapper2
    return wrapper

class ThreadCategory(Enum):
    
    GAMETHREAD = 0
    CURRENTTHREAD = 0


class ToolShelfSignalInstance:
    
    def __init__(self):
        self.__func_list = []
    
    def connect(self, func, thread_category=ThreadCategory.GAMETHREAD):
        result = (func, thread_category)
        self.__func_list.append(result)
    
    def disconnect(self, func):
        ...
    
    def disconnect_all(self):
        self.__func_list.clear()
    
    def a(self,*args):
        ...
        
    def emit(self, *args):
        for func_tuple in self.__func_list:
            func = func_tuple[0]
            thread_category = func_tuple[1]
            if thread_category == ThreadCategory.GAMETHREAD:
                unreal.executeInMainThreadWithResult(func, *args)
            else:
                func(*args)


class ToolShelfSignal:
    
    def __init__(self, args_type=None):
        self.__signal_instance = ToolShelfSignalInstance()
    
    def __get__(self, obj: object, ower: object):
        return self.__signal_instance


class BaseInterface:

    def __init__(self, logger: ToolShelfLogger):
        self.logger = logger

UMGWIDGET = None

def load_register_hanndles(handle_list: list[BaseHandle]):
    order = []
    graph = {}
    for i in handle_list:
        graph[i.__name__] = i.dep
    # starting ending
    state = {}
    def recursive(class_name):
        if class_name not in graph:
            raise SystemError(f"无法找到类：{class_name}")
        
        if state.get(class_name) == "starting":
            raise SystemError("存在循环依赖")
        if state.get(class_name) == "ending":
            return
        for i in graph.get(class_name, []):
            recursive(i)
        state[class_name] = "ending"
        order.append(class_name)
    
    for i in handle_list:
        recursive(i.__name__)
    res = []
    for i in order:
        for r in handle_list:
            if r.__name__ == i:
                res.append(r)
    return res
