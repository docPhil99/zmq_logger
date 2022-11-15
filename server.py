# server.py
import sys
import zmq
from loguru import logger
import threading
import json

class ZMQLogger:
    def __init__(self, host="tcp://127.0.0.1",port=9999, logfile='log.txt'):
        self.host= host
        self.port = port
        logger.configure(handlers=[{"sink": sys.stderr, "format":ZMQLogger._formatter}])
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
        addr=f"{self.host}:{self.port}"
        print(f'Addr {addr}')
        self.socket.bind(addr)
        self.socket.subscribe("")
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        while self._run:
            print('get message')
            socks = dict(poller.poll(1000))
            if socks:
                if socks.get(self.socket) == zmq.POLLIN:
                    message= self.socket.recv_multipart(zmq.NOBLOCK)#.decode("utf8").strip()

                    print("got message ",message )
            else:
                print("error: message timeout")
            # try:
            #     _, message = self.socket.recv_multipart(flags=zmq.NOBLOCK)
            #     print(f'Got {message}')
            # except zmq.Again as e:
            #     print('time out')

    @classmethod
    def _formatter(cls,record):
        fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>| <lvl>{level: <8}</lvl>| {name}:{function}:{line} {extra[host]} -  <lvl>{message}</lvl>\n"
        fmt_local = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>| <lvl>{level: <8}</lvl>| {name}:{function}:{line}-  <lvl>{message}</lvl>\n"
        if 'host' in record["extra"]:
            return fmt
        else:
            return fmt_local





#
import time
from zmq.log.handlers import PUBHandler
#
# socket = zmq.Context().socket(zmq.SUB)
# socket.bind("tcp://127.0.0.1:12345")
# socket.subscribe("")
#
# logger.configure(handlers=[{"sink": sys.stderr, "format": "{message}"}])
#
# while True:
#     _, message = socket.recv_multipart()
#     logger.info(message.decode("utf8").strip())

zmlog = ZMQLogger()
zmlog.start()

class LogEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.__dict__ ['records']
        except:
            return obj.__dict__


class myPUBHandler(PUBHandler):
    def format(self,record):
        return LogEncoder().encode(record)


socket = zmq.Context().socket(zmq.PUB)
socket.connect("tcp://127.0.0.1:9999")
handler = myPUBHandler(socket)
logger.add(handler)

for p in range(10):
    logger.info(f"Logging from client {p}")
    time.sleep(1)

zmlog.stop()
#socket = zmq.Context().socket(zmq.SUB)
#socket.bind("tcp://127.0.0.1:12345")
#socket.subscribe("")

#logger.configure(handlers=[{"sink": sys.stderr, "format": "{message}"}])

#while True:
#    _, message = socket.recv_multipart()
#    logger.info(message.decode("utf8").strip())