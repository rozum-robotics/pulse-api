from pdhttp import (
    BoxObstacle,
    CapsuleObstacle,
    PlaneObstacle,
    SimplifiedCapsuleObstacle,
)


def create_box_obstacle(sides, center_position, name="unnamed_box"):
    return BoxObstacle("BOX", name, sides, center_position)


def create_capsule_obstacle(
    radius, start_point, end_point, name="unnamed_capsule"
):
    return CapsuleObstacle("CAPSULE", name, radius, start_point, end_point)


def create_plane_obstacle(points, name="unnamed_plane"):
    return PlaneObstacle("PLANE", name, points)


def create_simple_capsule_obstacle(radius, start_point, finish_point):
    return SimplifiedCapsuleObstacle(
        radius=radius, begin=start_point, finish=finish_point
    )
