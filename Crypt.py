from cryptography.fernet import Fernet
import json

def encryptm(message):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    
    file = open('key.txt','wb')
    file.write(key)
    file.close()
    return encMessage

def decryptm(encMessage):

    #read the key from the Notepad File

    file = open('key.txt','rb')
    key=file.read()
    fernet = Fernet(key)
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage

'''
val=encryptm('Hello')

print(val)
print(decryptm(val))
'''