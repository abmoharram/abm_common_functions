"""Base class to monitor all child non-private method calls."""

import time
from emo_logger import EmoLogger

class BaseClass:
    """Base class to monitor all child method calls."""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'logger'):
            cls.logger = EmoLogger(cls.__name__, '')
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, cls._monitor_function(attr_value))

    @staticmethod
    def _monitor_function(func):
        """Private method to monitor function execution time."""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger = args[0].logger if hasattr(args[0], 'logger') else None
            if logger:
                logger.start(f"Starting '{func.__name__}'")

            result = func(*args, **kwargs)

            end_time = time.time()
            if logger:
                logger.end(f"Ending '{func.__name__}'")
                logger.done(f"Execution time for '{func.__name__}': "
                            f"{end_time - start_time:.4f} seconds")

            return result
        return wrapper
