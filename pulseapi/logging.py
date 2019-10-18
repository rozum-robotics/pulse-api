import logging
import logging.config


PACKAGE_LOGGER_NAME = "pulseapi"

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        },
        "func": {
            "format": "%(asctime)s %(levelname)s %(funcName)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "func"
        }
    },
    "loggers": {
        PACKAGE_LOGGER_NAME: {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    }
}

def configure(log_config):
    if log_config is None:
        logger = logging.getLogger("pulseapi")
        logger.addHandler(logging.NullHandler())
        return logger
    if "pulseapi" not in log_config["loggers"]:
        raise ValueError("pulseapi logger not found in configuration")
    logging.config.dictConfig(log_config)
    return logging.getLogger("pulseapi")
