# client.py
import zmq
from zmq.log.handlers import PUBHandler
from loguru import logger
import time

socket = zmq.Context().socket(zmq.PUB)
socket.connect("tcp://127.0.0.1:9999")
handler = PUBHandler(socket)
logger.add(handler)

for p in range(20):
    logger.info(f"Logging from client {p}")
    time.sleep(1)