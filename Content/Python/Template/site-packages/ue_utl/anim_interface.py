import unreal
import logging
from .utl_interface import (add_logger, 
                            UnrealUTLInterface, 
                            UnrealInterface, 
                            asset_tools,
                            )
from dataclasses import dataclass, astuple
from typing import List
import os


@dataclass
class ImportParams:
    file_path: str = ""
    dst_path: str = ""
    skeleton_path: str = ""
    dst_name: str = ""

def useful_interchanged():
    result = False
    try:
        result = unreal.SystemLibrary.get_console_variable_bool_value('Interchange.FeatureFlags.Import.FBX')
    except Exception as e:
        ...
    return result


class InterchangdScope:
    def __enter__(self):
        self.old_value = useful_interchanged()
        try:
            unreal.SystemLibrary.execute_console_command(None, 'Interchange.FeatureFlags.Import.FBX 0')
        except Exception as e:
            ...
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            unreal.SystemLibrary.execute_console_command(None, f'Interchange.FeatureFlags.Import.FBX {self.old_value}')
        except Exception as e:
            ...
        self.old_value = None


class AnimInterface(UnrealInterface):

    def __init__(self, logger: logging.Logger = None):
        super().__init__(logger)
        self.utl = UnrealUTLInterface(logger)
    
    @add_logger
    def batch_import(self, file_list: List[str], dst_path: str, skeleton_path: str) -> List[unreal.AnimSequence]:
        import_param_list = []
        for i in file_list:
            if os.path.isfile(i) and i.lower().endswith(".fbx"):
                temp = ImportParams()
                temp.file_path = i
                temp.dst_path = dst_path
                temp.skeleton_path = skeleton_path
                import_param_list.append(temp)
        return self.import_animation_file(import_param_list)
    
    @add_logger
    def import_animation_file(self, import_param_list: List[ImportParams]) -> List[unreal.AnimSequence]:
        if useful_interchanged():
            out_anim_seq = self.__import_file_by_interchanged(import_param_list)
        else:
            out_anim_seq = self.__import_file_by_task(import_param_list)
        return out_anim_seq
    
    def __import_file_by_task(self, import_param_list: List[ImportParams]) -> List[unreal.AnimSequence]:
        task_list = []
        for i in import_param_list:
            task = self.__create_animation_task(*astuple(i))
            task_list.append(task)
        if task_list: asset_tools.import_asset_tasks(task_list)
        animation_list = []
        for i in task_list: animation_list.extend(i.get_editor_property("imported_object_paths"))
        animation_list = [unreal.load_asset(i)for i in animation_list if unreal.EditorAssetLibrary.does_asset_exist(i)]
        return animation_list

    def __import_file_by_interchanged(self, import_param_list: List[ImportParams]):
        out_res = []
        for i in import_param_list:
            source_data = unreal.InterchangeManager.create_source_data(i.file_path)
            pipeline = unreal.InterchangeGenericAssetsPipeline()
            import_asset_parameters = unreal.ImportAssetParameters()
            import_asset_parameters.is_automated = True
            import_asset_parameters.replace_existing = True
            import_asset_parameters.override_pipelines.append(unreal.SoftObjectPath(pipeline.get_path_name()))
            if i.dst_name:
                import_asset_parameters.destination_name = i.dst_name
            pipeline.common_skeletal_meshes_and_animations_properties.import_only_animations = True
            self.temp_skeleton = unreal.load_asset(i.skeleton_path)
            pipeline.common_skeletal_meshes_and_animations_properties.skeleton = self.temp_skeleton
            interchange_manager = unreal.InterchangeManager.get_interchange_manager_scripted()
            import_result = interchange_manager.import_asset(i.dst_path, source_data, import_asset_parameters)
            if import_result: out_res.extend(import_result)
        self.temp_skeleton = None
        return out_res

    def __create_animation_task(self, file_path, dst_path, skeleton_path, destination_name=None):
        if unreal.SystemLibrary.get_engine_version().startswith("5"):
            asset_system = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
        else:
            asset_system = unreal.EditorAssetLibrary
        if not asset_system.does_asset_exist(skeleton_path):
            print(skeleton_path + ": 骨骼网格体不存在")
            return
        skele_obj = unreal.load_asset(skeleton_path)
        if skele_obj.get_class() == unreal.SkeletalMesh.static_class():
            skeleton = skele_obj.get_editor_property("skeleton")
        elif skele_obj.get_class() == unreal.Skeleton.static_class():
            skeleton = skele_obj
        else:
            skeleton = None
        if not skeleton:
            print(skeleton_path + ": 骨骼不存在")
            return
        import_task = unreal.AssetImportTask()
        options = unreal.FbxImportUI()
        options.original_import_type = unreal.FBXImportType.FBXIT_ANIMATION
        import_task.replace_existing = True
        import_task.options = options
        import_task.replace_existing_settings = True
        import_task.save = False
        import_task.automated = True
        import_task.filename = file_path
        import_task.destination_path = dst_path
        if destination_name:
            import_task.destination_name = destination_name
        '''
        FbxImportUI配置
        '''
        options.import_animations = True
        options.import_materials = False
        options.import_textures = False
        options.skeleton = skeleton
        options.anim_sequence_import_data.import_translation = unreal.Vector(0.0, 0.0, 0.0)
        options.anim_sequence_import_data.import_rotation = unreal.Rotator(0.0, 0.0, 0.0)
        options.anim_sequence_import_data.import_uniform_scale = 1.0
        # FbxAnimSequenceImportData
        options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
        options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', True)

        return import_task