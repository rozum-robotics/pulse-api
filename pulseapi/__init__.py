from pdhttp.rest import ApiException as PulseApiException
from pdhttp import Point, Rotation, MotionStatus, SystemState
from pulseapi.environment import (
    create_box_obstacle,
    create_capsule_obstacle,
    create_plane_obstacle,
    create_simple_capsule_obstacle,
)
from pulseapi.constants import MT_JOINT, MT_LINEAR, SIG_HIGH, SIG_LOW
from pulseapi.robot import RobotPulse
from pulseapi.utils import pose, position, tool_info, tool_shape, Versions, jog
from pulseapi.actions import (
    close_gripper_action,
    open_gripper_action,
    output_action,
)

try:
    from pulseapi.aiorobot import AioRobotPulse
except ImportError as ie:
    pass  # silent because aiorobot is experimental feature

RestApiException = PulseApiException  # backward compatibility alias
