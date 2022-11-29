# zmq_logger

A quick and dirty client and logger based on loguru and zmq for
logging over a network. 

Start the server, binding to suitable port, and then you can
send messages from multiple clients.

It is currently using pickle with no security consideration, so don't use it on an untrusted network. 