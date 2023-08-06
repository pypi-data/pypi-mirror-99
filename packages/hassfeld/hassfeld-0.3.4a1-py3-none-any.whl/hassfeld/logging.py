"""Logging functions"""
import logging

#logger = logging.getLogger(__name__)


def log_debug(message):
    """Logging of debug information."""
    name = inspect.currentframe().f_back.f_code.co_name
    filename = inspect.currentframe().f_back.f_code.co_filename
    basename = os.path.basename(filename)
    logger.debug("%s->%s: %s", basename, name, message)


def log_info(message):
    """Logging of information."""
    logger.info(message)


def log_warn(message):
    """Logging of warnings."""
    logger.warning(message)


def log_error(message):
    """Logging of errors."""
    logger.error(message)


def log_critical(message):
    """Logging of information."""
    logger.critical(message)
