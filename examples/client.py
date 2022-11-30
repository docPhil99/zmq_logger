from zmq_logger.LoggerClient import setup
from loguru import logger
import time

if __name__ == "__main__":

    # this is a simple helper function that set up securepickle and configures the loguru handler
    # to print to stderr and the remote server.
    setup(host="tcp://127.0.0.1", port=9999, hash=b"change me to something else")

    for p in range(20):
        # log a message and send to the server. Note,
        logger.info(f"Logging from client {p}")
        time.sleep(1)

