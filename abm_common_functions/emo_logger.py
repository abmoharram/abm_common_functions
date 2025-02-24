from __future__ import annotations

import logging
import os
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Filter,
    Formatter,
    StreamHandler,
    _ArgsType,  # type: ignore
    _ExcInfoType,  # type: ignore
    getLogger,
)
from sys import stdout
from time import strftime, time
from typing import Any, Literal, Mapping


class EmoFilter(Filter):
    """ABM custom logger filter class.

    This class is used to create a custom filter for the ABM-MLPL project.
    The filter will add an emoji to the log message based on the log level.

    Attributes:
        emo_DONE (str): The emoji for the DONE log level.
        emo_ERROR (str): The emoji for the ERROR log level.
        emo_CRITICAL (str): The emoji for the CRITICAL log level.
        emo_WARNING (str): The emoji for the WARNING log level.
        emo_INFO (str): The emoji for the INFO log level.
        emo_DEBUG (str): The emoji for the DEBUG log level.
        emo_START (str): The emoji for the START log level.
        emo_END (str): The emoji for the END log level.
        emo_UNKNOWN (str): The emoji for the UNKNOWN log level.
        emo_TRACE (str): The emoji for the TRACE log level.

    Methods:
        filter: Filter the log message.
    """

    emo_DONE = "✅"
    emo_ERROR = "❌"
    emo_CRITICAL = "🚨"
    emo_WARNING = "⚠️"
    emo_INFO = "💁"
    emo_DEBUG = "🐞"
    emo_START = "🚀"
    emo_END = "🎉"
    emo_UNKNOWN = "❓"
    emo_TRACE = "🔍"

    def filter(self, record: object) -> bool:
        """Filter the log message."""
        record.levelemoji = None

        if record.levelname == "DEBUG":
            record.levelemoji = self.emo_DEBUG
        elif record.levelname == "INFO":
            record.levelemoji = self.emo_INFO
        elif record.levelname == "WARNING":
            record.levelemoji = self.emo_WARNING
        elif record.levelname == "ERROR":
            record.levelemoji = self.emo_ERROR
        elif record.levelname == "CRITICAL":
            record.levelemoji = self.emo_CRITICAL
        elif record.levelname == "DONE":
            record.levelemoji = self.emo_DONE
        elif record.levelname == "START":
            record.levelemoji = self.emo_START
        elif record.levelname == "END":
            record.levelemoji = self.emo_END
        elif record.levelname == "TRACE":
            record.levelemoji = self.emo_TRACE
        else:
            record.levelemoji = self.emo_UNKNOWN

        if len(record.filename) > 25:
            record.filename = ".." + record.filename[-23:]
        return True


class EmoLogger:
    """ABM customer logger class.

    This class is used to create a custom logger for the ABM-MLPL project.
    The logger will add a custom log level to the logger.

    Attributes:
        DONE_INT (int): The integer value for the DONE log level.
        ERROR_INT (int): The integer value for the ERROR log level.
        CRITICAL_INT (int): The integer value for the CRITICAL log level.
        WARNING_INT (int): The integer value for the WARNING log level.
        INFO_INT (int): The integer value for the INFO log level.
        DEBUG_INT (int): The integer value for the DEBUG log level.
        START_INT (int): The integer value for the START log level.
        END_INT (int): The integer value for the END log level.
        UNKNOWN_INT (int): The integer value for the UNKNOWN log level.
        TRACE_INT (int): The integer value for the TRACE log level.

    Methods:
        __init__: Initialize the logger.
        trace: Log a message with the TRACE log level.
        done: Log a message with the DONE log level.
        start: Log a message with the START log level.
        end: Log a message with the END log level.
        unknown: Log a message with the UNKNOWN log level.
        debug: Log a message with the DEBUG log level.
        info: Log a message with the INFO log level.
        warning: Log a message with the WARNING log level.
        error: Log a message with the ERROR log level.
        critical: Log a message with the CRITICAL log level.
        is_enabled_for: Check if the logger is enabled for the given level.
        write_message: Write the log message to the log file.
        _log: Log a message with the given log level.
        close: Close the logger."""

    DONE_INT = INFO + 3
    ERROR_INT = ERROR
    CRITICAL_INT = CRITICAL
    WARNING_INT = WARNING
    INFO_INT = INFO
    DEBUG_INT = DEBUG
    START_INT = INFO + 1
    END_INT = INFO + 2
    UNKNOWN_INT = INFO + 5
    TRACE_INT = DEBUG + 1

    def __init__(self, log_folder: str, app_name: str | None, log_level: int = DEBUG) -> None:
        self.log_folder = log_folder

        if (app_name is None) or (app_name == ""):
            self.app_name = "no_app_name"
        else:
            self.app_name = app_name

        self.app_name = app_name
        self.logger = getLogger(app_name)
        self.logger.setLevel(log_level)
        self.formatter = Formatter(
            "%(levelemoji)s %(levelname)8s | "
            "%(asctime)s | %(name)s | "
            "%(filename)25s:%(lineno)5d | %(funcName)s() "
            "- %(message)s"
        )

        self.logger.addFilter(EmoFilter())
        self.stream_handler = StreamHandler(stdout)
        self.stream_handler.setFormatter(self.formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(self.stream_handler)

        logging.addLevelName(self.START_INT, "START")
        logging.addLevelName(self.END_INT, "END")
        logging.addLevelName(self.DONE_INT, "DONE")
        logging.addLevelName(self.UNKNOWN_INT, "UNKNOWN")
        logging.addLevelName(self.TRACE_INT, "TRACE")
        self.logger.trace = self.trace  # type: ignore
        self.logger.done = self.done  # type: ignore
        self.logger.start = self.start  # type: ignore
        self.logger.end = self.end  # type: ignore
        self.logger.unknown = self.unknown  # type: ignore
        self.logger.debug = self.debug  # type: ignore
        self.logger.info = self.info  # type: ignore
        self.logger.warning = self.warning  # type: ignore
        self.logger.error = self.error  # type: ignore
        self.logger.critical = self.critical  # type: ignore

        self.last_message = None
        self.last_message_time = None
        self.stack_distance = 2

    def set_stack_distance(self, stack_distance: int) -> None:
        """Set the stack distance for the logger."""
        self.stack_distance = stack_distance

    def trace(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'TRACE'."""
        if self.is_enabled_for(self.TRACE_INT):
            self._log(self.TRACE_INT, message, args)

    def done(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'DONE'."""
        if self.is_enabled_for(self.DONE_INT):
            self._log(self.DONE_INT, message, args)

    def start(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'START'."""
        if self.is_enabled_for(self.START_INT):
            self._log(self.START_INT, message, args)

    def end(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'END'."""
        if self.is_enabled_for(self.END_INT):
            self._log(self.END_INT, message, args)

    def unknown(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'UNKNOWN'."""
        if self.is_enabled_for(self.UNKNOWN_INT):
            self._log(self.UNKNOWN_INT, message, args)

    def debug(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'DEBUG'."""
        if self.is_enabled_for(self.DEBUG_INT):
            self._log(self.DEBUG_INT, message, args)

    def info(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'INFO'."""
        if self.is_enabled_for(self.INFO_INT):
            self._log(self.INFO_INT, message, args)

    def warning(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'WARNING'."""
        if self.is_enabled_for(self.WARNING_INT):
            self._log(self.WARNING_INT, message, args)

    def error(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'ERROR'."""
        if self.is_enabled_for(self.ERROR_INT):
            self._log(self.ERROR_INT, message, args)

    def critical(self, message: str, *args: _ArgsType) -> None:
        """Log 'message' with severity 'CRITICAL'."""
        if self.is_enabled_for(self.CRITICAL_INT):
            self._log(self.CRITICAL_INT, message, args)

    def is_enabled_for(self, level: int):
        """Check if the logger is enabled for the given level."""
        if self.logger is None:
            return False
        return self.logger.isEnabledFor(level)

    def write_message(
        self,
        level: int,
        msg: object,
        args: _ArgsType,
        exc_info: _ExcInfoType = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ) -> None:
        """Write the log message to the log file."""
        date = strftime("%Y-%m-%d")
        now = strftime("%H:%M:%S")
        self.last_message_time = time()
        level_name = logging.getLevelName(int(level))

        if level_name in ("START", "END", "DONE"):
            level_filename = "PROCESS"
        else:
            level_filename = level_name

        emo = getattr(EmoFilter(), f"emo_{level_name}")
        folder_name = f"{self.log_folder}/{self.app_name}/{date}"
        if os.path.exists(folder_name) is False:
            os.makedirs(folder_name)
        filename = f"{folder_name}/{level_filename}.log"

        with open(filename, "a", encoding="UTF-8") as file:
            file.write(
                f"{emo} {now} | {level_name} | {msg} | {args} | {exc_info} | {extra} | {stack_info} | {stacklevel}\n"
            )

    def _log(
        self,
        level: int,
        msg: object,
        args: _ArgsType,
        exc_info: _ExcInfoType = None,
        extra: Mapping[str, object] | None = None,
        stack_info: bool = False,
        stacklevel: int = 1,
    ):
        """Log 'message' with severity 'TRACE'."""
        self.last_message = msg

        if self.logger is None:
            return
        else:
            self.write_message(level, msg, args, exc_info, extra, stack_info, stacklevel)

        self.logger.log(
            level=level,
            msg=msg,
            *args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel + self.stack_distance,
        )

    def close(self):
        """close _summary_"""
        if self.logger is None:
            return

        if self.stream_handler is None:
            return

        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
        self.logger = None
        self.formatter = None
        self.stream_handler = None
