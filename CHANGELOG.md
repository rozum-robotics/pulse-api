# Changelog

## 1.5.1

* Added `pulseapi.logging` module:
  * Under the hood it uses `logging.config.dictConfig()` function from the python standard library.
    * [Example config](https://docs.python.org/3/howto/logging-cookbook.html#an-example-dictionary-based-configuration)
    * [Python logging documentation](https://docs.python.org/3/library/logging.html)
    * [Example of logging configuration defined in the module.](pulseapi/logging.py) (DEFAULT_LOGGING_CONFIG)
* `pulseapi.robot` module:
  * Added `log_config` parameter to `RobotPulse.__init__()` method.
  * Added logging to the function calls using `RobotPulse.logger` field.
  * Added `logger.debug()` calls to track function calls with parameters.
