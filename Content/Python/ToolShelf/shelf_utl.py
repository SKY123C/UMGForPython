import logging
from . import shelf_core
import pathlib
import importlib
import os
import unreal

logger = logging.getLogger("ToolShelf")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

logger_list = [
    
]

def register_all_stack_handle(reload=False):
    '''
    dadsada
    '''
    def check_py(in_path: pathlib.Path):
        return in_path.is_file() and in_path.suffix.lower() == ".py" and not in_path.stem.startswith("__")
    root = "ToolShelf"
    shelf_name = "shelves"
    for x in pathlib.Path(__file__).parent.joinpath(shelf_name).iterdir():
        if check_py(x) and x.stem.startswith("shelf_"):
            module_obj = importlib.import_module(f".{shelf_name}.{x.stem}", root)
            if reload:
                importlib.reload(module_obj)
        elif x.is_dir():
            for x1 in x.iterdir():
                if check_py(x1) and x1.stem.startswith("shelf_"):
                    module_obj = importlib.import_module(f".{shelf_name}.{x.stem}.{x1.stem}", root)
                    if reload:
                        importlib.reload(module_obj)

def get_is_debug():
    tw_debug = os.environ.get("tw_debug")
    result = False
    if tw_debug is not None:
        result = False if os.environ.get("tw_debug") == "False" else True
    return result

def create_animation_task(file_path, dst_path, skeleton_path):
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
    import_task.replace_existing = True
    import_task.options = options
    import_task.save = True
    import_task.automated = True
    import_task.filename = file_path
    import_task.destination_path = dst_path
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

def batch_import_animation(cls, file_list, dst_path, skeleton):
    task_list = []
    for i in file_list:
        task_list.append(create_animation_task(i, dst_path, skeleton))
    if task_list:asset_tools.import_asset_tasks(task_list)


def create_logger(logger_name):
    ...