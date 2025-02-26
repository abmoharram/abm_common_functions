"""Base class to monitor all child non-private method calls."""

import time
from logging import INFO
from typing import Any, Callable

from abm_common_functions.emo_logger import EmoLogger

DEFAULT_LOGGING_FOLDER = ".logs"
DEFAULT_APP_NAME = "undefined"


class BaseClass:
    """Base class to monitor all child method calls."""

    def __init__(self, log_folder: str | None = None, app_name: str | None = None):
        """Initialize the class with a logger."""
        if log_folder is None:
            self.log_folder = BaseClass.get_global_log_folder()
        else:
            self.log_folder = log_folder

        if app_name is None:
            self.app_name = BaseClass.get_global_app_name()
        else:
            self.app_name = app_name

        if not hasattr(self, "logger"):
            self.logger = EmoLogger(self.log_folder, self.app_name, log_level=INFO)
        self.logger.set_stack_distance(3)

    @staticmethod
    def set_global_log_data(log_folder: str, app_name: str):
        """Set the global log data for the class."""
        BaseClass.log_folder = log_folder
        BaseClass.app_name = app_name

    @staticmethod
    def get_global_log_folder() -> str:
        """Get the global log folder."""
        try:
            return BaseClass.log_folder
        except AttributeError:
            BaseClass.log_folder = DEFAULT_LOGGING_FOLDER
            return BaseClass.log_folder

    @staticmethod
    def get_global_app_name() -> str:
        """Get the global app name."""
        try:
            return BaseClass.app_name
        except AttributeError:
            BaseClass.app_name = DEFAULT_APP_NAME
            return BaseClass.app_name

    def __init_subclass__(cls, **kwargs: dict[str, Any]):
        """Initialize the subclass and wrap methods for monitoring."""
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("_"):
                setattr(cls, attr_name, cls._monitor_function(attr_value))  # type: ignore

    @staticmethod
    def _monitor_function(func: Callable[..., dict[str, Any]]) -> Callable[..., dict[str, Any]]:
        """Private method to monitor function execution time."""

        def wrapper(*args: ..., **kwargs: dict[str, Any]) -> Any:
            start_time = time.time()
            logger = args[0].logger if hasattr(args[0], "logger") else None
            if logger:
                logger.start(f"Starting '{func.__name__}'")

            result: dict[str, Any] = func(*args, **kwargs)

            end_time = time.time()
            if logger:
                logger.end(f"Ending '{func.__name__}'")
                logger.done(f"Execution time for '{func.__name__}': {end_time - start_time:.4f} seconds")

            return result

        return wrapper
