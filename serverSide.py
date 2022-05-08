#from msilib import CAB
from fileinput import filename
from ntpath import join
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import os
import sys
import socket
import pickle
import struct
import csv
import numpy
import glob

BUFFER = 1024


def sendObject(obj, sock):
    pass

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
    #returns a byte stream
    return pick_f




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

    pk_file =open("server_file/" +str(filename), 'wb')
    bytes =0
    while bytes < file_size:
        file_buffer = sock.recv(BUFFER)
        pk_file.write(file_buffer)
        bytes += len(file_buffer)
    
    pk_file.close()
    unpick_f =pickle.load(pk_file)
    return unpick_f

def addCtxt(sock):
    print("Entering ctxt method")
    #retrieve file name
    sock.send(b'1')
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
    

def unpackObj(sock):
    print("Entering unpack method")
    sock.send(b'1')
    #file_header = struct.unpack("h", sock.recv(2))[0]
    filename = sock.recv(1024).decode()

    sock.send(b'1') #ack of file name

    #retrieve file size
    file_size = struct.unpack("i", sock.recv(4))[0]
    #file_size = 

    sock.send(b'1')

    #receive pickled file stream and write

    with open("server_file/" +str(filename), 'wb') as pk_file:
        bytes =0
        while bytes < file_size:
            file_buffer = sock.recv(BUFFER)
            pk_file.write(file_buffer)
            bytes += len(file_buffer)
    
    pk_file =open("server_file/" +str(filename),'rb')
    unpick_f =pickle.load(pk_file)
    return unpick_f





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
    print("waiting for input")
    with conn:
        print(f'receive input {val}')
        while True:
            
            if val == 'HE':
              x = unpackObj(conn)
              HE_CL = x
              conn.send(b'1')
              val = conn.recv(1024).decode()

            elif val == 'ctxt':
                x = unpackObj(conn)
                conn.send(b'1')
                val = conn.recv(1024).decode()

            elif val == 'ls':
                file_lst =glob.glob("server_file/*.ctxt")
                db_lst = glob.glob("server_file/*.db")
                lst = file_lst + db_lst
                pick_lst =pickle.dumps(lst)
                conn.send(pick_lst)
                val = conn.recv(1024).decode()

            elif val == 'db_down':
                f = unpackObj(conn)
                conn.send(b'1')
                val = conn.recv(1024).decode()

            elif val == 'Query':
                #error here
                conn.send(b'1') #ack for receiving query, wait for operation
                print('ack for receiving query')
                op = conn.recv(1024).decode() #operation

                conn.send(b'1') #operation ack
                print('ack for receiving operation')
                pick_operands =conn.recv(1024)

                operands = pickle.loads(pick_operands)

                conn.send(b'1')  #operands ack

                #ctxt with float val of 0.0
                
                    

                unpick_filled_val = unpackObj(conn)
                unpick_filled_val._pyfhel = HE_CL

                if op == 'add_all': # all data is sent as a vector so the algos can do operations as a vector
                    #open existing filepath of operand and create filereader
                    oper_lst = []
                    for file_path in operands:
                        fp = file_path 
                        if 'server_file' not in fp :
                            fp ='server_file/' + fp
                        
                        oper_file = open(fp,'rb')
                        oper_lst.append(pickle.load(oper_file))
                    
                        #need to attach HE_CL to ctxts or else it will throw an error
                        
                        for oper in oper_lst:
                            for ctxt in oper:
                                ctxt._pyfhel = HE_CL

                        #val of 
                        #numpy array of float vals
                        for oper in oper_lst:
                            for ctxt in oper:
                                unpick_filled_val = unpick_filled_val+ ctxt

                        pick_result = pickle.dumps(unpick_filled_val)
                        conn.send(pick_result)
                        
                        
                        conn.recv(1024)
                        
                        



                        
                            

                if op == 'sub':
                    pass
                if op == 'avg':
                    pass

                if op == 'sum':
                    pass
                
                if op == 'mult':
                    pass

                if op == 'cdiv':
                    pass

                if op == 'div':
                    pass

                if op == 'min':
                    pass
                if op == 'max':
                    pass

                
                print("exiting query operations on server")
                conn.send(b'1')
                val = conn.recv(1024).decode()
                


            else:
                print("exiting program")
                conn.close()
                break
                #HE_CL.decrypt(CA)   throws error because it is incapable of decrypting 
                #without priv key
                #simple addition operation of two ciphertexts

                #remember file is still pickled

                #noise budget has error but it may be because theres no private key here
                #if file is sent over perhaps it wont crash T.T on decryption

                #we must pickle the result and send 
                # filesize and then byte stream

                #sending file length
                
            
'''
                with open('server_file/sum.ctxt', 'rb') as file_contents:
                    fc = file_contents.read(1024)
                    while fc:
                        conn.send(fc)
                        print("sending segment")
                        #print(str(fc))
                        fc = file_contents.read(1024)
                        '''
                        
                


'''
            might not need to send pub key
            if val == 'pk':
              x =unpackObj(conn)
              print(x)
              HE_pk = x
              #HE_CL.from_bytes_publicKey(HE_pk)
              conn.send(b'1') 
              val = conn.recv(1024).decode()
            '''



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