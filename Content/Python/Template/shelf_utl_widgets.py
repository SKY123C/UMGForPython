import unreal
import pathlib

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

# @unreal.uclass()
# class StageConfig(unreal.Object):
#     stage = unreal.uproperty(str, meta={"GetOptions": "StageOptions"})

#     @unreal.ufunction(ret=unreal.Array(str))
#     def StageOptions(self):
#         a = unreal.Array()
#         a.append("PVZ")
#         a.append("LAY")
#         return a

# @unreal.uclass()
# class CustomDetailDialog(unreal.PythonWindow):

#     details_view = unreal.uproperty(unreal.DetailsView)
#     config = unreal.uproperty(unreal.Object)

#     def _post_init(self):
#         self.window_text = "选择环节"
#         self.details_view = unreal.DetailsView()
#         vertical_box = unreal.VerticalBox()
#         horizontal_box = unreal.HorizontalBox()
#         self.details_view.set_object(self.config)
#         ok_btn = unreal.EditorUtilityButton()
#         cancel_btn = unreal.EditorUtilityButton()
#         slot = horizontal_box.add_child_to_horizontal_box(ok_btn)
#         slot.size.size_rule = unreal.SlateSizeRule.FILL
#         slot = horizontal_box.add_child_to_horizontal_box(cancel_btn)
#         slot.size.size_rule = unreal.SlateSizeRule.FILL
#         slot = vertical_box.add_child_to_vertical_box(self.details_view)
#         slot.size.size_rule = unreal.SlateSizeRule.AUTOMATIC
#         slot.horizontal_alignment = unreal.HorizontalAlignment.H_ALIGN_FILL
#         vertical_box.add_child_to_vertical_box(horizontal_box)
#         self.set_content(vertical_box)

# config = StageConfig()
# dialog = CustomDetailDialog()
# dialog.details_view.set_object(config)
# unreal.PythonWidgetExtendLib.show_window(dialog, False)
    

