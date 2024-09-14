import unreal
from .. import (shelf_core,
                shelf_utl,
                )


class ShelfAction:
    
    def __init__(self, name="", callback=None, icon=""):
        self.name = name
        self.callback = callback
        self.icon = icon
        
@unreal.uclass()
class PythonToolExpandArea(unreal.PythonExpandableArea):
    head_layout = unreal.uproperty(unreal.HorizontalBox)
    
    def _post_init(self) -> None:
        self.head_layout = unreal.HorizontalBox()
        self.set_expandable_area_head(self.head_layout)
        return super()._post_init()
    
    @unreal.ufunction(params=[str])
    def set_header_text(self, text):
        text_block = unreal.TextBlock()
        text_block.set_text(text)
        text_block.font.size = 10
        slot = self.head_layout.add_child_to_horizontal_box(text_block)
        slot.horizontal_alignment = unreal.HorizontalAlignment.H_ALIGN_LEFT
    
    
    
    

class TitleBarHandle(shelf_core.BaseHandle):
    
    def __init__(self):
        self.action_list = []
        self._menu_btn
        super().__init__(self)
    
    def setup(self):
        self._root_widget = unreal.HorizontalBox()
        self.menu_anchor = unreal.MenuAnchor()
        self.main_layout = unreal.HorizontalBox()
        self._root_widget.add_child_to_horizontal_box(self.menu_anchor)
    

    def add_menu(self, name, icon=""):
        menu_anchor = unreal.MenuAnchor()
        self._create_menu_btn(menu_anchor, name, icon)
    
    
    def _create_menu_btn(self, menu_anchor: unreal.MenuAnchor, in_text="", icon=""):
        btn = unreal.Button()
        text = unreal.TextBlock()
        text.font.size = 10
        text.set_text(in_text)
        btn.set_content(text)
        btn.on_clicked.add_callable(lambda: menu_anchor.open(True))
    