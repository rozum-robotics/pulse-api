# Pulse Robot REST API Python

This folder contains `Python` wrapper for the [pulse robot](https://rozum.com/robotic-arm/) REST api. 
Tested on Python 3. Compatibility with Python 2 is not guarantied but underlying api (called `pdhttp`) is generated using 
[swagger-codegen](https://github.com/swagger-api/swagger-codegen) so it may work for you.

## Requirements
Python 3.4+

### Installation

Using pip: 
`pip install pulse-api --trusted-host pip.rozum.com -i http://pip.rozum.com/simple` 
to get the latest version. 

To install specific version: 
`pip install pulse-api==v1.v2.v3 --trusted-host pip.rozum.com -i http://pip.rozum.com/simple`
where **v1**, **v2**, and **v3** (e.g. pulse-api==1.4.3) are version numbers as listed below in compatibility table.

### Software compatibility table
Pulse desk version  | Python api version
------------------- |-------------------
1.4.3               | 1.4.3

### Getting started
Example uses the latest version of library. 
You may need to change something in order to make it work in previous versions.

Examples:
* [API initialization](#API initialization)
* [Motion control](#Motion control)
* [Devices and signals](#Devices and signals control)
* ["Tool" api](#Tool api)
* ["Base" api](#Base api)
* [Environment api](#Environment api)
* [Exceptions handling](#Exceptions handling)

[Documentation and further information](#Documentation and further information)

#### API initialization
```python
from pulseapi import RobotPulse
# create an instance of the API wrapper class
host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)
```

#### Motion control
Possible motion targets:
* Positions (`set_position`, `run_positions` and `get_position` methods) - control robot tcp 
(tool center point). Use `position` helper method to create motion target.
* Poses (`set_pose` and `run_poses` methods) - control motor angles directly.
Use `pose` helper method to create motion target.

Possible motion types:
* Joint (`MT_JOINT`, default)
* Linear (`MT_LINEAR`)

Auxiliary methods:
* `await_motion` - waits until robot finishes movements. **Will be soon replaced.**
* `status_motion` - the function returns the actual state of the robotic arm - 
whether it is running (in motion), idle (not in motion), in the zero gravity mode, 
or in error state.
* `freeze` - the function sets the arm in the "freeze" state. 
The arm stops moving, retaining its last position.  
**Note:**  in the state, it is not advisable to move the arm by hand as this 
can cause damage to its components.
* `relax` -  the function sets the arm in the \"relaxed\" state. The arm stops 
moving without retaining its last position. In this state, the user can move the 
robotic arm by hand (e.g., to verify/test a motion trajectory).
* `pack` - asking the arm to reach a compact pose for transportation

**WARNING!** This is an example, you must replace motion targets according to 
your specific case. Before launching this example make sure that manipulator 
would not cause any damage to your facilities.

```python
import math
import time
from pulseapi import position, pose, RobotPulse, MT_LINEAR, MotionStatus

robot = RobotPulse()
# create motion targets
pose_target = pose([0, -90, 90, -90, -90, 0])
position_target = position([-0.42, -0.12, 0.35], [math.pi, 0, 0])
position_targets = [
    position([-0.37, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.12, 0.35], [math.pi, 0, 0]),
    position([-0.42, -0.17, 0.35], [math.pi, 0, 0]),
    position([-0.37, -0.17, 0.35], [math.pi, 0, 0]),
]
SPEED = 30  # choose desired speed

# motion status usage example
def my_await_motion(robot_instance, asking_interval=0.1):
    status = robot_instance.status_motion()
    while status != MotionStatus.IDLE:
        time.sleep(asking_interval)
        status = robot_instance.status_motion()

robot.set_pose(pose_target, SPEED)
robot.await_motion()  # wait for motion to be finished
print('Current pose:\n{}'.format(robot.get_pose()))

robot.set_position(position_target, SPEED)
robot.await_motion(0.5) # checks that motion finished every 0.5 s
print('Current position:\n{}'.format(robot.get_position()))

# robot should go through multiple position waypoints (trajectory)
robot.run_positions(position_targets, SPEED)
my_await_motion(robot)

# change the motion type in order to provide linear motions
robot.run_positions(position_targets, SPEED, motion_type=MT_LINEAR)
robot.await_motion()

# limit tcp velocity to be not greater than 1 cm/s
robot.run_positions(position_targets, SPEED, 
    motion_type=MT_LINEAR, tcp_max_velocity=0.01)
robot.await_motion()

# stop the arm in last position
robot.freeze()
```

#### Devices and signals control
Methods:
* `close_gripper`, `open_gripper` with provided timeout (default: 500 ms). 
Supported grippers: Schunk and OnRobot.
* `set_digital_output_high` `set_digital_output_low`, `get_digital_output` with provided port
* `get_digital_input` with provided port

Signals:
* SIG_LOW - port is inactive
* SIG_HIGH - port is active

```python
from pulseapi import RobotPulse, SIG_LOW, SIG_HIGH

robot = RobotPulse()

# ask robot to close gripper and continue commands execution after 500 ms
robot.close_gripper() 

# ask robot to open gripper and immediately continue commands execution
robot.open_gripper(0)

# set the first output port to active state
robot.set_digital_output_high(1)

# execute some operations when input port 3 is active
if robot.get_digital_input(3) == SIG_HIGH:
    print('Input port 3 is active')
# execute some operations when input port 1 is inactive
if robot.get_digital_input(1) == SIG_LOW:
    print('Input port 1 is inactive')
```

#### Tool api
Sometimes it is convenient to calculate trajectory according to used tool and 
take it into account while calculating collisions.

Provided methods:
* `change_tool_info` - info to be used in trajectory calculation
* `change_tool_shape` - pass info to be used collision validation
* `get_tool_info`, `get_tool_shape` - receive information about current settings

Helper functions:
* `tool_info` - creates instance of tool info to be passed into 
`change_tool_info` method.
* `tool_shape` - creates tool shape to be passed into `change_tool_shape`

```python
from pulseapi import RobotPulse, position, Point
from pulseapi import create_simple_capsule_obstacle, tool_shape, tool_info

robot = RobotPulse()

# recieve info about current tool
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

#### Base api
Sometimes it is convenient to calculate trajectory relatively to some specific 
point in space.

Provided methods: 
* `change_base`
* `get_base`

```python
from pulseapi import RobotPulse, position
robot = RobotPulse()

current_base = robot.get_base()
print('Current base\n{}'.format(current_base))

# move the new base point along x and y axes
new_base = position([0.05, 0.05, 0], [0, 0, 0])
robot.change_base(new_base)

print('New base\n{}'.format(robot.get_base()))

```

#### Environment api
Add virtual obstacles to take into account while calculating trajectories and 
checking for collisions

#### Exceptions handling

### Documentation and further information
Could be found and downloaded 
[here](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).