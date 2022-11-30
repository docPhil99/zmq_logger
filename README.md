# zmq_logger

A quick and dirty client/server logger based on loguru and zmq for
logging over a network. 

Start the server, binding to suitable port, and then you can
send messages from multiple clients over a network. The host name of the client machine is added into loguru's extra
dictionary. 

It is currently using pickle to serialise the log message. https://pypi.org/project/securepickle/ is used to (hopefully) 
prevent attackers modify the data. However, there are currently no other security considerations, so I still wouldn't use
this on an untrusted network. 

Example usage:

```
#server.py
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
```

and

```
#client.py
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
```
