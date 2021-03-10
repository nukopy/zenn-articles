from log import getLogger


logger = getLogger(__name__)
logger.info("Inserting rows into MySQL", extra={"extra-log-message": "hoge hoge"})
