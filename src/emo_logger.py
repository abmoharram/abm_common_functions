from __future__ import annotations
import os
from sys import stdout
from time import strftime, time

import logging
from logging import (getLogger, Formatter, StreamHandler,
                     DEBUG, Filter, INFO, CRITICAL,
                     ERROR, WARNING)
from typing import Mapping


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

    emo_DONE = '✅'
    emo_ERROR = '❌'
    emo_CRITICAL = '🚨'
    emo_WARNING = '⚠️'
    emo_INFO = '💁'
    emo_DEBUG = '🐞'
    emo_START = '🚀'
    emo_END = '🎉'
    emo_UNKNOWN = '❓'
    emo_TRACE = '🔍'

    def filter(self, record):
        if record.levelname == 'DEBUG':
            record.levelemoji = self.emo_DEBUG
        elif record.levelname == 'INFO':
            record.levelemoji = self.emo_INFO
        elif record.levelname == 'WARNING':
            record.levelemoji = self.emo_WARNING
        elif record.levelname == 'ERROR':
            record.levelemoji = self.emo_ERROR
        elif record.levelname == 'CRITICAL':
            record.levelemoji = self.emo_CRITICAL
        elif record.levelname == 'DONE':
            record.levelemoji = self.emo_DONE
        elif record.levelname == 'START':
            record.levelemoji = self.emo_START
        elif record.levelname == 'END':
            record.levelemoji = self.emo_END
        elif record.levelname == 'TRACE':
            record.levelemoji = self.emo_TRACE
        else:
            record.levelemoji = self.emo_UNKNOWN

        if len(record.filename) > 25:
            record.filename = '..' + record.filename[-23:]
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

    def __init__(self,
                 log_dir: str,
                 log_name: str,
                 log_level: int = DEBUG) -> None:
        self.log_dir = log_dir

        if (log_name is None) or (log_name == ''):
            self.log_name = 'no_app_name'
        else:
            self.log_name = log_name

        self.log_name = log_name
        self.logger = getLogger(log_name)
        self.logger.setLevel(log_level)
        self.formatter = Formatter(
            '%(levelemoji)s %(levelname)8s | '
            '%(asctime)s | %(name)s | '
            '%(filename)25s:%(lineno)5d | %(funcName)s() '
            '- %(message)s')

        self.logger.addFilter(EmoFilter())
        self.stream_handler = StreamHandler(stdout)
        self.stream_handler.setFormatter(self.formatter)
        if not self.logger.hasHandlers():
            self.logger.addHandler(self.stream_handler)

        logging.addLevelName(self.START_INT, 'START')
        logging.addLevelName(self.END_INT, 'END')
        logging.addLevelName(self.DONE_INT, 'DONE')
        logging.addLevelName(self.UNKNOWN_INT, 'UNKNOWN')
        logging.addLevelName(self.TRACE_INT, 'TRACE')
        self.logger.trace = self.trace
        self.logger.done = self.done
        self.logger.start = self.start
        self.logger.end = self.end
        self.logger.unknown = self.unknown
        self.logger.debug = self.debug
        self.logger.info = self.info
        self.logger.warning = self.warning
        self.logger.error = self.error
        self.logger.critical = self.critical

        self.last_message = None
        self.last_message_time = None
        self.stack_distance = 2
    
    def set_stack_distance(self, stack_distance: int) -> None:
        """Set the stack distance for the logger."""
        self.stack_distance = stack_distance

    def trace(self, message, *args, **kws):
        """Log 'message' with severity 'TRACE'."""
        if self.is_enabled_for(self.TRACE_INT):
            self._log(self.TRACE_INT, message, args, **kws)

    def done(self, message, *args, **kws):
        """Log 'message' with severity 'DONE'."""
        if self.is_enabled_for(self.DONE_INT):
            self._log(self.DONE_INT, message, args, **kws)

    def start(self, message, *args, **kws):
        """Log 'message' with severity 'START'."""
        if self.is_enabled_for(self.START_INT):
            self._log(self.START_INT, message, args, **kws)

    def end(self, message, *args, **kws):
        """Log 'message' with severity 'END'."""
        if self.is_enabled_for(self.END_INT):
            self._log(self.END_INT, message, args, **kws)

    def unknown(self, message, *args, **kws):
        """Log 'message' with severity 'UNKNOWN'."""
        if self.is_enabled_for(self.UNKNOWN_INT):
            self._log(self.UNKNOWN_INT, message, args, **kws)

    def debug(self, message, *args, **kws):
        """Log 'message' with severity 'DEBUG'."""
        if self.is_enabled_for(self.DEBUG_INT):
            self._log(self.DEBUG_INT, message, args, **kws)

    def info(self, message, *args, **kws):
        """Log 'message' with severity 'INFO'."""
        if self.is_enabled_for(self.INFO_INT):
            self._log(self.INFO_INT, message, args, **kws)

    def warning(self, message, *args, **kws):
        """Log 'message' with severity 'WARNING'."""
        if self.is_enabled_for(self.WARNING_INT):
            self._log(self.WARNING_INT, message, args, **kws)

    def error(self, message, *args, **kws):
        """Log 'message' with severity 'ERROR'."""
        if self.is_enabled_for(self.ERROR_INT):
            self._log(self.ERROR_INT, message, args, **kws)

    def critical(self, message, *args, **kws):
        """Log 'message' with severity 'CRITICAL'."""
        if self.is_enabled_for(self.CRITICAL_INT):
            self._log(self.CRITICAL_INT, message, args, **kws)

    def is_enabled_for(self, level):
        """Check if the logger is enabled for the given level."""
        return self.logger.isEnabledFor(level)

    def write_message(self,
                      level: int,
                      msg: object,
                      args: logging._ArgsType,
                      exc_info: logging._ExcInfoType = None,
                      extra: Mapping[str, object] | None = None,
                      stack_info: bool = False,
                      stacklevel: int = 1,) -> None:
        """Write the log message to the log file."""
        date = strftime('%Y-%m-%d')
        now = strftime('%H:%M:%S')
        self.last_message_time = time()
        level_name = logging.getLevelName(int(level))
        
        if level_name in ('START', 'END', 'DONE'):
            level_filename = 'PROCESS'
        else:
            level_filename = level_name
        
        emo = getattr(EmoFilter(), f'emo_{level_name}')
        folder_name = f'{self.log_dir}/{self.log_name}/{date}'
        if os.path.exists(folder_name) is False:
            os.makedirs(folder_name)
        filename = f'{folder_name}/{level_filename}.log'

        with open(filename, 'a', encoding='UTF-8') as file:
            file.write(f'{emo} {now} | {level_name} | {msg} | {args} | '
                       f'{exc_info} | {extra} | {stack_info} | {stacklevel}\n')

    def _log(self,
             level: int,
             msg: object,
             args: logging._ArgsType,
             exc_info: logging._ExcInfoType = None,
             extra: Mapping[str, object] | None = None,
             stack_info: bool = False,
             stacklevel: int = 1,):
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
            stacklevel=stacklevel + self.stack_distance)

    def close(self):
        """close _summary_"""
        self.logger.removeHandler(self.stream_handler)
        self.stream_handler.close()
        self.logger = None
        self.formatter = None
        self.stream_handler = None