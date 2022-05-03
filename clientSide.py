"""
Client/Server demo with Pyfhel
========================================

Context Parameters shows how several parameters affect performance.
"""

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import tempfile
import json
from pathlib import Path
import socket
import numpy as np
import csv
import pickle

# Using a temporary dir as a "secure channel"
# This can be changed into real communication using other python libraries.
secure_channel = tempfile.TemporaryDirectory()
sec_con = Path(secure_channel.name)
pk_file = "mypk.pk"
contx_file = "mycontx.con"


##### CLIENT
#HE Object Creation, including the public and private keys
HE = Pyfhel()    
HE.contextGen(p=65537, m=2**12) 
HE.keyGen() # Generates both a public and a private key

# Saving only the public key and the context
HE.savepublicKey(pk_file)
HE.saveContext(contx_file)

#for the sake of brevity we're going to send a list of values and then the server will
# for this example send back one Ctxt object with the operation done on it
csvDict = {}
with open("toy_dataset.csv", "r", newline='') as f:
    csvReader = csv.DictReader(f)
    for entry in csvReader:
        csvDict[entry['Number']] = [entry['City'],entry['Gender'],entry['Age'], entry['Illness']]  #city,gender,age,income,illness

#serialize the public key, context and send over the network


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    for x in range(1,11): #1 to 10 0 is not in the csv as a starting point
        val =int(csvDict[str(x)][2])
        encVal =HE.encryptInt(val)



'''
#encrypt values and then send each value over to network

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for x in range(1,11): #1 to 10 0 is not in the csv as a starting point
        val =int(csvDict[str(x)][2])
        HE.encryptInt(val)
        #pickle value and send over connection
        print(f"Received {data!r}")
'''