from database import add_log
import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format=LOG_FORMAT,
    level=logging.INFO,
    encoding='utf-8'
)

class LEVELS:
    info = 'INFO'
    error = 'ERROR'
    warning = 'WARNING'
    debug = 'DEBUG'    

class DatabaseLogger:
    def __init__(self):
        self.basic_logger = logging.getLogger()

    def info(self, content):
        add_log(content, LEVELS.info)
        self.basic_logger.info(content)

    def error(self, content):
        add_log(content, LEVELS.error)
        self.basic_logger.error(content)

    def warn(self, content):
        add_log(content, LEVELS.warning)
        self.basic_logger.warn(content)

    def debug(self, content):
        add_log(content, LEVELS.debug)
        self.basic_logger.debug(content)

logger = DatabaseLogger()