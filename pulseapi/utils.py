from typing import Iterable, List, Optional, Union
from pdhttp import (
    Position,
    Point,
    Rotation,
    Pose,
    ToolInfo,
    ToolShape,
    VersionApi,
    JoggingAcceleration,
    JoggingAccelerationAcceleration,
    RobotActionType,
    OutputRobotAction,
    GripperRobotAction,
    RobotAction,
    SimplifiedCapsuleObstacle,
)

ActionsList = List[Union[OutputRobotAction, GripperRobotAction]]


def position(
    point: Iterable[float],
    rotation: Iterable[float],
    actions: Optional[ActionsList] = None,
) -> Position:
    """Creates position motion target.

    Use this method to create positions which will be passed to set_position
    and run_positions methods of RobotPulse.

    Example: there is need to move robot's TCP to point with coordinates
    x=0.3m, y=0.2m, z=0.1m and look down vertically relative to base.
    Call _position((0.3, 0.2, 0.1), (3.1415, 0, 0))_ and pass result to one
    of the methods mentioned earlier.

    :param point: list or tupple containing x, y, z coordinates (in meters)
    where robot should move its TCP
    :type point: Iterable[float]
    :param rotation: list or tupple containing roll, pitch, yaw coordinates
    (in radians) for TCP
    :type rotation: Iterable[float]
    :param actions: list containing actions from pulseapi.actions module,
    defaults to None
    :type actions: Optional[ActionsList], optional
    :return: position motion target
    :rtype: Position
    """
    return Position(Point(*point), Rotation(*rotation), actions)


def pose(
    angles: Iterable[float], actions: Optional[ActionsList] = None
) -> Pose:
    """Creates pose motion target.

    Use this method to create poses which will be passed to set_pose and
    run_poses methods of RobotPulse.

    :param angles: list or tupple containing 6 angles for motors (in degrees).
    Order: base-0th, tcp-5th
    :type angles: Iterable[float]
    :param actions: list containing actions from pulseapi.actions module,
    defaults to None
    :type actions: Optional[ActionsList], optional
    :return: pose motion target
    :rtype: Pose
    """
    return Pose(angles, actions)


def jog(
    x: float = 0,
    y: float = 0,
    z: float = 0,
    rx: float = 0,
    ry: float = 0,
    rz: float = 0,
) -> JoggingAcceleration:
    """Creates motion target for jogging mode.

    Jogging acceleration is a six-component vector
    ('x', 'y', 'z', 'rx', 'ry', 'rz'). Components are optional and relative to
    the base coordinate system of the robotic arm.
    Default value, corresponding to absense of the movement: 0.
    Values MUST belong to [-1;1] range inclusively.

    :param x: x component of the acceleration vector, defaults to 0
    :type x: float, optional
    :param y: y component of the acceleration vector, defaults to 0
    :type y: float, optional
    :param z: z component of the acceleration vector, defaults to 0
    :type z: float, optional
    :param rx: rx component of the acceleration vector, defaults to 0
    :type rx: float, optional
    :param ry: ry component of the acceleration vector, defaults to 0
    :type ry: float, optional
    :param rz: rz component of the acceleration vector, defaults to 0
    :type rz: float, optional
    :return: accelaration to be used in jogging mode
    :rtype: JoggingAcceleration
    """
    return JoggingAcceleration(
        JoggingAccelerationAcceleration(x, y, z, rx, ry, rz)
    )


def tool_info(tcp_position: Position, name: str = "unnamed_tool") -> ToolInfo:
    """Creates new TCP to match the properties of an attached or changed work
    tool.

    :param tcp_position: position that defines the distance (in meters) from the
    arm's mounting flange center point to the new TCP along the x, y, and z axes
    accordingly, rotates the new coordinate system according to the given roll,
    pitch and yaw.
    :type tcp_position: Position
    :param name: any random name of the work tool defined by the user
    (e.g., \"gripper\"), defaults to "unnamed_tool".
    :type name: str, optional
    :return: tool info to be used with change_tool_info() method.
    :rtype: ToolInfo
    """
    return ToolInfo(name=name, tcp=tcp_position)


def tool_shape(shape: List[SimplifiedCapsuleObstacle]) -> ToolShape:
    """Creates new form of the working tool of the robot, which is used in the
    calculation of collisions.

    :param shape: list of simplified capsule obstacles that describe the shape
    of the tool.
    :type shape: List[SimplifiedCapsuleObstacle]
    :return: tool shape to be used with change_tool_shape() method
    :rtype: ToolShape
    """
    return ToolShape(shape=shape)


class Versions:
    def __init__(self, host=None):
        self._api = VersionApi()
        if host is not None:
            self._api.api_client.configuration.host = host

    def hardware(self):
        return self._api.get_hardware_version()

    def software(self):
        return self._api.get_software_version()

    def robot_software(self):
        return self._api.get_robot_software_version()
