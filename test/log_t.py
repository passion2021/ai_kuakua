# test_logger.py
from logger_config import logger

def test_logger():
    logger.debug("This is a DEBUG message.")
    logger.info("This is an INFO message.")
    logger.warning("This is a WARNING message.")
    logger.error("This is an ERROR message.")
    logger.critical("This is a CRITICAL message.")

if __name__ == "__main__":
    test_logger()
