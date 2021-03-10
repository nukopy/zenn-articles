import logging
from pythonjsonlogger import jsonlogger


def getLogger():
    logger = logging.getLogger(__name__)
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)


root_logger = logging.RootLogger()
module_logger = logging.getLogger(__name__)