from cryptography.fernet import Fernet
import logging as log

log.basicConfig(filename="Cryptography.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

def encryptm(message):

    #the byte form of data, and the normal form of data is the same.

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message)
    logger.info(f'Returned the Encrypted Text: {encMessage}, Key: {key}')
    return encMessage, key

def decryptm(encMessage, key):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(encMessage)
    logger.info(f'Returned the Encrypted Text: {decMessage}, Key: {key}')
    return decMessage.decode()

#val, key = encryptm(b'Hello')
# print(val)
# print(decryptm(val, key))

#encryptm(b'Hello there')
