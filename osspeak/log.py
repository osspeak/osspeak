import clargs
import logging
import os
import logging.handlers

def setup_logger():
    # Set up a specific logger with our desired output level
    import settings
    logging_directory = os.path.join(settings.OSSPEAK_DIRECTORY, 'logs')
    if not os.path.isdir(logging_directory):
        os.makedirs(logging_directory)
    logger = logging.getLogger('root')
    logger.setLevel(logging.DEBUG)
    # Add the log message handler to the logger
    log_filename = os.path.join(logging_directory, 'log')
    handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=65536,
        backupCount=5,
    )
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    print_debug_level = logging.INFO
    ch.setLevel(print_debug_level)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch)
    return logger

logger = setup_logger()