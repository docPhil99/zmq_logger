# client.py
import zmq
from loguru import logger
import time
import pickle
import os


class _LogSocketHandler:
    def __init__(self, host="tcp://127.0.0.1", port=9999, machine_name=None):
        """
            Handler to send pickled log messages over the network. Beware the dangers of pickle on
            an untrusted network. Note this doesn't check the server is running, if it's down the message are lost.
        :param host: The host of the address of the server. Must be in the form tcp://[address]
        :param port: The port of the log server
        :param machine_name: A tag used to identify the source, defaults to the machine name. This data it appended to
        the extra dict in loguru's message.
        """
        self.socket = zmq.Context().socket(zmq.PUB)
        self.socket.connect(f"{host}:{port}")
        if not machine_name:
            machine_name = os.uname()[1]
        self.machine_name = machine_name

    def write(self, message):
        record = message.record
        record['extra'].update({'host': self.machine_name})
        data = pickle.dumps(record)
        self.socket.send(data)


def setup(host="tcp://127.0.0.1", port=9999, machine_name=None):
    logger.configure(handlers=[{"sink": _LogSocketHandler(host=host, port=port, machine_name=machine_name)}])


if __name__ == "__main__":
    # simple text code
    for p in range(20):
        logger.info(f"Logging from client {p}")
        time.sleep(1)