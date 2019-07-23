from pdhttp.rest import ApiException as PulseApiException
from pdhttp import Point, Rotation, MotionStatus
from pulseapi.environment import (
    create_box_obstacle,
    create_capsule_obstacle,
    create_plane_obstacle,
    create_simple_capsule_obstacle,
)
from pulseapi.constants import MT_JOINT, MT_LINEAR, SIG_HIGH, SIG_LOW
from pulseapi.robot import RobotPulse
from pulseapi.utils import pose, position, tool_info, tool_shape, Versions

try:
    from pulseapi.aiorobot import AioRobotPulse
except ImportError as ie:
    import warnings

    warnings.warn(
        "Asyncio-based client is not available. "
        "To use this feature install pulse-api[aio] "
        "(Run in terminal: pip install -U pulse-api[aio] -i"
        "https://pip.rozum.com/simple)"
    )

RestApiException = PulseApiException  # backward compatibility alias
