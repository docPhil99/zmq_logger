from zmq_logger.LoggerServer import ZMQLogger
import sys
from loguru import logger
import time

if __name__ == "__main__":
    """
    Simple test example, start the server for 600 seconds
    """
    logger.info('Starting')
    # change the hash to some private binary string
    zmlog = ZMQLogger(hash=b"change me to something else")
    # configure loguru to use our formatter. You need to do this, but this adds the client
    # hostname to the message.
    logger.configure(handlers=[{"sink": sys.stderr, "format": ZMQLogger.formatter}])
    # start the logger thread
    zmlog.start()
    time.sleep(600) # for the demo, just sleep this thread for 600 seconds before closing
    logger.info('Stopping')
    # stop the logger thread.
    zmlog.stop()