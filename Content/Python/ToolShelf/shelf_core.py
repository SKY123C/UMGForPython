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