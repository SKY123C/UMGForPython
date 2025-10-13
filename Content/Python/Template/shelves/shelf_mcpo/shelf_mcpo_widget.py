import unreal
from ... import (shelf_core,
                shelf_utl,
                shelf_utl_widgets,
                )
import pathlib
from . import shelf_mcpo_interface


class MCPToolHandle(shelf_core.StackWidgetHandle):
    
    support_tool = ["AI"]
    fill = True

    def __init__(self, entity):
        super().__init__(entity)
    
    def setup(self):
        self._root_widget = unreal.VerticalBox()
        self.create_mcp_widget()

    def create_mcp_widget(self):

        self.mcp_details_view = unreal.DetailsView()
        self.object = shelf_mcpo_interface.mcpo_model.uobject
        self.mcp_details_view.set_object(self.object)
        self.mcp_details_view.on_property_changed.add_callable(self.on_property_changed)
        self._root_widget.add_child_to_vertical_box(self.mcp_details_view)
        shelf_mcpo_interface.create_config()
        # expand_area = unreal.PythonExpandableArea()
        # text = unreal.TextBlock()
        # text.font.size = 10
        # text.set_text("MCP")
        # expand_area.set_expandable_area_head(text)
        # area_layout = unreal.VerticalBox()
        # expand_area.set_expandable_area_body(area_layout)
        # mcpo_list = shelf_mcpo_interface.get_mcpo()
        # for i in mcpo_list:
        #     text = unreal.TextBlock()
        #     text.font.size = 10
        #     text.set_text(i)
        #     button = unreal.CheckBox()
        #     layout = unreal.HorizontalBox()
        #     layout.add_child_to_horizontal_box(text)
        #     layout.add_child_to_horizontal_box(button)
        #     area_layout.add_child_to_vertical_box(layout)
        # slot: unreal.VerticalBoxSlot = self._root_widget.add_child_to_vertical_box(expand_area)
    
    def on_property_changed(self, name):
        shelf_mcpo_interface.refresh_enable_state(name)
        ...