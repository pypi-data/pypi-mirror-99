import rsa
from cryptography.fernet import Fernet
import uuid
import os
import json
from sync import SYNCHRONIZE

class InitializeRSA:
    def __init__(self, reset=False):
        self.reset = reset

        self.USER_CONFIG = {}

        username = self.createUser()
        ## Add the username to the config file
        self.USER_CONFIG['username'] = username
        
        if self.reset:
            self.recreateRSA()
        else:
            self.createDirectory()
            self.createRSA()
        

        sync = SYNCHRONIZE()
        sync.upload2Database(data=self.USER_CONFIG)

    def filesExistsorNot(self):
        if (os.path.exists(self.path) & os.path.exists(self.path + '/PrivateKey') & os.path.exists(self.path + '/user.config')):
            print('All the files exist')
        else:
            print('Some files are missing...')
    
    def createDirectory(self):
        # Directory 
        self.directory = "test"
        
        # Parent Directory path 
        parent_dir = "."
        
        # Path 
        self.path = os.path.join(parent_dir, self.directory) 

        # Check is the file already exsits or not
        try: 
            os.makedirs(self.path, exist_ok = True) 
            print("Directory '%s' created successfully" % self.path) 
        except OSError as error: 
            print("Directory '%s' can not be created" % self.directory)

    def deleteFiles(self):
        if os.path.exists("demofile.txt"):
            os.remove("demofile.txt")
        else:
            print("The file does not exist") 
        os.rmdir("myfolder")

    def checkUserConfigExists(self):
        return os.path.exists(self.path+'/user.config')
        

    def recreateRSA(self):
        pass
    


    def createRSA(self):
        (publicKey, privateKey) = rsa.newkeys(2048)

        with open(self.path + "/PrivateKey", 'wb') as prkey:
            prkey.write(privateKey.save_pkcs1())
        
        self.USER_CONFIG['PublicKey_FILENAME'] = uuid.uuid1().hex

        with open(self.path + "/" + self.USER_CONFIG['PublicKey_FILENAME'],'wb') as pubkey:
            pubkey.write(publicKey.save_pkcs1())
        
        with open(self.path + "/user.config", 'w') as uc:
            uc.write(json.dumps(self.USER_CONFIG))
    
    def enterUsername(self):
        print("Enter a username (which will be used by all): ")
        username = input()
        print("Re-enter the username: ")
        username2 = input()

        return username, username2
    
    def createUser(self, username=None):
        sync = SYNCHRONIZE()
        username, username2 = self.enterUsername()

        if username.strip() == username2.strip():
            if sync.checkUsernameExist(username):
                exit('Already exists...')
        else:
            exit("Username mismatch...")

        return username