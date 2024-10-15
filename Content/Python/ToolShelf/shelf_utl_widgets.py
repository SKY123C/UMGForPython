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
    button_text.set_text(text)
    button.set_content(button_text)
    button.set_tool_tip_text(text)
    return button