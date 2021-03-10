import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def divide(a: float, b: float) -> float:
    try:
        result = a / b
    except ZeroDivisionError:
        logger.error("Error: 0 is an invalid number")
        raise
    except Exception:
        logger.error("Error: another error occurred")
        raise ValueError
    else:
        return result
    finally:
        logger.info("Cleanup can go here")


# success
print(divide(1, 1))

# ZeroDivisionError
print(divide(1, 0))

# Exception
print(divide("1", 1))