import socket
import sys
import time
HOST = '127.0.0.1'
PORT = 65432


def run(string):
    print('str: ', string)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        start = time.time()
        s.sendall(str.encode(string))
        data = s.recv(1024)

        print('Received', repr(data), f"\n Time: {time.time() - start} secs")
        return data
