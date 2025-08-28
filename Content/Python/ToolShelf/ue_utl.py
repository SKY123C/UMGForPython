import unreal
import os
import sys
import logging
import traceback
from typing import List
from dataclasses import dataclass

CURRENT_LOGGER = None

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
asset_registry: unreal.AssetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
actor_system: unreal.EditorActorSubsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
asset_system = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)


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

@dataclass
class SequenceSettings:
    fps: str = "30"
    frame_start: str = "0"
    frame_end: str = "100"
    camera_name: str = ""

    def __post_init__(self):
        try:
            float(self.fps)
        except Exception as e:
            unreal.log_warning("帧率转换失败，使用默认30")
            self.fps = "30"
        try:
            float(self.frame_start)
        except Exception as e:
            unreal.log_warning("起始帧转换失败，使用默认0")
            self.frame_start = "0"
        try:
            float(self.frame_end)
        except Exception as e:
            unreal.log_warning("结束帧转换失败，使用默认100")
            self.frame_end = "100"
    
    def frame_range(self):
        return [int(self.frame_start), int(self.frame_end)]

class UnrealInterface:

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger


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


class UnrealSequenceInterface(UnrealInterface):

    def __init__(self, logger: logging.Logger = None):
        super().__init__(logger)
        self.utl = UnrealUTLInterface(logger)

    @add_logger
    def create_level_sequence_asset(self,path, name, create_camera=False, settings: SequenceSettings = SequenceSettings()):
        sequence: unreal.MovieSceneSequence = None
        package_name = unreal.Paths.combine([
            path,
            name])
        if unreal.EditorAssetLibrary.does_asset_exist(package_name):
            sequence = unreal.load_asset(package_name)
        else:
            sequence = self.utl.create_asset(
                path=path,
                name=name,
                asset_class=unreal.LevelSequence.static_class(),
                factory=unreal.LevelSequenceFactoryNew()
            )
        if settings:
            sequence.set_display_rate(unreal.FrameRate(int(settings.fps),1))
            sequence.set_playback_start(int(settings.frame_start))
            sequence.set_playback_end(int(settings.frame_end))
        if create_camera:
            self.create_camera_in_sequence(sequence, settings)
        return sequence

    @add_logger
    def create_camera_in_sequence(self, sequence: unreal.MovieSceneSequence, setting: SequenceSettings):
        camera_actor: unreal.Actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector.ZERO)
        camera_cut_track_list = sequence.find_tracks_by_type(unreal.MovieSceneCameraCutTrack)
        if not camera_cut_track_list:
            camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
        else:
            camera_cut_track = camera_cut_track_list[0]
        cut_section_list = camera_cut_track.get_sections()
        if not cut_section_list:
            section = camera_cut_track.add_section()
        else:
            section = cut_section_list[0]
        frame_range = setting.frame_range()
        section.set_range(*frame_range)
        actor_binding_proxy = sequence.add_spawnable_from_instance(camera_actor)
        component_binding_proxy = sequence.add_possessable(camera_actor.camera_component)
        temp_proxy = component_binding_proxy.get_parent()
        binding_id = sequence.get_portable_binding_id(sequence, actor_binding_proxy)
        section.set_camera_binding_id(binding_id)
        component_binding_proxy.set_parent(actor_binding_proxy)
        temp_proxy.remove()
        track = actor_binding_proxy.add_track(unreal.MovieScene3DTransformTrack)
        track.set_property_name_and_path("Transform", "Transform")
        section = track.add_section()
        section.set_end_frame_bounded(False)
        section.set_start_frame_bounded(False)
        actor_system.destroy_actor(camera_actor)
        if setting.camera_name:
            unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(sequence)
            unreal.LevelSequenceEditorBlueprintLibrary.force_update()
            binding_id = unreal.MovieSceneObjectBindingID()
            binding_id.set_editor_property("guid", actor_binding_proxy.get_id())
            actor_list = unreal.LevelSequenceEditorBlueprintLibrary.get_bound_objects(binding_id)
            for i in actor_list:
                if not unreal.MathLibrary.class_is_child_of(i.get_class(), unreal.Actor.static_class()):
                    continue
                i.set_actor_label(setting.camera_name)
                break
            actor_binding_proxy.set_display_name(setting.camera_name)
        return [actor_binding_proxy, component_binding_proxy, section]

    @add_logger
    def add_subsequence(self, parent_seq: unreal.MovieSceneSequence, children: List[unreal.MovieSceneSequence]):
        for i in children:
            track = parent_seq.add_track(unreal.MovieSceneSubTrack)
            track.set_display_name(i.get_name())
            section: unreal.MovieSceneSubSection = track.add_section()
            section.set_sequence(i)
            section.set_range(0, i.get_playback_end() - i.get_playback_start())
    
    @add_logger
    def add_shotsequence(self, parent_seq: unreal.MovieSceneSequence, children: List[unreal.MovieSceneSequence]):
        shot_track = parent_seq.add_track(unreal.MovieSceneCinematicShotTrack)
        count = 0
        for index, i in enumerate(children):
            start = i.get_playback_start()
            end = i.get_playback_end()
            offset = end - start
            section: unreal.MovieSceneCinematicShotSection = shot_track.add_section()
            section.set_sequence(i)
            #section.set_row_index(index)
            section.set_range(count, count + offset)
            count += offset

    @add_logger
    def get_specified_section(self, sequence: unreal.MovieSceneSequence, in_section_class) -> List[unreal.MovieSceneSection]:
        result = []
        for i in sequence.get_tracks():
            section_list = i.get_sections()
            for j in section_list:
                if unreal.MathLibrary.class_is_child_of(j.get_class(), in_section_class):
                    result.extend(section_list)
                break
        return result

    @add_logger
    def get_template_object_for_bp(self, object_template: unreal.Blueprint):
        '''
        自行销毁对象 destroy_actor
        '''
        if not unreal.MathLibrary.class_is_child_of(object_template, unreal.Blueprint):
            unreal.log_error("传入的不是蓝图对象")
            return
        
        gen_class = object_template.get_class()
        temp_spawn_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(gen_class, unreal.Vector(0, 0, 0),
                                                                            unreal.Rotator(0, 0, 0))
        
        return temp_spawn_actor