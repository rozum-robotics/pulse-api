# Changelog

## 1.8.2-1.8.4
* `pulseapi.robot` module
  * Added `RobotPulse.run_linear_positions()` and `RobotPulse.run_linear_poses()` methods
* `pulseapi` module
  * Added `LinearMotionParameters` class and `InterpolationType` enum to be used with the new `run` methods
* README: updated examples

## 1.8.1
* `pulseapi.robot` module
  * Added `RobotPulse.status_failure()` method (it was not added in 1.8.0)

## 1.8.0
* Added `experimental` module
  * Added `session` module
  * Added `robot` module that is using sessions
* `pulseapi.robot` module
  * Added `RobotPulse.zg_on()` and `RobotPulse.zg_off()` methods that control freedrive mode
  * Added `RobotPulse.stop()`, `RobotPulse.bind_stop()` and `RobotPulse.unbind_stop()`


## 1.7.1
* `pulseapi.robot` module
  * Added `RobotPulse.status_failure()` method


## 1.7.0:
* Added `pulseapi.actions` module
* `pulseapi.utils` module:
  * Added optional `actions` parameter to `pose()` and `position()` functions
  * Docstrings refactoring


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
