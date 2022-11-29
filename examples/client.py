from zmq_logger.LoggerClient import setup
from loguru import logger
import time

if __name__ == "__main__":
    setup()
    # simple text code
    for p in range(20):
        logger.info(f"Logging from client {p}")
        time.sleep(1)