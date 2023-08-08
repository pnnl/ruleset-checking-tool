import os.path

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(filename)s:%(lineno)s [%(levelname)s] [%(name)s]: %(message)s"
        },
    },
    "handlers": {
        "default_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            # TODO work on the directory later
            "filename": os.path.join(os.path.dirname(__file__), "rct.log"),
            "mode": "w",
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {"handlers": ["default_handler"], "level": "DEBUG", "propagate": False}
    },
}
