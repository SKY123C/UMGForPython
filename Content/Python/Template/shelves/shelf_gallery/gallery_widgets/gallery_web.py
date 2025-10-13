import unreal
from Template import shelf_core
from .. import gallery_class
import os


class GalleryWeb(gallery_class.GallaryWidgetFactory):

    def create(self):   

        layout = unreal.VerticalBox()
        self.line_edit = unreal.EditorUtilityEditableText()
        self.line_edit.on_text_committed.add_callable(self.set_url)
        try:
            self.widget = unreal.WebBrowser()
            # load_url 未将url传递给initoal_url
            self.widget.set_editor_property("initial_url", "https://github.com/SKY123C/UMGForPython/tree/main")
        except Exception as e:
            self.widget = unreal.TextBlock()
            self.widget.set_text("Please load WebBrowser module in Edit->Plugins")
        slot = layout.add_child_to_vertical_box(self.line_edit)
        slot = layout.add_child_to_vertical_box(self.widget)
        slot.size.size_rule = unreal.SlateSizeRule.FILL
        return layout
    
    def set_url(self, url, TextCommit):
        print(url)
        self.widget.load_url(str(url))

    def with_content(self):
        return "Web Browser"
