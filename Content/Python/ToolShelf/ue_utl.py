import unreal
import os
import sys
import logging
import traceback
from typing import List

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


class UnrealUTLInterface:

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger


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
    def create_level_sequence_asset(self,path, name, create_camera=False):
        sequence = None
        package_name = unreal.Paths.combine([
            path,
            name])
        if unreal.EditorAssetLibrary.does_asset_exist(package_name):
            sequence = unreal.load_asset(package_name)
        else:
            sequence = self.create_asset(
                path=path,
                name=name,
                asset_class=unreal.LevelSequence.static_class(),
                factory=unreal.LevelSequenceFactoryNew()
            )
        if create_camera:
            self.create_camera_in_sequence(sequence)
        return sequence

    @add_logger
    def create_camera_in_sequence(self, sequence: unreal.MovieSceneSequence, frame_range=[0,150]):
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
        return [actor_binding_proxy, component_binding_proxy, section]

    @add_logger
    def add_subsequence(self, parent_seq: unreal.MovieSceneSequence, children: List[unreal.MovieSceneSequence]):
        for i in children:
            track = parent_seq.add_track(unreal.MovieSceneSubTrack)
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
