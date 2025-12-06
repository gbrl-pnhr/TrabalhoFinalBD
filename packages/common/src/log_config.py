import logging.config
import sys
from pathlib import Path


def setup_logging(app_name: str, log_dir: Path | None = None):
    handler_names = ["console"]
    handlers_config = {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "stream": sys.stdout,
        }
    }
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        handler_names.extend(["file", "json_file"])
        handlers_config["file"] = {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": log_dir / f"{app_name}.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8",
        }
        handlers_config["json_file"] = {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": log_dir / f"{app_name}.json.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8",
        }
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            },
            "colored": {
                "()": "colorlog.ColoredFormatter",
                "format": "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "log_colors": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            },
        },
        "handlers": handlers_config,
        "loggers": {
            "root": {
                "handlers": handler_names,
                "level": "INFO",
                "propagate": True,
            },
            "yoyo": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "db": {
                "handlers": handler_names,
               "level": "INFO",
               "propagate": False
           },
        },
    }

    logging.config.dictConfig(logging_config)