import time
from deprecated import deprecated
import logging

from pdhttp.api.robot_api import RobotApi
from pdhttp.models import MotionStatus, SystemState
from pulseapi.constants import MT_JOINT


class RobotPulse:
    def __init__(self, host=None, logger=None):
        self._api = RobotApi()
        if host is not None:
            self._api.api_client.configuration.host = host
        if logger is None:
            logger = logging.getLogger("pulseapi")
            logger.addHandler(logging.NullHandler())
        self.logger = logger
        self.host = self._api.api_client.configuration.host

    def add_to_environment(self, obstacle):
        self.logger.debug(str(obstacle))
        return self._api.add_to_environment(obstacle)

    def change_base(self, base_position):
        self.logger.debug(str(base_position))
        return self._api.change_base(base_position)

    def change_tool_info(self, new_tool_info):
        self.logger.debug(str(new_tool_info))
        return self._api.change_tool_info(new_tool_info)

    def change_tool_shape(self, new_tool_shape):
        self.logger.debug(str(new_tool_shape))
        return self._api.change_tool_shape(new_tool_shape)

    def close_gripper(self, timeout=None):
        self.logger.debug(str(timeout))
        if timeout is not None:
            return self._api.close_gripper(timeout=timeout)
        return self._api.close_gripper()

    def freeze(self):
        return self._api.freeze()

    def get_all_from_environment(self):
        return self._api.get_all_from_environment()

    def get_base(self):
        return self._api.get_base()

    def get_digital_input(self, port):
        return self._api.get_digital_input(port)

    def get_digital_output(self, port):
        return self._api.get_digital_output(port)

    def get_from_environment_by_name(self, obstacle_name):
        return self._api.get_from_environment_by_name(obstacle_name)

    def get_pose(self):
        return self._api.get_pose()

    def get_position(self):
        return self._api.get_position()

    def get_tool_info(self):
        return self._api.get_tool_info()

    def get_tool_shape(self):
        return self._api.get_tool_shape()

    def information(self):
        return self._api.information()

    def identifier(self):
        return self._api.identifier()

    def jogging(self, jog_value):
        return self._api.jogging(jog_value)

    def open_gripper(self, timeout=None):
        self.logger.debug(str(timeout))
        if timeout is not None:
            return self._api.open_gripper(timeout=timeout)
        return self._api.open_gripper()

    def pack(self):
        return self._api.pack()

    def recover(self):
        return self._api.recover()

    def relax(self):
        return self._api.relax()

    def remove_all_from_environment(self):
        return self._api.remove_all_from_environment()

    def remove_from_environment_by_name(self, obstacle_name):
        return self._api.remove_from_environment_by_name(obstacle_name)

    def run_poses(
        self,
        poses,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        motion_parameters = self.__extract_motion_params(
            speed=speed,
            velocity=velocity,
            acceleration=acceleration,
            tcp_max_velocity=tcp_max_velocity,
            motion_type=motion_type,
        )
        self.logger.debug(
            str(dict(poses=poses, motion_parameters=motion_parameters))
        )
        return self._api.run_poses(poses, **motion_parameters)

    def run_positions(
        self,
        positions,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        motion_parameters = self.__extract_motion_params(
            speed=speed,
            velocity=velocity,
            acceleration=acceleration,
            tcp_max_velocity=tcp_max_velocity,
            motion_type=motion_type,
        )
        self.logger.debug(
            str(dict(positions=positions, motion_parameters=motion_parameters))
        )
        return self._api.run_positions(positions, **motion_parameters)

    def set_digital_output_high(self, port):
        return self._api.set_digital_output_high(port)

    def set_digital_output_low(self, port):
        return self._api.set_digital_output_low(port)

    def set_pose(
        self,
        target_pose,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        motion_parameters = self.__extract_motion_params(
            speed=speed,
            velocity=velocity,
            acceleration=acceleration,
            tcp_max_velocity=tcp_max_velocity,
            motion_type=motion_type,
        )
        self.logger.debug(
            str(dict(pose=target_pose, motion_parameters=motion_parameters))
        )
        return self._api.set_pose(target_pose, **motion_parameters)

    def set_position(
        self,
        target_position,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        motion_parameters = self.__extract_motion_params(
            speed=speed,
            velocity=velocity,
            acceleration=acceleration,
            tcp_max_velocity=tcp_max_velocity,
            motion_type=motion_type,
        )
        self.logger.debug(
            str(
                dict(
                    position=target_position,
                    motion_parameters=motion_parameters,
                )
            )
        )
        return self._api.set_position(target_position, **motion_parameters)

    @deprecated(reason="You should use status() method", version="1.6.0")
    def status_motion(self):
        result = self._api.status_motion()
        self.logger.debug(result)
        return result
    
    def status(self):
        result = self._api.status()
        self.logger.debug(result)
        return result
    
    def status_motors(self):
        return self._api.status_motors()

    @deprecated(reason="You should use await_stop() method", version="1.6.0")
    def await_motion(self, asking_interval=0.1):
        self.logger.debug(str(asking_interval))
        while self.status_motion() != MotionStatus.IDLE:
            time.sleep(asking_interval)

    def await_stop(self, asking_interval=0.1):
        self.logger.debug(str(asking_interval))
        while self.status().state == SystemState.MOTION:
            time.sleep(asking_interval)

    @staticmethod
    def __extract_motion_params(**kwargs):
        return {k: v for k, v in locals()["kwargs"].items() if v is not None}
