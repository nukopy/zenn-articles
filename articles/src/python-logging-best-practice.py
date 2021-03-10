import logging


def getLogger():
    logger = logging.getLogger(__name__)
    logHandler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)


root_logger = logging.RootLogger()
module_logger = logging.getLogger(__name__)