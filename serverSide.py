from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import json
from pathlib import Path
import socketserver
import pickle
import socket



HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432
x = PyCtxt()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        HE_CL = pickle.loads(data)
        val = conn.recv(1024)
        while(val != b'm'):
            val = conn.recv(1024)
            ctxtVal = pickle.loads(val)


'''

class MyHandler(socketserver.StreamRequestHandler):
    def handle(self):
        addr = self.request.
        print a    

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
x = []


'''

