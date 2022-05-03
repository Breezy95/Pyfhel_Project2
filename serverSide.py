from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os
import sys
import socket
import pickle
import struct
import regex

#server acts as FTP server, then performs computation.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50001))
s.listen(1)
conn, addr = s.accept()
BUFFER = 1024
data = conn.recv(BUFFER).decode()
if data == 'pk':
    conn.send(b'1') #ack of method

    #retrieve file name
    file_header = struct.unpack("h", conn.recv(2))[0]
    filename = conn.recv(file_header).decode()

    conn.send(b'1') #ack of file name

    #retrieve file size
    file_size = struct.unpack("i", conn.recv(4))[0]

    conn.send(b'1')

    #loop for file contents
    pk_file =open("server_file/" +str(filename), 'wb')
    bytes =0
    while bytes < file_size:
        file_buffer = conn.recv(BUFFER)
        pk_file.write(file_buffer)
        bytes += len(file_buffer)
    pk_file.close()


    


#upon receiving files it will create the public key and then perform calculations



#might be better to use some webserver functionality here
#that way it can receive and do the math without adding complex code