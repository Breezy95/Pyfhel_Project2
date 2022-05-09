from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import os
import socket
import pickle
import struct
import csv
import numpy as np
import time

#call this function when requesting results of data
#operation is a string  used to represent the type of
#operation the server will do on the data
#should receive a ciphertext

def receiveObject(sock):
    
    #code for receiving file

    f_name =sock.recv(1024).decode() # recv file name
    print(f'recv file name: {f_name}')
    sock.send(b'1') # ack for file name

    f_size = struct.unpack("i", sock.recv(4))[0] # file size

    sock.send(b'1') # file size ack

    with open(f'client_file/{f_name}','wb') as f:
        bytes =0
        while bytes < f_size:
            seg =s.recv(1024)
            f.write(seg)
            bytes+= len(seg)

    pick_f =open(f'client_file/{f_name}','rb')
    unpick_f = pickle.load(pick_f)   
    pick_f.close() 
    unpick_f._pyfhel = HE
    
    print(HE.decryptFrac(unpick_f))

    return unpick_f



def reqData(sock, operation, operands,he): # remember to pickle the objects
    
    print("entering reqData")
    sock.send(b'Query')
    
    v =sock.recv(1024)
    print(f'received query ack: {v}')
    # send operation
    sock.send(bytes(operation,'utf8'))
    #file_size = struct.unpack("i", sock.recv(4))[0]
    

    #server ack

    v =sock.recv(1024)
    print(f'received operation ack: {v}')

    #client sends operands 
    sock.send(pickle.dumps(operands))
    print('sending operand')

    #server ack for  operands
    v =sock.recv(1024)
    print(f'received operand ack: {v}')

    #send ctxt with value 0
    float_zero = HE.encryptFrac(float(0))

    s.recv(1024) #server should enter unpack obj here
    sendFile('1','pick_zero.ctxt',float_zero,s)
    print('sent empty cyphertext')

    ans =receiveObject(s)
    
    print(HE.decryptFrac(ans))
    return ans
    



    
    '''
    #receiving pickled data object
    with open('sum.ctxt', 'wb') as pk_file:
        bytes =0
        while bytes < file_size:
            file_buffer = sock.recv(1024)
            pk_file.write(file_buffer)
            bytes += len(file_buffer)
            print(f'the size of the file being written is currently {bytes} while the pickled filesize is {file_size}')

    #unpickle object and then decrypt
    pick_f = open('sum.ctxt','rb')
    unpick_ctxt =pickle.load(pick_f)
    unpick_ctxt._pyfhel = he 
    print('what is the sum')
    print(unpick_ctxt.decrypt())
    '''

#process which iswhat we want sent(HE, ctxt,context), filename, socket
def sendFile(proc,fn,obj,sock):
    if(proc != '1'):
        sock.send(bytes(proc,'utf8'))  #send process to be done
        print("waiting for proc. ack")
        v = sock.recv(1024).decode()   #wait for ack of prev msg
        print(f"received process ack: {v}")


#send file name
    print(fn)
    sock.send(fn.encode())
    print('sent file name')
    v=sock.recv(1024).decode()
    print(f'received filename ack {v}')
    

    #serialize obj and write to file
    pick_obj = pickle.dumps(obj)
    with open(fn,"wb") as pk_f:
        pk_f.write(pick_obj)

#send file size
#print(os.path.getsize(fn))
#use struct pack to send file size (is it needed?)
    
    sock.send(struct.pack("i", os.path.getsize(fn)))
    v =sock.recv(1024).decode() #wait for ack
    print(f"received  file size ack: {v}")

#send file contents
#send in segments so theres no weird file overlap with
#other files
    with open(fn, 'rb') as file_contents:
        fc = file_contents.read(1024)
        while fc:
            sock.send(fc)
            print("sending segment")
        #print(str(fc))
            fc = file_contents.read(1024)
    
    v =s.recv(1024)
    print(f'received file transfer ack {v}')
            



if __name__ == "__main__":
    
    HE = Pyfhel()
    HE.contextGen(p=65537, m= 2**12)
    HE.keyGen()

    print(HE)

    pk_file = "mypk.pk"
    HE.savepublicKey(pk_file)

    ctx_file = "myctx.con"
    HE.saveContext(ctx_file)
    #send files to server
    HOST = '127.0.0.1'
    PORT = 50001

    c1 = HE.encryptFrac(95.0)
    c2 = HE.encryptFrac(95.0)

    print(HE.decryptFrac(c1 + c2))



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.settimeout(None) #socket will wait until recv is filled

    #pk,HE,ciphtxt,ctx
    #test runs

                #open database, encrypt pairs and send
             
    
    db_list = []
    inp_list = []
    enc_entry = []
    cond = True
    while cond:
        inp =input('enter preferred operation: ')
        match inp:

            case 'HE':
                sendFile('HE',pk_file,HE,s)
                
                #s.recv(1024) #ack of sent HE

            case 'db_num':

                with open('toy_dataset.csv','r') as toy_f:

                        print("enter the columns you would like to use each one must be separated by enter/newline: ")
                        print('type stop to continue')
                        reader = csv.DictReader(toy_f)
                        #dict_from_csv = dict(list(reader)[0])
 
                        #readerlist from the keys of the dict
                        #column_names = list(dict_from_csv.keys())
                        while True:
                         #   print(column_names)
                            print('only numerical categories and must be more than one')
                            inp = input()
                            if inp == 'stop' and len(inp_list) > 0:
                                break
                            if inp in reader.fieldnames:
                                inp_list.append(inp)
                            else:
                                print('not a category name in the file')

                        m = int(input('enter the starting row'))
                        n = int(input('enter the end row'))
                        cat_lst = {}

                        for cat in inp_list:    # array for each category
                            cat_lst[cat] =np.empty(n-m+1,dtype=PyCtxt)

                        ind = 0
                        for row in reader:  # we now iterate through dict reader, later on I might add ranges
                            if int(row['Number']) < int(m):
                                continue
                            if int(row['Number']) > int(n):
                                break
                            
                            for cat in inp_list: 
                                   #goes through values selected
                                #encrypting by row and inserting into array
                                #  gives one pyctxt object instead of multiple
                                #instead we try going row by row
                                cat_lst[cat][ind] = HE.encryptFrac(float(row[cat]))
                                print(HE.decryptFrac(cat_lst[cat][ind]))
                            ind +=1

                            #save dbs as a file
                            #we can pull dbs because they will be in the order given
                            #by the keys in the categ dict 
                            #{categ}{m}to{n}.db

                            #find out how to prep server for multiple sends
                            # can still be done with one cat
                        for column in cat_lst.keys():
                            if cat_lst[column].size >0:
                                sendFile('db_down',f'{column}{m}to{n}.db',cat_lst[column],s)



            case 'val':  #sends an encrypted value over
                val = input("enter value, if float round up or down")

            case 'ls': #list files in server directory
                s.send(bytes('ls','utf8'))
                pick_dir = s.recv(1024)
                unpick_dir = pickle.loads(pick_dir)
                print(unpick_dir)

            case 'op':
                op =input("Enter the operation you want done: ")
                oper_lst = []
                operands = ''
                while operands != 'stop':
                    operands = input('Enter the files you want to be operated on, they must be of the same encryption: ')
                    if operands == 'stop':
                        break
                    oper_lst.append(operands)
                start = time.time()
                reqData(s,op, oper_lst, HE)
                end = time.time()
                print(f'time elapsed: {start-end}')

            case 'kill':
                cond = False
                break

            case _:
                print('not a valid entry\n commands are db_num, HE, val, ls, op ')




''' a = 1.5
    b = 2.5
    ca = HE.encryptFrac(a)
    cb = HE.encryptFrac(b)
    ca.to_file('ca.ctxt')
    cb.to_file('cb.ctxt')
    print(cb._encoding)'''

    




'''       
    sendFile('HE','pick_pk.pk',HE,s)
    s.recv(1024)
    sendFile('ctxt','ca.ctxt',ca,s)
    s.recv(1024)  #blocks socket so client doesnt send files before server is ready to move on
    sendFile('ctxt','cb.ctxt',cb,s)
    s.recv(1024)
    reqData(s,'+',HE)
    s.recv(1024)
    s.send(b'LEAVE')
    '''

    
    


    














