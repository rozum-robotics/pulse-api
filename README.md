# Pulse Robot Python API

<a href="https://www.python.org/">
<img alt="Python: 3.5 | 3.6 | 3.7 | 3.8" src="https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-blue.svg">
</a>
<a href="https://pypi.org/project/pulse-api/"><img alt="pypi.org package" src="https://img.shields.io/pypi/v/pulse-api"></a>
<a href="https://github.com/python/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This folder contains `Python` wrapper for the [Pulse Robot](https://rozum.com/robotic-arm/) REST API.
Tested with Python 3. Compatibility with Python 2 is not guaranteed but the underlying API (called `pdhttp`)
supports Python 2.

- [Pulse Robot Python API](#pulse-robot-python-api)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Software compatibility table](#software-compatibility-table)
    - [Getting started](#getting-started)
      - [Quickstart](#quickstart)
      - [API initialization](#api-initialization)
      - [Motion control](#motion-control)
      - [Freedrive mode](#freedrive-mode)
      - [Controlling accessories and signals](#controlling-accessories-and-signals)
      - [Controlling accessories and signals during trajectory execution](#controlling-accessories-and-signals-during-trajectory-execution)
      - [Tool API](#tool-api)
      - [Base API](#base-api)
      - [Environment API](#environment-api)
      - [Exception handling](#exception-handling)
      - [Versions API](#versions-api)
      - [Documentation and further information](#documentation-and-further-information)

[Documentation and further information](#documentation-and-further-information)


## Requirements

Python 3.5+

## Installation

To install from the [Python Package Index](https://pypi.org/project/pulse-api/):

`pip3 install pulse-api`

or, for a specific version

`pip3 install pulse-api==v1.v2.v3`

Alternatively, to get the version from our repository, use the following
command:

`pip3 install pulse-api -i https://pip.rozum.com/simple`  

To install a specific version:

`pip3 install pulse-api==v1.v2.v3 -i https://pip.rozum.com/simple`
where **v1**, **v2**, and **v3** (e.g., pulse-api==1.4.3) are version numbers as listed below in the compatibility table.

**Note:** To install the underlying API (`pdhttp`), use:
`pip3 install pdhttp -i https://pip.rozum.com/simple`

## Software compatibility table

[Changelog](./CHANGELOG.md)

| Pulse Desk UI version | Python API version |
| --------------------- | ------------------ |
| 1.4.3                 | 1.4.3              |
| 1.4.4                 | 1.4.4              |
| 1.5.0, 1.5.1, 1.5.2   | 1.5.0              |
| 1.6.0                 | 1.6.0              |
| 1.7.0                 | 1.7.0, 1.7.1       |
| 1.8.0, 1.8.1          | 1.8.0, 1.8.1       |
| 1.8.2, 1.8.3, 1.8.4   | 1.8.4              |

### Getting started

Examples use the latest version of the library.

#### Quickstart

**WARNING!** Before launching this example, make sure that there are no facilities
within 0.6 meters around the manipulator.

```python
import math
from pulseapi import RobotPulse, pose, position, PulseApiException, MT_LINEAR

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)  # create an instance of the API wrapper class

# create motion targets
home_pose = pose([0, -90, 0, -90, -90, 0])
start_pose = pose([0, -90, 90, -90, -90, 0])
pose_targets = [
    pose([10, -90, 90, -90, -90, 0]),
    pose([10, -90, 0, -90, -90, 0]),
]
position_target = position([-0.42, -0.12, 0.35], [math.pi, 0, 0])
position_targets = [
    position([-0.37, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.17, 0.35], [math.pi, 0, 0]),
    position([-0.37, -0.17, 0.35], [math.pi, 0, 0]),
]

# set the desired speed (controls both motor velocity and acceleration)
SPEED = 30
# set the desired motor velocity
VELOCITY = 40
# set the desired motor acceleration
ACCELERATION = 50
# set the desired tcp velocity
TCP_VELOCITY_1CM = 0.01
TCP_VELOCITY_10CM = 0.1

while True:
    try:
        robot.set_pose(home_pose, speed=SPEED)
        # checks every 0.1 s whether the motion is finished
        robot.await_stop()

        robot.set_pose(start_pose, velocity=VELOCITY, acceleration=ACCELERATION)
        robot.await_stop()

        robot.set_position(
            position_target, velocity=VELOCITY, acceleration=ACCELERATION
        )
        robot.await_stop()

        # command the robot to go through multiple position waypoints
        # (execute a trajectory)
        robot.run_positions(position_targets, SPEED)
        robot.await_stop()

        # set the linear motion type
        robot.run_positions(
            position_targets,
            velocity=VELOCITY,
            acceleration=ACCELERATION,
            motion_type=MT_LINEAR,
        )
        robot.await_stop()

        # limit the TCP velocity not to exceed 0.01 m/s (1 cm/s)
        robot.run_positions(
            position_targets,
            tcp_max_velocity=TCP_VELOCITY_1CM,
            motion_type=MT_LINEAR,
        )
        # checks every 0.5 s whether the motion is finished
        robot.await_stop(0.5)

        # limit the TCP velocity not to exceed 0.1 m/s (10 cm/s)
        robot.run_poses(pose_targets, tcp_max_velocity=TCP_VELOCITY_1CM)

    except PulseApiException as e:
        # handle possible errors
        print("Exception {} while calling robot at {} ".format(e, robot.host))
        break

```

[Back to the table of contents](#pulse-robot-python-api)

#### API initialization

```python
from pulseapi import RobotPulse
# create an instance of the API wrapper class
host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)
```

[Back to the table of contents](#pulse-robot-python-api)

#### Motion control

Possible motion targets:

* Positions (`run_linear_positions`, `set_position`, `run_positions` and `get_position` methods) - to control
the location of the robot's TCP (tool center point). Use the `position` helper function to create a
motion targets.
* Poses (`run_linear_poses`, `set_pose`, `run_poses` and `get_pose` methods) - to control motor angles.
Use the `pose` helper function to create a motion targets.
* Jogging (`jogging` method) - enter the 'jogging' mode. If the robotic arm 
already in the 'jogging' mode, use this method to control the direction of the movement.
Use `jog` helper function to create motion target.
The motion target has six components ('x', 'y', 'z', 'rx', 'ry', 'rz'). 
Components are optional with default value equal to 0. Components control
accelerations along the corresponding axis relative to the _base_ coordinate
system of the robotic arm. To disable the mode, pass `jog` motion target, where
all components are zeros.

Possible motion types:

* Joint (`MT_JOINT`, default)
* Linear (`MT_LINEAR`)

Auxiliary methods:

* `await_motion` - periodically requests robot status (default: every 0.1 s) and
waits until the robot finishes movements. **Deprecated, use await_stop**
* `await_stop` - periodically requests robot status (default: every 0.1 s) and
waits until the robot finishes movements.
* `status_motion` - returns the actual state of the robotic arm: running (arm in motion),
idle (arm not in motion), in the zero gravity mode, or in error state.
**Deprecated, use status**
* `status` - returns the actual state of the robotic arm - whether it is
initializing, or twisted, or running (in motion), or active (not in motion), or 
in the zero gravity mode, or failed (broken, failed initializing or in emergency).
* `freeze` - sets the arm in the "freeze" state.
The arm stops moving, retaining its last position.  
**Note:**  In the state, it is not advisable to move the arm by hand as this
can cause damage to its components.
* `relax` -  sets the arm in the \"relaxed\" state. The arm stops
moving without retaining its last position. In this state, the user can move the
robotic arm by hand (e.g., to verify/test a motion trajectory).
* `pack` - asking the arm to reach a compact pose for transportation.
* `status_motors` - returns the actual states of the six servo motors integrated
into the joints of the robotic arm.
* `stop` - sets the arm in the *Protection mode*. The arm stops moving,
  retaining its last position and is disabled for command execution until
  `recover` is called.

**WARNING!** The following example is sample code. Before running, you must
replace reference motion targets in the sample with the ones applicable to
your specific case. Before launching this example, make sure that manipulator
would not cause any damage to your facilities.

```python
import math
import time
from pulseapi import position, pose, RobotPulse, MT_LINEAR, SystemState, jog

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

# create motion targets
pose_target = pose([0, -90, 90, -90, -90, 0])
position_target = position([-0.42, -0.12, 0.35], [math.pi, 0, 0])
position_targets = [
    position([-0.37, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.17, 0.35], [math.pi, 0, 0]),
    position([-0.37, -0.17, 0.35], [math.pi, 0, 0]),
]
SPEED = 30  # set the desired speed
TCP_VELOCITY_1CM = 0.01


# use the status command as shown below
def my_await_stop(robot_instance, asking_interval=0.1):
    status = robot_instance.status()
    while status == SystemState.MOTION:
        time.sleep(asking_interval)
        status = robot_instance.status()


robot.set_pose(pose_target, SPEED)
robot.await_stop()  # checks every 0.1 s whether the motion is finished
print("Current pose:\n{}".format(robot.get_pose()))

robot.set_position(position_target, SPEED)
robot.await_stop(0.5)  # checks every 0.5 s whether the motion is finished
print("Current position:\n{}".format(robot.get_position()))

# command the robot to go through multiple position waypoints
# (execute a trajectory)
robot.run_positions(position_targets, SPEED)
my_await_stop(robot)

# set the linear motion type
robot.run_positions(position_targets, SPEED, motion_type=MT_LINEAR)
robot.await_stop()

# limit the TCP velocity not to exceed 0.01 m/s (1 cm/s)
robot.run_positions(
    position_targets, tcp_max_velocity=TCP_VELOCITY_1CM, motion_type=MT_LINEAR
)
robot.await_stop()

# stop the arm in the last position
robot.freeze()

# get status from motors
print(robot.status_motors())

# jogging example
# command the robot to execute preparatory motion targets
robot.set_pose(pose([0, -90, 0, -90, -90, 0]), SPEED)
robot.set_position(position([-0.45, -0, 0.33], [math.pi, 0, 0]), SPEED)
robot.await_stop()
# start the jogging mode and execute motion targets
robot.jogging(jog(x=-1, y=-1))
time.sleep(2)
robot.jogging(jog(x=1, y=1))
time.sleep(7)
robot.jogging(jog(rx=1, rz=-1))
time.sleep(5)
robot.jogging(jog(-0.1, -0.8, 0.1, 0, -1, 0.7))
time.sleep(5)
# disable the jogging mode
robot.jogging(jog())

```

The following example demonstrates usage of the `run_linear_positions`
and `run_linear_poses` methods. **Note:** the arm must be
in the first position (pose) of the trajectory before usage.

```python
import math

from pulseapi import (
    RobotPulse,
    pose,
    LinearMotionParameters,
    position,
    InterpolationType,
)

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)  # create an instance of the API wrapper class

SPEED = 25
VELOCITY = 0.3 # in meters per second
ACCELERATION = 0.2 # in meters per second squared
BLEND = 0.01 # in meters - radius of maximum deviation from the trajectory point
HOME_POSE = pose([0, -90, 0, -90, 0, 0])
TARGET_POSITIONS = [
    position([-0.35, 0.3, 0.45], [math.pi, 0.1, 1.57], blend=BLEND),
    position([-0.35, -0.3, 0.45], [math.pi, 0, 0], blend=BLEND),
    position([-0.35, -0.3, 0.5], [math.pi, 0, 0], blend=BLEND),
    position([-0.35, 0.3, 0.5], [math.pi, 0.1, 1.57], blend=BLEND),
]

TARGET_POSES = [
    pose([130, -85, -109, -56, 90, 8], blend=BLEND),
    pose([120, -85, -113, -17, 90, 8], blend=BLEND),
    pose([100, -93, -104, -26, 89, 8], blend=BLEND),
    pose([130, -85, -109, -56, 90, 8], blend=BLEND),
]


linear_motion_parameters = LinearMotionParameters(
    interpolation_type=InterpolationType.BLEND,
    velocity=VELOCITY,
    acceleration=ACCELERATION,
)
robot.set_pose(HOME_POSE, SPEED)
robot.set_position(TARGET_POSITIONS[0], SPEED)
robot.await_stop()
robot.run_linear_positions(
    TARGET_POSITIONS,
    linear_motion_parameters,
)
robot.await_stop()

robot.set_pose(TARGET_POSES[0], SPEED)
robot.await_stop()
robot.run_linear_poses(
    TARGET_POSES,
    linear_motion_parameters,
)
robot.await_stop()
```

[Back to the table of contents](#pulse-robot-python-api)

#### Freedrive mode

Freedrive ("Zero-gravity") mode is intended to be used when there is a need
to control the robotic arm directly "by-hand". With this functionality, for
example, the user can develop an application that remembers user defined path.
After mode activation, you can press and hold specific button that is described
in user manual and move the robotic arm "by-hand".

```python
from pulseapi import RobotPulse

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

# enter freedrive mode
robot.zg_on()

# additional logic goes here

# disable freedrive mode
robot.zg_off()

```

[Back to the table of contents](#pulse-robot-python-api)

#### Controlling accessories and signals

Available methods:

* `close_gripper`, `open_gripper` with a preset timeout before executing further commands (default: 500 ms).
Supported grippers: Schunk and OnRobot.
* `disable_gripper` and `enable_gripper`. Use this methods to disable (enable) power supply on wrist for gripper so
  that you can safely unplug and change gripper without powering off the robotic arm 
* `set_digital_output_high` `set_digital_output_low`, `get_digital_output` - to work with output ports on the controlbox.
* `get_digital_input` to work with input ports on the controlbox.
* `bind_stop` binds `stop` command to high or low input signal on a specific port.

Signals:

* SIG_LOW - port is inactive
* SIG_HIGH - port is active

```python
from pulseapi import RobotPulse, SIG_LOW, SIG_HIGH

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

# ask the robot to close the gripper and continue execution of
# commands after 500 ms
robot.close_gripper()

# ask the robot to open the gripper and begin to execute further
# commands after 100 ms
robot.open_gripper(100)

# set the first output port to the active state
robot.set_digital_output_high(1)

# execute required operations when input port 3 is active
if robot.get_digital_input(3) == SIG_HIGH:
    print("Input port 3 is active")
# execute required operations when input port 1 is inactive
if robot.get_digital_input(1) == SIG_LOW:
    print("Input port 1 is inactive")

# execute stop() command if input singnal is HIGH on input port 4
robot.bind_stop(4, SIG_HIGH)

```

[Back to the table of contents](#pulse-robot-python-api)

#### Controlling accessories and signals during trajectory execution

Use `output_action()`, `open_gripper_action()`, `close_gripper_action()` functions combined with
`pose()` and `position()` helper functions to control gripper/output signals during trajectory
execution.

**Note:** actions are performed asynchronously.

```python
from pulseapi import (
    RobotPulse, 
    SIG_LOW, 
    SIG_HIGH, 
    output_action, 
    position,
    open_gripper_action,
    close_gripper_action,
)

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

# create motion targets with actions

# ask the robot to set output signal to SIG_LOW value on port 1
# when it reaches the specified pose
pose_target = pose([0, -90, 90, -90, -90, 0], [output_action(1, SIG_LOW)])

# ask the robot to set output signal to SIG_HIGH value on port 1
# when it reaches the specified position
position_target = position(
    [-0.42, -0.12, 0.35], [math.pi, 0, 0], [output_action(1, SIG_HIGH)]
)

position_targets = [
    # ask the robot to open gripper at the specified position
    position([-0.37, -0.12, 0.35], [math.pi, 0, 0], [close_gripper_action()]),
    position([-0.42, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.17, 0.35], [math.pi, 0, 0]),
    # ask the robot to close gripper at the specified position and 
    # to set output signal to SIG_LOW value on port 1 at the specified position 
    position([-0.37, -0.17, 0.35], [math.pi, 0, 0], [
        open_gripper_action(),
        output_action(1, SIG_LOW),
    ]),
]
SPEED = 30  # set the desired speed

robot.set_pose(pose_target, SPEED)
robot.await_stop()

robot.set_position(position_target, SPEED)
robot.await_stop()

robot.run_positions(position_targets, SPEED)
robot.await_stop()
```
[Back to the table of contents](#pulse-robot-python-api)

#### Tool API

Use the Tool API methods when you need to calculate a robot motion trajectory with
regard to the used tool and to take the tool into account when the robot calculates collisions.

Available methods:

* `change_tool_info` - set tool info for trajectory calculations.
* `change_tool_shape` - set tool shape for collision validation.
* `get_tool_info`, `get_tool_shape` - receive information about current tool settings.

Helper functions:

* `tool_info` - creates a tool info instance to be passed into
`change_tool_info` method.
* `tool_shape` - creates a tool shape instance to be passed into `change_tool_shape` method.

```python
from pulseapi import RobotPulse, position, Point
from pulseapi import create_simple_capsule_obstacle, tool_shape, tool_info

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

# get info about the current tool
current_tool_info = robot.get_tool_info()
current_tool_shape = robot.get_tool_shape()
print("Current tool info\n{}".format(current_tool_info))
print("Current tool shape\n{}".format(current_tool_shape))

# create new tool properties
new_tool_info = tool_info(position([0, 0, 0.07], [0, 0, 0]), name="CupHolder")
new_tool_shape = tool_shape(
    [create_simple_capsule_obstacle(0.03, Point(0, 0, 0), Point(0, 0, 0.07))]
)

# change tool properties
robot.change_tool_info(new_tool_info)
robot.change_tool_shape(new_tool_shape)
print("New tool info\n{}".format(robot.get_tool_info()))
print("New tool shape\n{}".format(robot.get_tool_shape()))

```

[Back to the table of contents](#pulse-robot-python-api)

#### Base API

Use the Base API methods when you need to calculate a robot motion trajectory
relative to a specific point in space.

Available methods:

* `change_base`
* `get_base`

```python
from pulseapi import RobotPulse, position

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

current_base = robot.get_base()
print("Current base\n{}".format(current_base))

# move the new base point along x and y axes
new_base = position([0.05, 0.05, 0], [0, 0, 0])
robot.change_base(new_base)

print("New base\n{}".format(robot.get_base()))

```

[Back to the table of contents](#pulse-robot-python-api)

#### Environment API

Use the Environment API to add virtual obstacles to be taken into account when calculating collisions.

Available methods:

* `add_to_environment` - adds an obstacle to an environment. Use the helper functions below
to describe obstacles.
* `get_all_from_environment` - returns all obstacles from an environment.
* `get_from_environment_by_name` -  returns an obstacle with a specific name from an environment.
* `remove_all_from_environment` - removes all obstacles from an environment.
* `remove_from_environment_by_name` -  removes an obstacle with a specific name from an environment.

Helper functions:

* `create_box_obstacle`
* `create_capsule_obstacle`
* `create_plane_obstacle`

```python
from pulseapi import RobotPulse, Point, position
from pulseapi import (
    create_plane_obstacle,
    create_box_obstacle,
    create_capsule_obstacle,
)

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

print("Current environment\n{}".format(robot.get_all_from_environment()))
# add obstacles to the environment for calculating collisions
box = create_box_obstacle(
    Point(0.1, 0.1, 0.1), position((1, 1, 1), (0, 0, 0)), "example_box"
)
capsule = create_capsule_obstacle(
    0.1, Point(0.5, 0.5, 0.2), Point(0.5, 0.5, 0.5), "example_capsule"
)
plane = create_plane_obstacle(
    [Point(-0.5, 0.4, 0), Point(-0.5, 0, 0), Point(-0.5, 0, 0.1)],
    "example_plane",
)
robot.add_to_environment(box)
robot.add_to_environment(capsule)
robot.add_to_environment(plane)
print("New environment\n{}".format(robot.get_all_from_environment()))
print(
    "Get example box\n{}".format(robot.get_from_environment_by_name(box.name))
)
# remove specific obstacles
robot.remove_from_environment_by_name(box.name)
print("Environment without box\n{}".format(robot.get_all_from_environment()))
# remove all obstacles from an environment
robot.remove_all_from_environment()
print("Empty environment\n{}".format(robot.get_all_from_environment()))

```

[Back to the table of contents](#pulse-robot-python-api)

#### Exception handling

For information about errors, see the [API reference](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).
The client wraps errors from the robot into `PulseApiException`.

Available methods:

* `recover` - the function recovers the arm after an emergency, setting its motion status to IDLE.
Recovery is possible only after an emergency that is not fatal (corresponds
to the ERROR status).
* `status_failure` - the method  returns complete list of recent failures. Each
  list entry could contain failure message, type, level and datetime. This
  information could be used for error handling or incident investigation.

For example, we can trigger an API exception by sending `pose` into `set_position`
method.

```python
from pulseapi import RobotPulse, PulseApiException, pose, SystemState

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

try:
    robot.set_position(pose([0, -90, 90, -90, -90, 0]), 10)
    robot.await_stop()
except PulseApiException as e:
    print("Exception {}while calling robot at {} ".format(e, robot.host))
    status = robot.status()
    failure = robot.status_failure()
    if status == SystemState.EMERGENCY:
        print("Robot in emergency. Error message: {}".format(failure))

```

If the robotic arm went into "EMERGENCY" state, you can attemt to "recover" the
arm in order to continue operations execution:

```python
from pulseapi import RobotPulse, PulseApiException, pose, SystemState

host = "http://127.0.0.1:8081"  # replace with a valid robot address
robot = RobotPulse(host)

recover_result = robot.recover()
print("Recover result: {}".format(recover_result))

```


[Back to the table of contents](#pulse-robot-python-api)

#### Versions API

Use the Version API methods to get information about the software and hardware versions.
You may need to use the methods for contacting support specialists when you notice
strange robot behaviour.

Available methods:

* `hardware` - returns the hardware versions for all motors, the USB-CAN dongle, safety board and wrist.
* `software` - returns the software version for all motors, the USB-CAN dongle, safety board and wrist.
* `robot_software` - returns the version of the robot control software.

```python
from pulseapi import Versions

host = "http://127.0.0.1:8081"  # replace with a valid robot address
versions = Versions(host)

print(versions.hardware())
print(versions.software())
print(versions.robot_software())

```

[Back to the table of contents](#pulse-robot-python-api)

#### Documentation and further information

For further details, see the
[API reference guide](https://rozum.com/documentation/robotic-arm/pulse-75/rest-api-reference-guide/).
