from settings import LOGS_PATH
from loguru import logger
import sys


def setup_logger():
    logger.remove()

    # 添加终端日志处理器
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {file}:{line} in {function}"
    )

    # 添加文件日志处理器
    logger.add(
        LOGS_PATH / "app.log",
        level="INFO",
        rotation="1 week",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message} | {file}:{line} in {function}"
    )


setup_logger()
logger = logger
