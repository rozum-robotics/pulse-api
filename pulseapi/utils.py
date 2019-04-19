from pdhttp import Position, Point, Rotation, Pose, Tool


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


def tool(tcp_position, shape, name='unnamed_tool'):
    return Tool(name=name, tcp=tcp_position, shape=shape)
