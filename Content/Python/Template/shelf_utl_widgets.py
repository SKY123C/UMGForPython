import unreal
import pathlib
from . import shelf_core

def create_size_wrapper(widget):
    size_box = unreal.SizeBox()
    size_box.add_child(widget)
    return size_box

def create_btn_with_text(text):
    button = unreal.EditorUtilityButton()
    button_text = unreal.TextBlock()
    button_text.font.size = 10
    button_text.set_color_and_opacity(unreal.SlateColor(unreal.LinearColor(1,1,1,1)))
    button_text.set_text(text)
    button_text.font
    button.set_content(button_text)
    button.set_tool_tip_text(text)
    return button

    
@unreal.uclass()
class BaseConfigWidget(unreal.VerticalBox):

    config = unreal.uproperty(unreal.Object)
    details_view = unreal.uproperty(unreal.DetailsView)
    logger = unreal.uproperty(unreal.Object)

    def _post_init(self):
        self.details_view = unreal.DetailsView()
        self.add_child_to_vertical_box(self.details_view)
        #self.details_view.get_editor_property("on_property_changed").add_function(self, "on_property_changed")
    
    def set_object(self, obj):
        self.details_view.set_object(obj)
        self.config = obj

@unreal.uclass()
class ToolBarExpandArea(unreal.PythonExpandableArea):

    text_block = unreal.uproperty(unreal.TextBlock)
    head_layout = unreal.uproperty(unreal.HorizontalBox)

    def _post_init(self):
        self.border_color = unreal.SlateColor(unreal.LinearColor(0.5,0.5,0.5,0.5))
        self.head_layout = unreal.HorizontalBox()
        self.text_block = unreal.TextBlock()
        self.text_block.font.size = 11
        slot = self.head_layout.add_child_to_horizontal_box(self.text_block)
        slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_LEFT)
        slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
        self.set_expandable_area_head(self.head_layout)
    
    def set_text(self, text: str):
        self.text_block.set_text(text)
    
    def add_toolbar_button(self, icon_path, tooltip, radius=10):
        # 向右靠齐
        btn = self.__get_round_btn(icon_path, tooltip, radius)
        slot = self.head_layout.add_child_to_horizontal_box(btn)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
        slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_RIGHT)
        return btn

    def __get_round_btn(self, icon_path, tooltip, radius=10):
        btn: unreal.Button = unreal.EditorUtilityButton()
        btn.set_editor_property("tool_tip_text", tooltip)
        brush = unreal.SlateBrush()
        brush.outline_settings.corner_radii = unreal.Vector4(radius, radius, radius, radius)
        brush.outline_settings.rounding_type = unreal.SlateBrushRoundingType.HALF_HEIGHT_RADIUS
        brush.draw_as = unreal.SlateBrushDrawType.ROUNDED_BOX
        image_size = unreal.DeprecateSlateVector2D()
        image_size.set_editor_property("x", 25)
        image_size.set_editor_property("y", 25)
        brush.image_size = image_size
        brush.outline_settings.width = 0
        brush.resource_object = unreal.PythonWidgetExtendLib.create_texture2d_from_file(icon_path)
        # normal
        btn.widget_style.normal = brush
        # hovere
        brush.outline_settings.color = unreal.SlateColor(unreal.LinearColor(1,1,1,1))
        btn.widget_style.hovered = brush
        # pressed
        brush.outline_settings.color = unreal.SlateColor(unreal.LinearColor(0.5,0.5,0.5,1))
        btn.widget_style.pressed = brush
        return btn
    

@unreal.uclass()
class BaseConfigExpandableWidget(unreal.VerticalBox):

    expandable_area = unreal.uproperty(unreal.PythonExpandableArea)
    body_layout = unreal.uproperty(unreal.VerticalBox)
    help_btn = unreal.uproperty(unreal.Button)
    details_view = unreal.uproperty(unreal.DetailsView)
    logger = unreal.uproperty(unreal.Object)
    config = unreal.uproperty(unreal.Object)

    def _post_init(self):
        self.expandable_area = ToolBarExpandArea()
        self.help_btn = self.expandable_area.add_toolbar_button(shelf_core.Utl.get_full_icon_path("help.png"), "帮助")
        self.expandable_area.border_color = unreal.SlateColor(unreal.LinearColor(0.5,0.5,0.5,0.5))
        self.body_layout = unreal.VerticalBox()
        self.details_view = unreal.DetailsView()
        self.details_view.on_property_changed.add_function(self, "on_property_changed")
        self.body_layout.add_child_to_vertical_box(self.details_view)
        self.expandable_area.set_expandable_area_body(self.body_layout)
        self.add_child_to_vertical_box(self.expandable_area)
        super()._post_init()
    
    def set_text(self, text: str):
        self.expandable_area.set_text(text)
    
    def add_widget(self, widget: unreal.Widget):
        self.body_layout.add_child(widget)

    def set_object(self, obj):
        self.details_view.set_object(obj)
        self.config = obj
    
    @unreal.ufunction(params=[unreal.Name()])
    def on_property_changed(self, property_name):
        if self.property_callback:
            callback = unreal.resolve_python_object_handle(self.property_callback)
            if callback and callable(callback):
                callback(property_name)