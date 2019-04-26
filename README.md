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

```python
from pprint import pprint
from pulseapi import *
# create an instance of the API wrapper class
host = "127.0.0.1:8080"  # replace with valid robot address 
robot = RobotPulse(host)
# create motion targets
zero_pose = pose([0, 0, 0, 0, 0, 0])
example_position = position([-0.33, -0.33, 0.43], [0, -1.1659, 0])
SPEED = 10
try:
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
except PulseApiException as e:
    print("Exception when calling PulseRobot %s\n" % e)
```

### Documentation
Could be found and downloaded 
[here](https://rozum.com/tpl/pdf/ARM/PULSE%20ROBOT_API%20REFERENCE%20GUIDE_v.6.pdf).