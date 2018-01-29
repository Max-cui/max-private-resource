# encoding=utf-8
import logging
import sys


RESOURCE_PATH = '/data_server/data/CAAS/'

DB_PATH = '/data_server/data/uias.db'


LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s (%(process)d/%(threadName)s) %(name)s %(levelname)s - %(message)s'

def setup_logging(level=None):
    level = level or LOG_LEVEL
    file_handler = logging.FileHandler("/var/log/data_server.log")
    console_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)
    # Disable requests logging
    logging.getLogger("requests").propagate = False
