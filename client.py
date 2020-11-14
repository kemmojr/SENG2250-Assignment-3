# file for the client side of the SSL handshake

import socket

HOST = '127.0.0.1'
PORT = 60051

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # send all the communication that is on the client side of the SSL handshake
    s.sendall(b'Client Hello')
    data = s.recv(1024)
    print('Received', repr(data))
    # sends all the client hello info
    s.sendall(b'SSL version\\Timestamp\\nonce\\Session ID\\Cipher suite\\Compression methods: list of algorithms')
    data = s.recv(1024)
    print('Received', repr(data))
    s.sendall(b'Client continue')
    data = s.recv(1024)
    print('Received\n', repr(data))  # receives all of the information from the server hello
    s.sendall(b'Client received')
    data = s.recv(1024)
    print('Received\n', repr(data))
    # client has received all of the server hello info
    # client checks whether the server accepted the sent security parameters
    # client does client key exchange which involves pre-master secret key and
    # encrypting using the provided server public key
    # Client changes the cipher spec and makes the agreed cipher spec current
    # Finished -
    # verifies the key echange and authentication &
    # signed hash code using master secret calculated from pre master secret (use sha256 here)
    s.sendall(b'Client Finished')
    data = s.recv(1024)
    print('Received\n', repr(data))
    print("Client has finished")


