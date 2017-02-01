import logging
import os
import logging.handlers

def setup_logger():
    # Set up a specific logger with our desired output level
    import user.settings
    logging_directory = os.path.join(user.settings.OSSPEAK_DIRECTORY, 'logs')
    if not os.path.isdir(logging_directory):
        os.mkdir(logging_directory)
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
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(ch) 
    return logger

logger = setup_logger()