from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import os
import socket
import pickle
import struct

#call this function when requesting results of data
#operation is a string  used to represent the type of
#operation the server will do on the data
#should receive a ciphertext
def reqData(sock, operation):
    sock.send(bytes(operation))

    with open(operation, 'wb') as f:
        bytes =0
        

#process which iswhat we want sent(pk, ctxt,context), filename, socket
def sendFile(proc,fn,sock):
    sock.send(bytes(proc,'utf8'))  #send process to be done
    v = sock.recv(1024).decode()   #wait for ack of prev msg
    print(f"received process ack: {v}")
#send file name
    print(fn)
    sock.send(fn.encode())

    v=sock.recv(1024).decode()
    print(f"received filename ack : {v}")

    #pickle file here
    #pickled_file = pickle.dumps()
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

    #pk_file = "mypk.pk"
    #HE.savepublicKey(pk_file)

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

    #serialize pub key
    pick_pk = pickle.dumps(HE)
    with open("pick_pk.pk","wb") as pk_f:
        pk_f.write(pick_pk)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))

    #pk,HE,ciphtxt,ctx
    sendFile('pk','pick_pk.pk',s)
    print("exit method")
    sendFile('pk','pick_pk.pk',s)
    
    #s.send(bytes('ctxt','utf8'))
    #sendFile('HE','ca.ctxt',s)


    














