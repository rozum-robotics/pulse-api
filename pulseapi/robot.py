import time
from deprecated import deprecated

from pdhttp.api.robot_api import RobotApi
from pdhttp.models import MotionStatus
from pulseapi.constants import MT_JOINT


class RobotPulse:
    def __init__(self, host=None):
        self._api = RobotApi()
        if host is not None:
            self._api.api_client.configuration.host = host
        self.logger = self._api.api_client.configuration.logger
        self.host = self._api.api_client.configuration.host

    def add_to_environment(self, obstacle):
        return self._api.add_to_environment(obstacle)

    def change_base(self, base_position):
        return self._api.change_base(base_position)

    def change_tool_info(self, new_tool_info):
        return self._api.change_tool_info(new_tool_info)

    def change_tool_shape(self, new_tool_shape):
        return self._api.change_tool_shape(new_tool_shape)

    def close_gripper(self, timeout=None):
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

    def identifier(self):
        return self._api.identifier()

    def open_gripper(self, timeout=None):
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
        return self._api.run_poses(
            poses,
            **self.__extract_motion_params(
                speed=speed,
                velocity=velocity,
                acceleration=acceleration,
                tcp_max_velocity=tcp_max_velocity,
                motion_type=motion_type,
            )
        )

    def run_positions(
        self,
        positions,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        return self._api.run_positions(
            positions,
            **self.__extract_motion_params(
                speed=speed,
                velocity=velocity,
                acceleration=acceleration,
                tcp_max_velocity=tcp_max_velocity,
                motion_type=motion_type,
            )
        )

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
        return self._api.set_pose(
            target_pose,
            **self.__extract_motion_params(
                speed=speed,
                velocity=velocity,
                acceleration=acceleration,
                tcp_max_velocity=tcp_max_velocity,
                motion_type=motion_type,
            )
        )

    def set_position(
        self,
        target_position,
        speed=None,
        velocity=None,
        acceleration=None,
        tcp_max_velocity=None,
        motion_type=MT_JOINT,
    ):
        return self._api.set_position(
            target_position,
            **self.__extract_motion_params(
                speed=speed,
                velocity=velocity,
                acceleration=acceleration,
                tcp_max_velocity=tcp_max_velocity,
                motion_type=motion_type,
            )
        )

    def status_motion(self):
        return self._api.status_motion()

    def status_motors(self):
        return self._api.status_motors()

    def await_motion(self, asking_interval=0.1):
        while self.status_motion() != MotionStatus.IDLE:
            time.sleep(asking_interval)

    @staticmethod
    def __extract_motion_params(**kwargs):
        return {k: v for k, v in locals()["kwargs"].items() if v is not None}
