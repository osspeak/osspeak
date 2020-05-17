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
    logger.setLevel(settings.settings['file_logging_level'])
    # Add the log message handler to the logger
    log_filename = os.path.join(logging_directory, 'log.txt')
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=65536,
        backupCount=5,
    )
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    ch = logging.StreamHandler()
    ch.setLevel(settings.settings['print_logging_level'])
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = setup_logger()