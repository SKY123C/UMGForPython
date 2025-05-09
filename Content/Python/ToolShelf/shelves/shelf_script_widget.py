
from .. import shelf_core
import unreal
import os
import threading
import time


@unreal.uclass()
class ScriptToolHandleClass(unreal.Object):
    
    object_class = unreal.uproperty(unreal.Object, meta={"Category": "打 印", "DisplayName": "类 型"})
    debug = unreal.uproperty(bool, meta={"Category": "Debug", "DisplayName": "调试"})
    
    def _post_init(self):
        self.debug = True if os.environ.get("tw_debug") == "True" else False
        
    @unreal.ufunction(meta={"CallInEditor": "true", "DisplayName": "打印所选资产以及属性", "Category": "打 印"})
    def print_selected_assets(self):
        unreal.clear
        for i in unreal.EditorUtilityLibrary.get_selected_assets():
            print(i)
            for j in sorted(dir(i)):
                print(j)
            print("-"* 20)
    
    @unreal.ufunction(meta={"CallInEditor": "true", "DisplayName": "打印所选Actor", "Category": "打 印"})
    def print_selected_actors(self):
        subsystem: unreal.LevelEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        sel_set = subsystem.get_selection_set()
        for i in sel_set.get_selected_objects():
            print(i)
    
    @unreal.ufunction(meta={"CallInEditor": "true", "DisplayName": "多线程打印", "Category": "打 印"})
    def print_number_by_thread(self):
        def a():
            for i in range(10):
                time.sleep(1)
                print(i)
        thread = threading.Thread(target=a)
        thread.start()

    @unreal.ufunction(meta={"CallInEditor": "true", "DisplayName": "打印对象属性(Python)", "Category": "打 印"})
    def print_object_property(self):
        if self.object_class:
            if isinstance(self.object_class, unreal.Class):
                class_name = str(self.object_class.get_name())
                exec(rf"print(*dir(unreal.{class_name}), sep='\n')")
            else:
                print(*dir(self.object_class), sep='\n')
            
    @unreal.ufunction(meta={"CallInEditor": "true", "DisplayName": "GC"})
    def exec_gc(self):
        unreal.SystemLibrary.collect_garbage()
    
    
                       
class ScriptToolHandle(shelf_core.StackWidgetHandle):
    
    support_tool = ["脚本"]
    
    def __init__(self, entity):
        super().__init__(entity)
    
    def setup(self):
        self._root_widget = unreal.VerticalBox()
        self.details_view = unreal.DetailsView()
        self.object = ScriptToolHandleClass()
        self.details_view.set_object(self.object)
        self._root_widget.add_child(self.details_view)
        self.details_view.on_property_changed.add_callable(self.on_property_changed)
        self.layout = unreal.HorizontalBox()
        #self.menu = unreal.MenuAnchor()
        # self.btn = unreal.EditorUtilityButton()
        # text = unreal.TextBlock()
        # text.set_text("Menu")
        # text.font.size = 10
        # self.btn.set_content(text)
        
        #self.btn.on_clicked.add_callable(self.test)
        #self.menu.add_child(self.btn)
        #self.layout.add_child_to_horizontal_box(self.menu)
        #self.menu.get_editor_property("on_get_menu_content_event").bind_callable(self.create)
        self._root_widget.add_child_to_vertical_box(self.layout)
        #self._root_widget.add_child_to_vertical_box(self.input_btn)
    
    def test2(self, input_chord):
        print(2222)
        
    def test(self):
        self.menu.open(True)
        ...
    
    def on_hover(self):
        ...
    
    def on_leave(self):
        print(self.input_chord.escape_keys)
        print(self.input_chord.selected_key)
        print(self.input_chord.selected_key.key.get_editor_property("key_name"))
        a = unreal.InputChord()
        self.input_chord.set_selected_key(a)
        ...
    
    def create(self):
        layout = unreal.VerticalBox()
        for i in range(10):
            btn = unreal.EditorUtilityButton()
            text = unreal.TextBlock()
            text.set_text(str(i))
            text.font.size = 10
            btn.add_child(text)
            layout.add_child_to_vertical_box(btn)
        return layout
        
    def on_property_changed(self, property_name):
        property_name = str(property_name)
        if property_name == "debug":
            os.environ["tw_debug"] = str(getattr(self.object, property_name))