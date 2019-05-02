# Pulse Robot Python API 

This folder contains `Python` wrapper for the [pulse robot](https://rozum.com/robotic-arm/) REST API. 
Tested with Python 3. Compatibility with Python 2 is not guaranteed but the underlying API (called `pdhttp`) 
is generated using [swagger-codegen](https://github.com/swagger-api/swagger-codegen) so it may work for you.

## Requirements
Python 3.4+

### Installation

To get the latest version use the following command: 
`pip install pulse-api --trusted-host pip.rozum.com -i http://pip.rozum.com/simple`  

To install a specific version: 
`pip install pulse-api==v1.v2.v3 --trusted-host pip.rozum.com -i http://pip.rozum.com/simple`
where **v1**, **v2**, and **v3** (e.g. pulse-api==1.4.3) are version numbers as listed below in the compatibility table.

### Software compatibility table
Pulse desk version  | Python api version
------------------- |-------------------
1.4.3               | 1.4.3

### Getting started
Examples use the latest version of library. 

Examples:
* [API initialization](#api-initialization)
* [Motion control](#motion-control)
* [Controlling accessories and signals](#controlling-accessories-and-signals)
* ["Tool" API](#tool-api)
* ["Base" API](#base-api)
* ["Environment" API](#environment-api)
* [Exception handling](#exception-handling)
* ["Versions" API](#versions-api)

[Documentation and further information](#documentation-and-further-information)

#### API initialization
```python
from pulseapi import RobotPulse
# create an instance of the API wrapper class
host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)
```
[Back to table of contents](#getting-started)

#### Motion control
Possible motion targets:
* Positions (`set_position`, `run_positions` and `get_position` methods) - to control 
the location of the robot's TCP (tool center point). Use the `position` helper method to create a 
motion target.
* Poses (`set_pose`, `run_poses` and `get_pose` methods) - to control motor angles.
Use the `pose` helper method to create the motion target.

Possible motion types:
* Joint (`MT_JOINT`, default)
* Linear (`MT_LINEAR`)

Auxiliary methods:
* `await_motion` - periodically requests robot status and waits until robot finishes 
movements. **To be replaced soon.**
* `status_motion` - returns the actual state of the robotic arm: running (arm in motion), 
idle (arm not in motion), in the zero gravity mode, 
or in error state.
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

**WARNING!** The following example is sample code. Before running, you must 
replace reference motion targets in the sample with the ones applicable to
your specific case. Before launching this example make sure that manipulator 
would not cause any damage to your facilities.

```python
import math
import time
from pulseapi import position, pose, RobotPulse, MT_LINEAR, MotionStatus

host = "127.0.0.1:8080"  # replace with valid robot address 
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

# example of using the motion status command
def my_await_motion(robot_instance, asking_interval=0.1):
    status = robot_instance.status_motion()
    while status != MotionStatus.IDLE:
        time.sleep(asking_interval)
        status = robot_instance.status_motion()

robot.set_pose(pose_target, SPEED)
robot.await_motion()  # waits the end of motion
print('Current pose:\n{}'.format(robot.get_pose()))

robot.set_position(position_target, SPEED)
robot.await_motion(0.5) # checks whether the motion is finished finishes every 0.5 s
print('Current position:\n{}'.format(robot.get_position()))

# robot should go through multiple position waypoints (trajectory)
robot.run_positions(position_targets, SPEED)
my_await_motion(robot)

# set linear motion type
robot.run_positions(position_targets, SPEED, motion_type=MT_LINEAR)
robot.await_motion()

# limit TCP velocity to be not greater than 1 cm/s
robot.run_positions(position_targets, SPEED, 
    motion_type=MT_LINEAR, tcp_max_velocity=0.01)
robot.await_motion()

# stop the arm in the last position
robot.freeze()

# get status from motors
print(robot.status_motors())

```
[Back to the table of contents](#getting-started)

#### Controlling accessories and signals
Available methods:
* `close_gripper`, `open_gripper` with a preset timeout before continuing execution of commands (default: 500 ms). 
Supported grippers: Schunk and OnRobot.
* `set_digital_output_high` `set_digital_output_low`, `get_digital_output` with provided port.
* `get_digital_input` with provided port.

Signals:
* SIG_LOW - port is inactive
* SIG_HIGH - port is active

```python
from pulseapi import RobotPulse, SIG_LOW, SIG_HIGH

host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)

# ask the robot to close the gripper and continue execution of commands after 500 ms
robot.close_gripper() 

# ask the robot to open the gripper and begin to execute further commands immediately 
robot.open_gripper(0)

# set the first output port to the active state
robot.set_digital_output_high(1)

# execute some operations when input port 3 is active
if robot.get_digital_input(3) == SIG_HIGH:
    print('Input port 3 is active')
# execute some operations when input port 1 is inactive
if robot.get_digital_input(1) == SIG_LOW:
    print('Input port 1 is inactive')
```
[Back to the table of contents](#getting-started)

#### Tool API
Use the Tool API methods when you need to calculate a robot motion trajectory with
regard to the used tool and to take the tool into account when the robot calculates collisions.

Available methods:
* `change_tool_info` - info to be used in trajectory calculation
* `change_tool_shape` - pass info to be used for collision validation
* `get_tool_info`, `get_tool_shape` - receive information about current settings

Helper functions:
* `tool_info` - creates a tool info instance to be passed into 
`change_tool_info` method.
* `tool_shape` - creates a tool shape instance to be passed into `change_tool_shape` method.

```python
from pulseapi import RobotPulse, position, Point
from pulseapi import create_simple_capsule_obstacle, tool_shape, tool_info

host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)

# get info about the current tool
current_tool_info = robot.get_tool_info()
current_tool_shape = robot.get_tool_shape()
print('Current tool info\n{}'.format(current_tool_info))
print('Current tool shape\n{}'.format(current_tool_shape))

# create new tool properties
new_tool_info = tool_info(position([0, 0, 0.07], [0, 0, 0]), name='CupHolder')
new_tool_shape = tool_shape([
    create_simple_capsule_obstacle(0.03, Point(0, 0, 0), Point(0,0,0.07))
])

# change tool properties
robot.change_tool_info(new_tool_info)
robot.change_tool_shape(new_tool_shape)
print('New tool info\n{}'.format(robot.get_tool_info()))
print('New tool shape\n{}'.format(robot.get_tool_shape()))

```
[Back to table of contents](#getting-started)

#### Base API
Sometimes it is convenient to calculate trajectory relatively to some specific 
point in space.

Provided methods: 
* `change_base`
* `get_base`

```python
from pulseapi import RobotPulse, position

host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)

current_base = robot.get_base()
print('Current base\n{}'.format(current_base))

# move the new base point along x and y axes
new_base = position([0.05, 0.05, 0], [0, 0, 0])
robot.change_base(new_base)

print('New base\n{}'.format(robot.get_base()))

```
[Back to the table of contents](#getting-started)

#### Environment api
Add virtual obstacles to take into account while calculating collisions.

Provided methods:
* `add_to_environment` - add obstacle to environment. Use helper functions 
listed below to create objects that should be provided to this method.
* `get_all_from_environment` - return all obstacles from environment.
* `get_from_environment_by_name` -  return obstacle from environment by name.
* `remove_all_from_environment` - remove all obstacles from robot environment.
* `remove_from_environment_by_name` -  remove obstacle from robot environment by name.

Helper functions:
* `create_box_obstacle`
* `create_capsule_obstacle`
* `create_plane_obstacle`

```python
from pulseapi import RobotPulse, Point, position
from pulseapi import create_plane_obstacle, create_box_obstacle, create_capsule_obstacle

host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)

print('Current environment\n{}'.format(robot.get_all_from_environment()))
# add some obstacles to environment so that possible collisions are calculated
box = create_box_obstacle(Point(0.1, 0.1, 0.1), position((1, 1, 1), (0, 0, 0)), 'example_box')
capsule = create_capsule_obstacle(0.1, Point(0.5, 0.5, 0.2), Point(0.5, 0.5, 0.5), 'example_capsule')
plane = create_plane_obstacle([Point(-0.5, 0.4, 0), Point(-0.5, 0, 0), Point(-0.5, 0, 0.1)], 'example_plane')
robot.add_to_environment(box)
robot.add_to_environment(capsule)
robot.add_to_environment(plane)
print('New environment\n{}'.format(robot.get_all_from_environment()))
print('Get example box\n{}'.format(robot.get_from_environment_by_name(box.name)))
# remove some obstacles
robot.remove_from_environment_by_name(box.name)
print('Environment without box\n{}'.format(robot.get_all_from_environment()))
# remove all obstacles from environment
robot.remove_all_from_environment()
print('Empty environment\n{}'.format(robot.get_all_from_environment()))

```

[Back to table of contents](#getting-started)

#### Exception handling
Possible errors could be found [here](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).
This client wraps errors from robot into `PulseApiException`.

Provided methods:
* `recover` - the function recovers the arm after an emergency, setting its motion status to IDLE. 
Recovery is possible only after an emergency that is not fatal — corresponding 
to the ERROR status.

For example, we can trigger api exception by sending `pose` into `set_position`
method.

```python
from pulseapi import RobotPulse, PulseApiException, pose, MotionStatus

host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)

try:
    robot.set_position(pose([0, -90, 90, -90, -90, 0]), 10)
    robot.await_motion()
except PulseApiException as e:
    print('Exception {}while calling robot at {} '.format(e, robot.host))
    if robot.status_motion() == MotionStatus.ERROR:
        robot.recover()
        print('Robot recovered from error')

```
[Back to table of contents](#getting-started)

#### Versions api
You may need to get information about software and hardware versions. For example,
you want to contact developers because you noticed some strange behaviour. 

Provided methods:
* `hardware` - return hardware version for all motors, usb-can, safety, wrist.
* `software` - return software version for all motors, usb-can, safety, wrist.
* `robot_software` - return robot software version.

Example below will give you additional information about versions of robot components that 
you can send to developers:

```python
from pulseapi import Versions

host = '127.0.0.1:8080'  # replace with valid robot address
versions = Versions(host)

print(versions.hardware())
print(versions.software())
print(versions.robot_software())

```
[Back to table of contents](#getting-started)

### Documentation and further information
Could be found and downloaded 
[here](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).