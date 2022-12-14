import zmq
from loguru import logger
import threading

import securepickle as pickle
# make sure the port is open,

class ZMQLogger:
    def __init__(self, host="tcp://*", port=9999,  hash=b"change me to something else"):
        self.host = host
        self.port = port
        pickle.set_key(hash)

        self._run = False
        self._thread = None

    def start(self):
        if self._run:
            return
        self._run = True
        self._thread = threading.Thread(target=self._worker)
        self._thread.start()

    def stop(self):
        self._run = False

    def _worker(self):
        self.socket = zmq.Context().socket(zmq.SUB)
        addr = f"{self.host}:{self.port}"
        logger.debug(f'Binding Addr: {addr}')
        self.socket.bind(addr)
        self.socket.subscribe("")
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        while self._run:
            socks = dict(poller.poll(1000))
            if socks:
                if socks.get(self.socket) == zmq.POLLIN:
                    pmessage = self.socket.recv(zmq.NOBLOCK)
                    try:
                        record = pickle.loads(pmessage)
                    except pickle.InvalidSignatureError:
                        logger.warning("Invalid signature in log data")
                        continue
                    except:
                        logger.exception("Cannot recover message")
                        continue
                    level, message = record["level"].no, record["message"]
                    logger.patch(lambda record: record.update(record)).bind(host=record['extra']['host']).log(level, message)

            else:
                pass
                # message timeout


    @classmethod
    def formatter(cls,record):
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>| <lvl>{level: <8}</lvl>| {name}:{function}:{line} <blue>{extra[host]}</blue> -  <lvl>{message}</lvl>\n"
        fmt_local = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>| <lvl>{level: <8}</lvl>| {name}:{function}:{line}-  <lvl>{message}</lvl>\n"
        if 'host' in record["extra"]:
            return fmt
        else:
            return fmt_local


