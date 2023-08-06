from CONFIG import firebaseConfig
from CONFIG import firebaseLocation
import pyrebase

class SYNCHRONIZE:
    def __init__(self):
        self.connection = firebaseConfig
        self.establishConnection()

    def establishConnection(self):
        firebase = pyrebase.initialize_app(self.connection)
        self.storage = firebase.storage()
        self.database = firebase.database()

    def uploadFile(self, filename, cloudfilename):
        cloudpath = firebaseLocation + str(cloudfilename)
        self.storage.child(cloudfilename).put(filename)
        pass

    def downloadFidownloadFilesles(self, cloudfilename):
        cloudpath = str(firebaseLocation) + str(cloudfilename)
        self.storage.child(cloudpath).download(cloudfilename)

    def upload2Database(self, data):
        self.database.child('UserDetails').child(data['username']).set(data)
    
    def checkUsernameExist(self, username):
        data = self.database.child("UserDetails").order_by_child("username").equal_to(str(username)).get()
        count = 0
        for i in data.each():
            count = count + 1
        
        if count < 1:
            return False
        else:
            return True

obj = SYNCHRONIZE()
obj.establishConnection()
# test = str(firebaseLocation)+str()
#obj.downloadFiles('Seaborn_Cheatsheet_Datacamp.png')
# obj.upload2Database()
# print(obj.checkUsernameExist('joel'))
