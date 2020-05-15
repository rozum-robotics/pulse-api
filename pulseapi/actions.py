from pdhttp.models import (
    RobotAction,
    RobotActionType,
    OutputRobotAction,
    GripperRobotAction,
)

def output_action(port: int, value: str) -> OutputRobotAction:
    """Creates an action to cotrol output ports on the controlbox.

    :param port: port to control (either 1 or 2)
    :type port: int
    :param value: value to set on given port (either SIG_HIGH or SIG_LOW)
    :type value: str
    :return: action that should be executed during trajectory execution
    :rtype: OutputRobotAction
    """
    return OutputRobotAction(RobotActionType.OUTPUT, port, value)

def __gripper_action(value: str) -> GripperRobotAction:
    return GripperRobotAction(RobotActionType.GRIPPER, value)

def open_gripper_action() -> GripperRobotAction:
    """Creates an action to open gripper.

    :return: action that should be executed during trajectory execution
    :rtype: GripperRobotAction
    """
    return __gripper_action("OPEN")

def close_gripper_action() -> GripperRobotAction:
    """Creates an action to close gripper.

    :return: action that should be executed during trajectory execution
    :rtype: GripperRobotAction
    """
    return __gripper_action("CLOSE")
