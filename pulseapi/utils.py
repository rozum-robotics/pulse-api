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
)


def position(point, rotation):
    """Creates position motion target.

    Use this method to create positions which will be passed to set_position and run_positions methods of RobotPulse.

    Example: there is need to move robot's TCP to point with coordinates x=0.3m, y=0.2m, z=0.1m
    and look down vertically relative to base. Call _position((0.3, 0.2, 0.1), (3.1415, 0, 0))_ and pass result to one
    of the methods mentioned earlier.

    :param point: list containing x, y, z coordinates (in meters) where robot should move its TCP
    :param rotation: list containing roll, pitch, yaw coordinates (in radians) for TCP
    :return: Position
    """
    return Position(Point(*point), Rotation(*rotation))


def pose(angles):
    """Creates pose motion target.

    Use this method to create poses which will be passed to set_pose and run_poses methods of RobotPulse.

    :param angles: list containing 6 angles for motors (in degrees). Order: base-0th, tcp-5th
    :return: Pose
    """
    return Pose(angles)


def jog(x=0, y=0, z=0, rx=0, ry=0, rz=0):
    """Creates motion target for jogging mode.
    
    Jogging acceleration is a six-component vector ('x', 'y', 'z', 'rx', 'ry', 'rz'). 
    Components are optional and relative to the base coordinate system of the robotic arm. 
    Default value, corresponding to absense of the movement: 0. 
    Values MUST belong to [-1;1] range inclusively.
    
    """
    return JoggingAcceleration(
        JoggingAccelerationAcceleration(x, y, z, rx, ry, rz)
    )


def tool_info(tcp_position, name="unnamed_tool"):
    return ToolInfo(name=name, tcp=tcp_position)


def tool_shape(shape):
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
