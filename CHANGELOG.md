# Changelog

## 1.7.0:
* added `pulseapi.actions` module
* `pulseapi.utils` module:
  * added optional `actions` parameter to `pose()` and `position()` functions
  * docstrings refactoring


## 1.6.0

* `pulseapi.robot` module:
  * Added optional `logger` parameter to `RobotPulse.__init__()` method.
  * Added logging with debug level to the function calls using 
  `RobotPulse.logger` field.
  * Added `RobotPulse.jogging()` method, to interact with jogging mode of the
  robotic arm.
  * Added `RobotPulse.status()` method.
  * Added `RobotPulse.await_stop()` method.
  * Deprecated `RobotPulse.await_motion()` method. Use `RobotPulse.await_stop()`
  as a drop-in replacement.
  * Deprecated `RobotPulse.status_motion()` method. Use `RobotPulse.status()`
  instead.
  * Maximum value for acceleration parameter in motion control methods
  is now 200%.
* `pulseapi.utils` module:
  * Added `jog()` function. Use it to create motion targets for the jogging mode
  of the robotic arm.
