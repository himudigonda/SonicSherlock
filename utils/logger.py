import logging
import sys

from config import DEBUG, config


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(
            logging.DEBUG if DEBUG else logging.INFO
        )  # Set default level based on DEBUG

        # Create handlers
        stream_handler = logging.StreamHandler(
            sys.stdout
        )  # Use stdout for cleaner output
        stream_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(config.LOG_FILE)
        file_handler.setLevel(logging.DEBUG if DEBUG else logging.INFO)

        # Create formatter and add it to handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = Logger(__name__)
