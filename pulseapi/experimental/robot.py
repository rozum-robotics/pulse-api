import time
import logging
import functools

from deprecated import deprecated

from pdhttp.api.robot_api import RobotApi
from pdhttp.models import MotionStatus, SystemState
from pulseapi.constants import MT_JOINT
from pulseapi.session import Session, refresh_token


class RobotPulse:
    def __init__(self, session: Session = None, logger: logging.Logger = None):
        self._api = RobotApi()
        self._session = session

        self._api.api_client.configuration.host = self._session.location
        if logger is None:
            logger = logging.getLogger("pulseapi")
            logger.addHandler(logging.NullHandler())

        self.logger = logger
        self.host = self._api.api_client.configuration.host

    @refresh_token
    def add_to_environment(self, obstacle):
        self.logger.debug(str(obstacle))
        return self._api.add_to_environment(obstacle, self._session.token)

    @refresh_token
    def change_base(self, base_position):
        self.logger.debug(str(base_position))
        return self._api.change_base(base_position, self._session.token)

    @refresh_token
    def change_tool_info(self, new_tool_info):
        self.logger.debug(str(new_tool_info))
        return self._api.change_tool_info(new_tool_info, self._session.token)

    @refresh_token
    def change_tool_shape(self, new_tool_shape):
        self.logger.debug(str(new_tool_shape))
        return self._api.change_tool_shape(new_tool_shape, self._session.token)

    @refresh_token
    def close_gripper(self, timeout=None):
        self.logger.debug(str(timeout))
        if timeout is not None:
            return self._api.close_gripper(
                self._session.token, timeout=timeout
            )
        return self._api.close_gripper(self._session.token)

    @refresh_token
    def freeze(self):
        return self._api.freeze(self._session.token)

    @refresh_token
    def get_all_from_environment(self):
        return self._api.get_all_from_environment(self._session.token)

    @refresh_token
    def get_base(self):
        return self._api.get_base(self._session.token)

    @refresh_token
    def get_digital_input(self, port):
        return self._api.get_digital_input(port, self._session.token)

    @refresh_token
    def get_digital_output(self, port):
        return self._api.get_digital_output(port, self._session.token)

    @refresh_token
    def get_from_environment_by_name(self, obstacle_name):
        return self._api.get_from_environment_by_name(
            obstacle_name, self._session.token
        )

    @refresh_token
    def get_pose(self):
        return self._api.get_pose(self._session.token)

    @refresh_token
    def get_position(self):
        return self._api.get_position(self._session.token)

    @refresh_token
    def get_tool_info(self):
        return self._api.get_tool_info(self._session.token)

    @refresh_token
    def get_tool_shape(self):
        return self._api.get_tool_shape(self._session.token)

    @refresh_token
    def information(self):
        return self._api.information(self._session.token)

    @refresh_token
    def identifier(self):
        return self._api.identifier(self._session.token)

    @refresh_token
    def jogging(self, jog_value):
        return self._api.jogging(jog_value, self._session.token)

    @refresh_token
    def open_gripper(self, timeout=None):
        self.logger.debug(str(timeout))
        if timeout is not None:
            return self._api.open_gripper(self._session.token, timeout=timeout)
        return self._api.open_gripper(self._session.token)

    @refresh_token
    def pack(self):
        return self._api.pack(self._session.token)

    @refresh_token
    def recover(self):
        return self._api.recover(self._session.token)

    @refresh_token
    def relax(self):
        return self._api.relax(self._session.token)

    @refresh_token
    def remove_all_from_environment(self):
        return self._api.remove_all_from_environment(self._session.token)

    @refresh_token
    def remove_from_environment_by_name(self, obstacle_name):
        return self._api.remove_from_environment_by_name(
            obstacle_name, self._session.token
        )

    @refresh_token
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
        return self._api.run_poses(
            poses, self._session.token, **motion_parameters
        )

    @refresh_token
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
        return self._api.run_positions(
            positions, self._session.token, **motion_parameters
        )

    @refresh_token
    def set_digital_output_high(self, port):
        return self._api.set_digital_output_high(port, self._session.token)

    @refresh_token
    def set_digital_output_low(self, port):
        return self._api.set_digital_output_low(port, self._session.token)

    @refresh_token
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
        return self._api.set_pose(
            target_pose, self._session.token, **motion_parameters
        )

    @refresh_token
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
        return self._api.set_position(
            target_position, self._session.token, **motion_parameters
        )

    @deprecated(reason="You should use status() method", version="1.6.0")
    @refresh_token
    def status_motion(self):
        result = self._api.status_motion(self._session.token)
        self.logger.debug(result)
        return result

    @refresh_token
    def status(self):
        result = self._api.status(self._session.token)
        self.logger.debug(result)
        return result

    @refresh_token
    def status_motors(self):
        return self._api.status_motors(self._session.token)

    @deprecated(reason="You should use await_stop() method", version="1.6.0")
    def await_motion(self, asking_interval=0.1):
        self.logger.debug(str(asking_interval))
        while self.status_motion() != MotionStatus.IDLE:
            time.sleep(asking_interval)

    def await_stop(self, asking_interval=0.1):
        self.logger.debug(str(asking_interval))
        while self.status() == SystemState.MOTION:
            time.sleep(asking_interval)

    @staticmethod
    def __extract_motion_params(**kwargs):
        return {k: v for k, v in locals()["kwargs"].items() if v is not None}
