from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import os
import socket
import pickle
import struct

#process which iswhat we want sent(pk, ctxt,context), filename, socket
def sendFile(proc,fn,sock):
    s.send(bytes(proc))  #send process to be done
    v = s.recv(1024).decode()   #wait for ack of prev msg
    print(f"received process ack: {v}")
#send file name

    s.send(fn.encode())

    v=s.recv(1024).decode()
    print(f"received filename ack : {v}")
#send file size
    print(os.path.getsize(fn))
#use struct pack to send file size (is it needed?)
    s.send(struct.pack("i", os.path.getsize(fn)))
    v =s.recv(1024).decode() #wait for ack
    print("received  file size ack: {v}")


#send file contents
#send in segments so theres no weird file overlap with
#other files
    with open(fn, 'rb') as file_contents:
        fc = file_contents.read(1024)
        while fc:
            s.send(fc)
            print("sending segment")
        #print(str(fc))
            fc = file_contents.read(1024)




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

#serialize pub key
pick_pk = pickle.dumps(HE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#pk or ctxt
sendFile('pk',pk_file,s)

            














