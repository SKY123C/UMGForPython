import unreal
from . import shelf_core

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


@unreal.uclass()
class BuildArgsWidget(unreal.PythonExpandableArea):

    config = unreal.uproperty(unreal.Object)
    details_view = unreal.uproperty(unreal.DetailsView)
    header_text = unreal.uproperty(unreal.TextBlock)
    import_btn = unreal.uproperty(unreal.EditorUtilityButton)

    logger = unreal.uproperty(unreal.PythonObjectHandle)

    def _post_init(self):
        self.header_text = unreal.TextBlock()
        self.header_text.font.size = 10
        self.set_expandable_area_head(self.header_text)
        self.details_view = unreal.DetailsView()
        main_layout = unreal.VerticalBox()
        self.set_expandable_area_body(main_layout)
        self.set_is_expanded(True)
        self.import_btn = create_btn_with_text("创建")
        self.import_btn.on_clicked.add_function(self, "test")
        #self.import_btn.on_clicked.add_callable(self.test)
        self.border_color = unreal.SlateColor(unreal.LinearColor(0.7,0.7,0.7,1))
        main_layout.add_child_to_vertical_box(self.details_view)
        main_layout.add_child_to_vertical_box(self.import_btn)

    def set_logger(self, logger: shelf_core.ToolShelfLogger):
        """
        设置日志记录器
        """
        self.logger = unreal.create_python_object_handle(logger)

    def set_view_object(self, obj):
        """
        设置详情视图对象
        """
        self.details_view.set_object(obj)
        self.config = obj
        self.header_text.set_text(self.config.scene_type.name)

    @shelf_core.check_status("创建失败")
    def aaa(self):
        print("执行函数")

    @unreal.ufunction()
    def test(self):
        self.aaa()