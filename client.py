# file for the client side of the SSL handshake

import socket

HOST = '127.0.0.1'
PORT = 60051

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # send all the communication that is on the client side of the SSL handshake
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))