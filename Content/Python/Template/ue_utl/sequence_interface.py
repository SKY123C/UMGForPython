import unreal
import logging
from .utl_interface import add_logger, UnrealUTLInterface, UnrealInterface, actor_system
from dataclasses import dataclass
from enum import Enum, auto
from typing import List
import os
try:
    import fbx
    import FbxCommon
except ImportError:
    unreal.log_warning("未安装fbx sdk，无法使用相机同步功能")

@dataclass
class SequenceSettings:

    fps: float = property
    frame_start: float = property
    frame_end: float = property
    camera_name: str = ""
    
    @fps
    def fps(self):
        return self._fps
    
    @fps.setter
    def fps(self, value):
        if isinstance(value, str):
            try:
                self._fps = float(value)
            except Exception as e:
                unreal.log_warning("帧率转换失败，使用默认30")
                self._fps = 30.0
        elif isinstance(value, (int, float)):
            self._fps = float(value)
    
    @frame_start
    def frame_start(self):
        return self._frame_start
    
    @frame_start.setter
    def frame_start(self, value):
        if isinstance(value, str):
            try:
                self._frame_start = float(value)
            except Exception as e:
                unreal.log_warning("起始帧转换失败，使用默认0")
                self._frame_start = 1001
        elif isinstance(value, (int, float)):
            self._frame_start = float(value)
        
    @frame_end
    def frame_end(self):
        return self._frame_end
    
    @frame_end.setter
    def frame_end(self, value):
        if isinstance(value, str):
            try:
                self._frame_end = float(value)
            except Exception as e:
                unreal.log_warning("结束帧转换失败，使用默认1100")
                self._frame_end = 1100
        elif isinstance(value, (int, float)):
            self._frame_end = float(value)
    
    def __post_init__(self):
        self.fps = 30.0
        self.frame_start = 1001
        self.frame_end = 1100
    
    def frame_range(self):
        return [int(self.frame_start), int(self.frame_end)]


@dataclass
class ImportParams:
    file_path: str = ""
    dst_path: str = ""
    skeleton_path: str = ""


@dataclass
class CameraSetting:

    focal_length: float = 0
    sensor_width: float = 0
    sensor_height: float = 0
    projection_mode: unreal.CameraProjectionMode = unreal.CameraProjectionMode.PERSPECTIVE
    gate_fit: Enum = auto
    current_aperture: float = 0.0
    constrain_aspect_ratio: bool = False


class SequenceObjectType(Enum):
    SPAWNABLE = 0
    POSSESSABLE = 1


class AddObjectScope:

    def __init__(self, object):
        self.object = object
        self.actor = None

    def __enter__(self):
        self.actor = actor_system.spawn_actor_from_object(self.object, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
        
        return self.actor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.actor:
            actor_system.destroy_actor(self.actor)

class SyncCameraSetting:
    ...
    
    def __init__(self, camera__root):
        self.camera_root = camera__root
    
    def _get_camera_attr(self):
        setting = CameraSetting()
        camera_attr_obj = self.camera_root.GetNodeAttribute()
        if camera_attr_obj.GetApertureMode() == fbx.FbxCamera.EApertureMode.eFocalLength:
            focal_length = camera_attr_obj.FocalLength.Get()
        else:
            fov = camera_attr_obj.FieldOfView.Get()
            focal_length = camera_attr_obj.ComputeFocalLength(fov)
        setting.focal_length = focal_length
        setting.sensor_width = camera_attr_obj.GetApertureWidth()
        setting.sensor_height = camera_attr_obj.GetApertureHeight()
        setting.projection_mode = unreal.CameraProjectionMode.PERSPECTIVE if camera_attr_obj.ProjectionType.Get() == fbx.FbxCamera.EProjectionType.ePerspective else \
                                    unreal.CameraProjectionMode.ORTHOGRAPHIC
        gate_fit = camera_attr_obj.GateFit.Get()
        setting.gate_fit = gate_fit
        return setting

    def parse(self, camera_root, res_width, res_height):
        # 1080 1920  36 24 宽不变，高度变小（变化较小） 24 36 高度变小（变化较大）
        setting = self._get_camera_attr()
        scale = float(res_width) / float(res_height)
        if setting.gate_fit == fbx.FbxCamera.EGateFit.eFitFill:
            setting.sensor_height = setting.sensor_width / scale
        elif setting.gate_fit == fbx.FbxCamera.EGateFit.eFitHorizontal:

            
            ...
        raise NotImplementedError()


class SyncMayaToUECameraSetting:

    def parse(self, camera_root):
        # UE and Maya use horizontal FOV
        camera_attr_obj = camera_root.GetNodeAttribute()

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
            sequence.set_display_rate(unreal.FrameRate(settings.fps,1))
            sequence.set_playback_start(int(settings.frame_start))
            sequence.set_playback_end(int(settings.frame_end))
            sequence.set_work_range_start((int(settings.frame_start) - 100)/settings.fps )
            sequence.set_work_range_end((int(settings.frame_end) + 100)/settings.fps)
            sequence.set_view_range_start((int(settings.frame_start) - 100)/settings.fps)
            sequence.set_view_range_end((int(settings.frame_end) + 100)/settings.fps)

        if create_camera:
            self.create_camera_in_sequence(sequence, settings)
        return sequence

    @add_logger
    def create_camera_in_sequence(self, sequence: unreal.MovieSceneSequence, setting: SequenceSettings, camera_setting: CameraSetting = None):
        camera_actor: unreal.Actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector.ZERO)
        camera_cut_track_list = sequence.find_tracks_by_type(unreal.MovieSceneCameraCutTrack)
        if not camera_cut_track_list:
            camera_cut_track = sequence.add_track(unreal.MovieSceneCameraCutTrack)
        else:
            camera_cut_track = camera_cut_track_list[0]
        cut_section_list = camera_cut_track.get_sections()
        if not cut_section_list:
            cut_section = camera_cut_track.add_section()
        else:
            cut_section = cut_section_list[0]
        frame_range = setting.frame_range()
        cut_section.set_range(*frame_range)
        actor_binding_proxy = sequence.add_spawnable_from_instance(camera_actor)
        component_binding_proxy = sequence.add_possessable(camera_actor.camera_component)
        temp_proxy = component_binding_proxy.get_parent()
        binding_id = sequence.get_portable_binding_id(sequence, actor_binding_proxy)
        cut_section.set_camera_binding_id(binding_id)
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
            #binding_id = unreal.MovieSceneObjectBindingID()
            #binding_id.set_editor_property("guid", actor_binding_proxy.get_id())
            actor_list = unreal.LevelSequenceEditorBlueprintLibrary.get_bound_objects(binding_id)
            for i in actor_list:
                if not unreal.MathLibrary.class_is_child_of(i.get_class(), unreal.Actor.static_class()):
                    continue
                self.set_camera_setting(i, camera_setting)
                i.set_actor_label(setting.camera_name)
                break
            actor_binding_proxy.set_display_name(setting.camera_name)
            unreal.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
            unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(sequence)
        return [actor_binding_proxy, component_binding_proxy, cut_section]
    
    @add_logger
    def set_camera_setting(self, camera_actor: unreal.CineCameraActor, camera_setting: CameraSetting):
        if not camera_setting:
            return
        component: unreal.CineCameraComponent = camera_actor.get_editor_property("camera_component")
        if not component:
            #seq_name = str(actor_binding_proxy.sequence.get_name())
            #raise ValueError(f"{seq_name}: 未找到摄像机组件")
            ...

        # if unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence() == actor_binding_proxy.sequence:
        #     unreal.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
        #     has_opend = True
        film_back = component.get_editor_property("filmback")
        film_back.set_editor_property("sensor_width", camera_setting.sensor_width)
        film_back.set_editor_property("sensor_height", camera_setting.sensor_height)
        component.set_editor_property("filmback", film_back)
        component.set_editor_property("current_focal_length", camera_setting.focal_length)
        component.set_editor_property("current_aperture", camera_setting.current_aperture)
        component.set_editor_property("constrain_aspect_ratio", camera_setting.constrain_aspect_ratio)
        # if has_opend:
        #     unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(actor_binding_proxy.sequence)

    @add_logger
    def import_camera(self, camera_file, sequence: unreal.MovieSceneSequence, camera_binding):
        if not camera_file or not os.path.exists(camera_file):
            self.logger.warning(f"{sequence.get_name()}: 摄像机文件不存在 {camera_file}")
            return
        unreal_editor_system: unreal.UnrealEditorSubsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        cam_import_setting = self.__get_import_camera_setting()
        unreal.SequencerTools.import_level_sequence_fbx(unreal_editor_system.get_editor_world(), 
                                                        sequence, 
                                                        [camera_binding],
                                                        cam_import_setting,
                                                        camera_file)
        #unreal.LevelSequenceEditorBlueprintLibrary.open_level_sequence(sequence)
        if unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence() == sequence:
            unreal.LevelSequenceEditorBlueprintLibrary.close_level_sequence()
        i = camera_binding.get_object_template()
        if not i:
            self.logger.error(f"{sequence.get_name()}: 未找到摄像机模板对象")
            return
        tags: unreal.Array = i.get_editor_property("tags")
        tags.append(unreal.Name(camera_file))
        i.set_editor_property("tags", tags)
        unreal.LevelSequenceEditorBlueprintLibrary.force_update()
    
    def __get_import_camera_setting(self):
        engine_version = unreal.SystemLibrary.get_engine_version()
        import_setting = unreal.MovieSceneUserImportFBXSettings()
        if engine_version.startswith('4.27'):
            import_setting.set_editor_property('create_cameras', False)
            import_setting.set_editor_property('force_front_x_axis', False)
            import_setting.set_editor_property('match_by_name_only', False)
            import_setting.set_editor_property('reduce_keys', False)
            import_setting.set_editor_property('reduce_keys_tolerance', 0.001)
            import_setting.set_editor_property('convert_scene_unit', False)
            import_setting.set_editor_property('import_uniform_scale', 1.0)
            import_setting.set_editor_property('replace_transform_track', True)
        elif engine_version.startswith('5'): #UE5
            import_setting.set_editor_property('create_cameras', False)
            import_setting.set_editor_property('force_front_x_axis', False)
            import_setting.set_editor_property('match_by_name_only', False)
            import_setting.set_editor_property('reduce_keys', False)
            import_setting.set_editor_property('reduce_keys_tolerance', 0.001)
            import_setting.set_editor_property('replace_transform_track', True)
        else:
            raise Exception("不支持的引擎版本")
        return import_setting

    @add_logger
    def add_subsequence(self, parent_seq: unreal.MovieSceneSequence, children: List[unreal.MovieSceneSequence], start_frame=0):
        track_list = parent_seq.find_tracks_by_type(unreal.MovieSceneSubTrack.static_class())
        for i in children:
            for track in track_list:
                section_list = track.get_sections()
                for section in section_list:
                    if section.get_sequence() == i:
                        break
                else:
                    continue
                break
            else:
                track = parent_seq.add_track(unreal.MovieSceneSubTrack)
                section: unreal.MovieSceneSubSection = track.add_section()
                section.set_sequence(i)
            start = 0
            end = i.get_playback_end() - i.get_playback_start()
            track.set_display_name(i.get_name())
            if start_frame:
                start = start_frame
                end = start_frame + i.get_playback_end() - i.get_playback_start()
            section.set_range(start, end)

    @add_logger
    def add_shotsequence(self, parent_seq: unreal.MovieSceneSequence, children: List[unreal.MovieSceneSequence]):
        if not children:
            return
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
    
    @add_logger
    def set_sequence_setting(self, sequence: unreal.MovieSceneSequence, settings: SequenceSettings):
        if not settings:
            return
        rate = sequence.get_display_rate()
        if float(rate.numerator / rate.denominator) != settings.fps:
            sequence.set_display_rate(unreal.FrameRate(settings.fps,1))
        if sequence.get_playback_start() != int(settings.frame_start):
            sequence.set_playback_start(int(settings.frame_start))
        if sequence.get_playback_end() != int(settings.frame_end):
            sequence.set_playback_end(int(settings.frame_end))

    @add_logger
    def set_section_range(self, section: unreal.MovieSceneSection, start, end):
        end = int(end)
        if section.get_start_frame() != int(start):
            section.set_start_frame(int(start))
        if section.get_end_frame() != end:
            section.set_end_frame(end)

    @add_logger
    def set_sequence_playback(self, sequence: unreal.MovieSceneSequence, start, end):
        end = int(end)
        if sequence.get_playback_start() != int(start):
            sequence.set_playback_start(int(start))
        if sequence.get_playback_end() != end:
            sequence.set_playback_end(end)
        fps = sequence.get_display_rate().numerator / sequence.get_display_rate().denominator
        sequence.set_work_range_start((int(start) - 100)/fps )
        sequence.set_work_range_end((int(end) + 100)/fps)
        sequence.set_view_range_start((int(start) - 100)/fps)
        sequence.set_view_range_end((int(end) + 100)/fps)
    
    @add_logger
    def add_object(self, sequence: unreal.MovieSceneSequence, obj: unreal.Object, type: SequenceObjectType):
        binding_proxy = None
        if obj:
            unreal.SkeletalMesh.static_class()
            with AddObjectScope(obj) as actor:
                if type == SequenceObjectType.SPAWNABLE:
                    binding_proxy = sequence.add_spawnable_from_instance(actor)
                    actor_system.destroy_actor(actor)
                elif type == SequenceObjectType.POSSESSABLE:
                    binding_proxy = sequence.add_possessable(actor)
        return binding_proxy