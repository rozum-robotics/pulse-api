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
#### API initialization
```python
from pulseapi import RobotPulse
# create an instance of the API wrapper class
host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)
```

#### Motion control
Possible motion targets:
* Positions (`set_position` and `run_positions` methods) - control robot's tcp 
(tool center point). Use `position` method to create motion target.
* Poses (`set_pose` and `run_poses` methods) - control motor angles directly.
Use `pose` method to create motion target.

Possible motion types:
* Joint (`MT_JOINT`, default)
* Linear (`MT_LINEAR`)

**WARNING!** This is an example, you must replace motion targets according to 
your specific case. Before launching this example make sure that manipulator 
would not cause any damage to your facilities.

```python
import math
from pulseapi import position, pose, RobotPulse, MT_LINEAR

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

robot.set_pose(pose_target, SPEED)
robot.await_motion()  # wait for motion to be finished

robot.set_position(position_target, SPEED)
robot.await_motion()

# robot should go through multiple position waypoints (trajectory)
robot.run_positions(position_targets, SPEED)
robot.await_motion()

# change the motion type in order to provide linear motions
robot.run_positions(position_targets, SPEED, motion_type=MT_LINEAR)
robot.await_motion()

# limit tcp velocity to be not greater than 1 cm/s
robot.run_positions(position_targets, SPEED, 
    motion_type=MT_LINEAR, tcp_max_velocity=0.01)
robot.await_motion()
```

#### External devices control
```python

# add some obstacles to environment so that possible collisions are calculated
robot.add_to_environment(create_box_obstacle(Point(0.1, 0.1, 0.1), position((1, 1, 1), (0, 0, 0)), 
                                             'example_box'))
robot.add_to_environment(create_capsule_obstacle(0.1, Point(0.5, 0.5, 0.2), Point(0.5, 0.5, 0.5), 
                                                 'example_capsule'))
robot.add_to_environment(create_plane_obstacle([Point(-0.5, 0.2, 0), Point(-0.5, 0, 0), Point(-0.5, 0, 0.1)], 
                                               'example_plane'))
# change robot tool, set tcp offset and set tool shape
robot.change_tool(tool(
    tcp_position=position([0, 0, 0.1], [0, 0, 0]), 
    shape=[create_capsule_obstacle(0.02, Point(0, 0, 0), Point(0, 0, 0.1), 'tool_part_0')], 
    name='example_tool'))
# execute desired actions
robot.set_pose(pose, SPEED)
robot.await_motion()
robot.set_position(position, SPEED, MT_LINEAR)
robot.await_motion()
# get some information
status_motors = robot.status_motors()
pprint(status_motors)


```

### Documentation
Could be found and downloaded 
[here](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).