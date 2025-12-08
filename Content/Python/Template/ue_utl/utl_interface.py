import logging
import unreal
import traceback

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry: unreal.AssetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
actor_system: unreal.EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_system = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
seq_subsystem: unreal.LevelSequenceEditorSubsystem = unreal.get_editor_subsystem(unreal.LevelSequenceEditorSubsystem)
editor_asset_system: unreal.EditorAssetSubsystem = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)

class UnrealInterface:

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger


def add_logger(func):
    def wrapper2(*args, **kwargs):
        instance = args[0]
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            if instance.logger:
                instance.logger.error(traceback.format_exc())
            else:
                raise e
        return result
    return wrapper2

class UnrealUTLInterface(UnrealInterface):

    @add_logger
    def create_asset(self, path, name, asset_class, factory):
        """
        创建资产
        """
        if unreal.EditorAssetLibrary.does_asset_exist(f"{path}/{name}"):
            unreal.log_warning(f"Asset {path}/{name} already exists.")
            return None
        return asset_tools.create_asset(name, path, asset_class, factory)

    @add_logger
    def get_asset_by_path(self, path, recursive=False, alllow_class_list=None):
        """
        通过路径获取资产
        """
        if not unreal.EditorAssetLibrary.does_directory_exist(path):
            return []

        asset_data_list = asset_registry.get_assets_by_path(path, recursive=recursive)
        if not asset_data_list:
            return []
        result = []
        for i in asset_data_list:
            if alllow_class_list and i.get_class() in alllow_class_list:
                result.append(i.get_asset())
            elif not alllow_class_list:
                result.append(i.get_asset())
        return result