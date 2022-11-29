from zmq_logger.LoggerServer import ZMQLogger
import sys
from loguru import logger

if __name__ == "__main__":
    """
    Simple test example, start server for 60 seconds
    """
    import time

    logger.info('Starting')
    zmlog = ZMQLogger()
    logger.configure(handlers=[{"sink": sys.stderr, "format": ZMQLogger.formatter}])
    zmlog.start()
    time.sleep(600)
    logger.info('Stopping')
    zmlog.stop()