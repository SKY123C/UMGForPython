import unreal
import pathlib
from . import shelf_core
import traceback


def create_button_with_text(text="", tool_tip="", icon_path="", button_type=unreal.Button.static_class(), display=True) -> unreal.Button:
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

def create_size_wrapper(widget):
    size_box = unreal.SizeBox()
    size_box.add_child(widget)
    return size_box


class StackedWidgetHandle:
    
    def __init__(self, entity_list: list[shelf_core.SideEntity], side_color):
        ...
        self.side_size = unreal.Vector2D()
        self.side_size.x = 40
        self.side_size.y = 150
        self.side_icon_size = unreal.Vector2D()
        self.side_icon_size.x = 20
        self.entity_list = entity_list
        self.side_button_size = 40
        self.side_color: unreal.LinearColor = side_color
        self._handle_list: list[shelf_core.StackWidgetHandle] = []
        self._handle_instance_list: list[shelf_core.StackWidgetHandle] = []
        self.register_handles()
        self.setup()
    
    def setup(self):
        self.container_widget = unreal.WidgetSwitcher()
        self.main_layout = unreal.VerticalBox()
        h_layout = unreal.HorizontalBox()
        slot = self.main_layout.add_child_to_vertical_box(h_layout)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
        self.tool_main_v_box = unreal.VerticalBox()
        
        self.tool_size_box = unreal.SizeBox()
        self.side_border = unreal.Border()
        self.side_border.set_brush_color(self.side_color)
        self.tool_size_box.set_width_override(self.side_size.x)
        slot = h_layout.add_child_to_horizontal_box(self.tool_size_box)
        #slot.size.size_rule = unreal.SlateSizeRule.FILL
        slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_LEFT)
        
        slot = h_layout.add_child_to_horizontal_box(self.container_widget)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
        scroll = unreal.EditorUtilityScrollBox()
        
        self.tool_size_box.add_child(self.side_border)
        slot = self.side_border.add_child(scroll)
        slot.set_editor_property("padding", unreal.Margin())
        #self.tool_size_box.add_child(scroll)
        
        self.utl_tool_side_layout = unreal.VerticalBox()
        self.tool_side_layout = unreal.VerticalBox()
        self.tool_main_v_box.add_child_to_vertical_box(self.utl_tool_side_layout)
        slot = self.tool_main_v_box.add_child_to_vertical_box(self.tool_side_layout)
        #slot.size.size_rule = unreal.SlateSizeRule.FILL
                
        slot: unreal.ScrollBoxSlot = scroll.add_child(self.tool_main_v_box)
        self.button_list: list[dict] = []
        self.add_utl()
        self.add_tool_box()
    
    def _modify_side_property(self, check_state):
        self.side_border.background.draw_as = unreal.SlateBrushDrawType.BORDER
        if check_state:
            ...
            self.side_border.background.draw_as = unreal.SlateBrushDrawType.BORDER
            self.side_border.background.margin = unreal.Margin(1,1,1,1)
            color = unreal.LinearColor(1, 1, 1, 0.2)
            #color = unreal.LinearColor(228/255, 228/255, 228/255, 1)
        else:
            self.side_border.background.draw_as = unreal.SlateBrushDrawType.NO_DRAW_TYPE
            color = self.side_color
        self.side_border.set_brush_color(color)
        self.tool_size_box.set_width_override(self.side_size.y if check_state else self.side_size.x)
        
    @property
    def export_widget(self):
        return self.main_layout
    
    def add_tool_box(self):
                
        for i in self.entity_list:
            button = create_button_with_text(i.display_name, i.tool_tip, i.icon_path, unreal.CheckBox.static_class())
            button.set_is_checked(self.default_is_checked(i.display_name))
            self.button_list.append({i:button})
            wrapper = self._switch(i)
            button.on_check_state_changed.add_callable(wrapper)
            #tw_animation_widget.AnimationToolHandle().export_widget()
            scroll_box, layout = self.create_container_child()
            self.container_widget.add_child(scroll_box)
            for handle_class in self._handle_list:
                if i.entity_id in handle_class.support_tool:
                    handle_ins = None
                    try:
                        if handle_class.instance:
                            result = [j for j in self._handle_instance_list if isinstance(j, handle_class)]
                            handle_ins = result[0] if result else None
                        else:
                            handle_ins = handle_class(i)
                        if not handle_ins:
                            raise
                        widget = handle_ins.export_widget()
                    except Exception as e:
                        widget = unreal.TextBlock()
                        widget.font.size = 10
                        widget.set_is_read_only(True)
                        widget.set_text("加载失败\n" + traceback.format_exc())
                    if handle_ins:self._handle_instance_list.append(handle_ins)
                    layout.add_child_to_vertical_box(widget)
            size_box = create_size_wrapper(button)
            size_box.set_width_override(self.side_button_size)
            size_box.set_height_override(self.side_button_size)
            self.tool_side_layout.add_child(size_box)
    
    def add_utl(self):
        self.home_button = create_button_with_text(icon_path=shelf_core.Utl.get_full_icon_path("home.png"), button_type=unreal.CheckBox.static_class(), display=False)
        size_box = create_size_wrapper(self.home_button)
        size_box.set_width_override(self.side_button_size)
        size_box.set_height_override(self.side_button_size)
        # self.tool_size_box.set_width_override(self.side_size.x if state else self.side_size.y
        self.home_button.on_check_state_changed.add_callable(self._modify_side_property)
        self.utl_tool_side_layout.add_child(size_box)
    
    def _switch(self, in_checkbox_id: shelf_core.SideEntity):
        def wrapper(check_state: bool):
            if check_state:
                for index, i in enumerate(self.button_list):
                    check_box_id, button  = list(i.items())[0]
                    if in_checkbox_id != check_box_id:
                        button.set_is_checked(False)
            else:
                for index, i in enumerate(self.button_list):
                    check_box_id, button  = list(i.items())[0]
                    if in_checkbox_id == check_box_id:
                        current_button = button
                    if button.is_checked():
                        break
                else:
                    current_button.set_is_checked(True)
                    ...
            for index, i in enumerate(self.button_list):
                for j, button in i.items():
                    if button.is_checked():
                        
                        self.update_container_vis(index)
                        break
            a = [index for index, i in enumerate(self.button_list) for j, button in i.items() if button.is_checked()]
            for i in self._handle_instance_list:
                i.on_active_changed(in_checkbox_id)
            self.update_container_vis(a[0])
        return wrapper
    
    def default_is_checked(self, name):
        return True if name == "动画" else False
            
    def create_container_child(self):
        scroll_box = unreal.EditorUtilityScrollBox()
        border = unreal.Border()
        border.set_brush_color(unreal.LinearColor(4/255, 4/255, 4/255, 1))
        layout = unreal.VerticalBox()
        border.set_content(layout)
        slot: unreal.ScrollBoxSlot = scroll_box.add_child(border)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
        return scroll_box, layout
    
    def update_container_vis(self, index):
        self.container_widget.set_active_widget_index(index)
    
    def register_handles(self):
        self._handle_list = shelf_core.StackWidgetHandle.__subclasses__()
        self._handle_list.sort(key=lambda x: x.order)
        for i in self._handle_list:
            print(i)
            if i.instance:
                for entity in self.entity_list:
                    if entity.display_name in i.support_tool:
                        self._handle_instance_list.append(i(entity))

class CGTeamWorkWindow:
    
    def __init__(self):
        self.setup()
    
    def setup(self):
        self.entity_list = [
            shelf_core.SideEntity("动画",icon_path=shelf_core.Utl.get_full_icon_path("animation.png")),
            shelf_core.SideEntity("材质",icon_path=shelf_core.Utl.get_full_icon_path("material.png")),
            shelf_core.SideEntity("定序器",icon_path=shelf_core.Utl.get_full_icon_path("sequence.png")),
            shelf_core.SideEntity("CGTeamWork",icon_path=shelf_core.Utl.get_full_icon_path("cgteamwork.png")),
            shelf_core.SideEntity("脚本",icon_path=shelf_core.Utl.get_full_icon_path("code.png")),
            shelf_core.SideEntity("通用",icon_path=shelf_core.Utl.get_full_icon_path("utl.png")),
            shelf_core.SideEntity("日志",icon_path=shelf_core.Utl.get_full_icon_path("log.png")),
        ]
        self.main_layout = unreal.VerticalBox()
        self.border = unreal.Border()
        color = unreal.LinearColor(0, 0, 0, 0.001)
        self.border.set_brush_color(color)
        slot = self.main_layout.add_child_to_vertical_box(self.border)
        self.main_handle = StackedWidgetHandle(self.entity_list, color)
        self.border.set_content(self.main_handle.export_widget)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
