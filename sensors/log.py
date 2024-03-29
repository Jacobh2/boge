import logging
import logging.handlers
from settings import Settings
import sys
import uvicorn


def setup_logging(settings: Settings):
    log_format = logging.Formatter(settings.LOG_FORMAT)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(log_format)
    stdout_handler.setLevel(settings.LOG_LEVEL)

    # Log rotation handler - keep the last 10 MB of logs in boge.log
    log_file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE_NAME,
        maxBytes=settings.LOG_MAX_FILE_SIZE_MB * 1024 * 1024,
        backupCount=0,
    )
    log_file_handler.setLevel(settings.LOG_LEVEL)
    log_file_handler.setFormatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(log_file_handler)

    # Setup exception handler
    def log_uncaught_exceptions(exctype, value, tb):
        root_logger.critical("Uncaught exception", exc_info=(exctype, value, tb))

    # Set the custom exception hook as the default one
    sys.excepthook = log_uncaught_exceptions


def setup_uvicorn_logging():
    root_logger = logging.getLogger()

    uvicorn_server_logger = logging.getLogger("uvicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    # Update the Uvicorn loggers to use the root logger's handlers
    uvicorn_server_logger.handlers = root_logger.handlers
    uvicorn_access_logger.handlers = root_logger.handlers
