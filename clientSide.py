from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import os
import socket
import pickle
import struct

#call this function when requesting results of data
#operation is a string  used to represent the type of
#operation the server will do on the data
#should receive a ciphertext
def reqData(sock, operation, he):
    sock.send(b'Query')
    x =sock.recv(4096)
    #sock.send(bytes(operation))
    print(he.dec)
    with open('test.d', 'wb') as f:
        bytes =0
        

#process which iswhat we want sent(HE, ctxt,context), filename, socket
def sendFile(proc,fn,obj,sock):
    sock.send(bytes(proc,'utf8'))  #send process to be done
    print("waiting for proc. ack")
    v = sock.recv(1024).decode()   #wait for ack of prev msg
    print(f"received process ack: {v}")
#send file name
    print(fn)
    sock.send(fn.encode())
    
    v=sock.recv(1024).decode()
    

    #serialize obj and write to file
    pick_obj = pickle.dumps(obj)
    with open(fn,"wb") as pk_f:
        pk_f.write(pick_obj)

#send file size
    print(os.path.getsize(fn))
#use struct pack to send file size (is it needed?)
    
    sock.send(struct.pack("i", os.path.getsize(fn)))
    v =sock.recv(1024).decode() #wait for ack
    print("received  file size ack: {v}")

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



if __name__ == "__main__":
    
    HE = Pyfhel()
    HE.contextGen(p=65537, m=2**12)
    HE.keyGen()

    print(HE)

    pk_file = "mypk.pk"
    HE.savepublicKey(pk_file)

    ctx_file = "myctx.con"
    HE.saveContext(ctx_file)
    a = 1.5
    b = 2.5
    ca = HE.encryptFrac(a)
    cb = HE.encryptFrac(b)
    ca.to_file('ca.ctxt')
    cb.to_file('cb.ctxt')

    #send files to server
    HOST = '127.0.0.1'
    PORT = 50001



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))
    s.settimeout(None) #socket will wait until recv is filled

    #pk,HE,ciphtxt,ctx
    #test runs
    sendFile('HE','pick_pk.pk',HE,s)
    s.recv(1024)
    sendFile('ctxt','ca.ctxt',ca,s)
    s.recv(1024)  #blocks socket so client doesnt send files before server is ready to move on
    sendFile('ctxt','cb.ctxt',cb,s)
    s.recv(1024)
    reqData(s,'+',HE)
    
    



    #sendFile('pk',pk_file,HE.,s)
    
    #database file
    # we could send individual files but I believe 
    # the assignment calls for the database file to be on the server?
    #this will not change the functionality of anything in my opinion
    #Pyfhel can encrypt arrays and then we can serialize and send
    #  the arrays over the connection
    
    
    #sendFile('pk','pick_pk.pk',s)
    
    
    


    














