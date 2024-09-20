import unreal
import pathlib
import os

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

class BaseHandle:
    
    support_tool = []
    order = 0
    
    def __init__(self, handle_id=""):
        self._root_widget = None
        self._handle_id = handle_id if handle_id else type(self).__name__
        self.setup()
        
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
    fill = True
    
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
    button = unreal.EditorUtilityButton()
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
        press_color = unreal.SlateColor(unreal.LinearColor(0.05, 0.05, 0.05, 1))
        button = unreal.EditorUtilityCheckBox()
        widget_style: unreal.CheckBoxStyle = button.get_editor_property("widget_style")
        widget_style.check_box_type = unreal.SlateCheckBoxType.TOGGLE_BUTTON
        widget_style.checked_hovered_image.set_editor_property("resource_name", "")
        widget_style.checked_image.set_editor_property("resource_name", "")
        widget_style.checked_pressed_image.set_editor_property("resource_name", "")
        widget_style.checked_hovered_image.tint_color = press_color if not display else checked_hover_color
        widget_style.checked_image.tint_color = hover_color
        widget_style.checked_pressed_image.tint_color = hover_color
        widget_style.unchecked_pressed_image.tint_color = press_color
        widget_style.unchecked_hovered_image.tint_color = press_color
        widget_style.unchecked_hovered_image.draw_as = unreal.SlateBrushDrawType.IMAGE
    else:
        button = unreal.EditorUtilityButton()
    
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