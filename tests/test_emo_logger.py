"""Testing the EmoLogger class."""
from emo_logger import EmoLogger


def test_emo_logger_init():
    logger = EmoLogger('../tests/logger_dir', 'test')
    assert logger is not None
    assert logger.last_message is None
    assert logger.last_message_time is None

def test_emo_logger_trace():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.trace('testing the trace function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_debug():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.debug('testing the debug function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_info():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.info('testing the info function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_warning():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.warning('testing the warning function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_error():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.error('testing the error function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_critical():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.critical('testing the critical function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_done():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.done('testing the done function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_start():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.start('testing the start function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None

def test_emo_logger_end():
    logger = EmoLogger('../tests/logger_dir', 'test')
    logger.end('testing the end function')
    assert logger is not None
    assert logger.last_message is not None
    assert logger.last_message_time is not None
