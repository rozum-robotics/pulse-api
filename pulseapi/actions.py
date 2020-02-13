from pdhttp.models import (
    RobotAction,
    RobotActionType,
    OutputRobotAction,
    GripperRobotAction,
)

def output_action(port: int, value: str) -> OutputRobotAction:
    return OutputRobotAction(RobotActionType.OUTPUT, port, value)

def __gripper_action(value: str) -> GripperRobotAction:
    return GripperRobotAction(RobotActionType.GRIPPER, value)

def open_gripper_action() -> GripperRobotAction:
    return __gripper_action("OPEN")

def close_gripper() -> GripperRobotAction:
    return __gripper_action("CLOSE")
