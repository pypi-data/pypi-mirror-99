from crptography.fernet import  Fernet
import rsa
# open the symetric key file
skey = open('symmetric.key','rb')
key = skey.read()

#create the cipher
cipher = Fernet(key)

#open file for encrypting

myfile = open('mysecretdata','rb')
myfiledata = myfile.read()

#encrypt the dada
encrypted_data = cipher.encrypt(myfiledata)
edata = open('encrypted_file','wb')
edata.write(encrypted_data)

print(encrypted_data)

# open the public key file
pkey = open('publickey.key','rb')
pkdata = pkey.read()

#load the file
pubkey = rsa.Publickey.load_pkcsl(pkdata)

#encrypt the symmetric key file with the public key
encrypted_key = rsa.encrypt(key,pubkey)

#write the encryptedsymmetric key to a file
ekey = open('encrypted_key','wb')
ekey.write(encrypted_key)

print(encrypted_key)
