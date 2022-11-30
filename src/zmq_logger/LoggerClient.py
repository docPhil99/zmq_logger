# client.py
import hashlib

import securepickle
import zmq
from loguru import logger
#import pickle
import os
from .LoggerServer import ZMQLogger
import sys
import securepickle as pickle


class LogSocketHandler:
    def __init__(self, host="tcp://127.0.0.1", port=9999, machine_name=None,hash_key=None):
        """
            Handler to send pickled log messages over the network. Beware the dangers of pickle on
            an untrusted network. Note this doesn't check the server is running, if it's down the message are lost.
        :param host: The host of the address of the server. Must be in the form tcp://[address]
        :param port: The port of the log server
        :param machine_name: A tag used to identify the source, defaults to the machine name. This data it appended to
        the extra dict in loguru's message. If none is supplied os.uname()[1] is used.
        """
        self._hash = hash_key
        self.socket = zmq.Context().socket(zmq.PUB)
        addr = f"{host}:{port}"
        print(f'Connected to {addr}')
        self.socket.connect(addr)
        if not machine_name:
            machine_name = os.uname()[1]
        self.machine_name = machine_name

    def write(self, message):
        record = message.record
        record['extra'].update({'host': self.machine_name})
        try:
            data = pickle.dumps(record)
        except:
            logger.exception("Data pickle error")
            raise
        try:
            self.socket.send(data)
        except:
            logger.exception("Logging send error")
            raise


def setup(host="tcp://127.0.0.1", port=9999, machine_name=None, hash=b"change me to something else"):
    """
    Configures two loguru handlers. One writes to the host server, the other to stderr. This is a very basic setup,
    so you might want to write your own.
    :param host: server host
    :param port: server port
    :param machine_name: Appends the local machines name to loguru's extra dictionary.
    :return:
    """
    securepickle.set_key(hash)
    logger.configure(handlers=[{"sink": LogSocketHandler(host=host, port=port, machine_name=machine_name),
                                "enqueue": True},
                               {"sink": sys.stderr, "format": ZMQLogger.formatter, "enqueue": True}])

