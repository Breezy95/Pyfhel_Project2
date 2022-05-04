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

BUFFER = 1024

#server acts as FTP server, then performs computation.
def pkSetup(sock):
    sock.send(b'1') #ack of method

    #retrieve file name
    file_header = struct.unpack("h", sock.recv(2))[0]
    filename = sock.recv(file_header).decode()

    sock.send(b'1') #ack of file name

    #retrieve file size
    file_size = struct.unpack("i", sock.recv(4))[0]

    sock.send(b'1')

    #receive pickled file
    #contents are consistently small enough that 
    # I decided to leave this as one line
    pick_f =sock.recv(1024)
    print()
    #returns a byte stream
    return pick_f



'''
#context is pickled inside HE
def HESetup(sock):
    sock.send(b'1') #ack of method

    #retrieve file name
    file_header = struct.unpack("h", sock.recv(2))[0]
    filename = sock.recv(file_header).decode()

    sock.send(b'1') #ack of file name

    #retrieve file size
    file_size = struct.unpack("i", sock.recv(4))[0]

    sock.send(b'1')

def addCtxt(sock):
    sock.sendall(bytes('1','utf8')) #ack of method

    #retrieve file name
    file_header = struct.unpack("h", sock.recv(2))[0]
    filename = sock.recv(file_header).decode()

    sock.send(b'1') #ack of file name

    #retrieve file size
    file_size = struct.unpack("i", sock.recv(4))[0]

    sock.send(b'1')

    #receive pickled file stream and write

    pk_file =open("server_file/" +str(filename), 'wb')
    bytes =0
    while bytes < file_size:
        file_buffer = sock.recv(BUFFER)
        pk_file.write(file_buffer)
        bytes += len(file_buffer)
    
    pk_file.close()
    unpick_f =pickle.load(pk_file)
    return unpick_f
    
'''



#main method, switch statement:
# global vars: HE, use regex to load list of 
# ciphertexts
if __name__ == "__main__":    
    HE_CL = Pyfhel()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 50001))
    s.listen(1)
    conn, addr = s.accept()
    val = conn.recv(1024).decode()
    #when pickling a pyfhel object only context is serialized
    #keys must be transmitted independently
    with conn:
        while True:    
            if val == 'pk':
              x =pkSetup(conn)
              print(x)
              HE_pk =pickle.loads(x)
              #HE_CL.from_bytes_publicKey(HE_pk)
              conn.send(b'1') 
              val = conn.recv(1024).decode()
            #might be unnecessary
            elif val == 'HE':
             # x = HESetup(s)
             # HE_CL = x
              val = conn.recv(1024).decode()

            elif val == 'ctxt':
              #  addCtxt(s)
                val = s.recv(1024).decode()

            else:
                print("exiting program")







        
        





    '''
    need python3.10 for match statements
    match val:
        case 'pk':
            pass
        case 'ctxt':
            pass
        case 'add':
            pass
        case _:
            conn.send(b'invalid query')
            print('invalid query')
'''
#upon receiving files it will create the public key and then perform calculations



#might be better to use some webserver functionality here
#that way it can receive and do the math without adding complex code