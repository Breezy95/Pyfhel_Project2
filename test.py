from Pyfhel import Pyfhel, PyPtxt, PyCtxt


HmoEnc = Pyfhel()
HmoEnc.contextGen(p = 65537)

HmoEnc.keyGen()

print("This is the context and key setup")
print(HmoEnc)


int1 = 127
int2 = -2

ctxt1 = HmoEnc.encryptInt(int1)
ctxt2 = HmoEnc.encryptInt(int2)


print("3. Integer Encryption")
print("    int ",int1,'-> ctxt1 ', type(ctxt1))
print("    int ",int2,'-> ctxt2 ', type(ctxt2))

ctxtSum = ctxt1 + ctxt2

resSum = HmoEnc.decryptInt(ctxtSum)

print("#. Decrypting result:")
print("     addition:       decrypt(ctxt1 + ctxt2) =  ", resSum)


