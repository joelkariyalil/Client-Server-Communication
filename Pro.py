import socket
from cryptography.fernet import Fernet
import logging as log
import datetime
import sys
import time
import argparse

log.basicConfig(filename="Server-Client.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

class Cryptography:

    def encrypt(self,message):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        enc_message = fernet.encrypt(message)
        logger.info(f'Returned the Encrypted Text: {enc_message}, Key: {key}')
        return enc_message, key

    def decrypt(self,enc_message, key):
        try:
            fernet = Fernet(key)
            dec_message = fernet.decrypt(enc_message)
            logger.info(f'Returned the Encrypted Text: {dec_message}, Key: {key}')
            return dec_message.decode()
        except Exception as e:
            print("Error: " + str(e))

class Server:

    def __init__(self):
        self.host = self.get_ip_address()
        self.port = 8080


    def get_ip_address(self):
        try:
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            return ip_address
        except socket.error as e:
            print("Error:", e)
            return None

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        server_socket.bind(server_address)
        server_socket.listen(1)

        print(f"Server listening on {self.host}:{self.port}")

        client_socket, client_address = server_socket.accept()
        print("Connected by:", client_address)
        logger.info(f'Connection Established by {client_address}')

        cryptography = Cryptography()

        while True:
            rec = client_socket.recv(1024)
            key = client_socket.recv(1024)
            logger.info(f'Key: {key}')

            data = cryptography.decrypt(rec, key)
            if not data:
                break
            print("Received:", data)

            response = data

            response, key = cryptography.encrypt(response.encode())
            client_socket.send(response)
            client_socket.send(key)

        client_socket.close()
        server_socket.close()

class Client:

    def __init__(self):
        self.reconn_attempts = 0
        self.max_reconn_attempts = 5

    def send_text(self, client_socket):
        message = input("Enter the text message to send: ")
        if sys.getsizeof(message) <= 1024:
            logger.info('Sent text to Encryption')
            mes, key = cryptography.encrypt(message.encode())
            logger.info('The Text Message is Encrypted')

            client_socket.send(mes)
            client_socket.send(key)

            response = client_socket.recv(1024)
            key = client_socket.recv(1024)

            logger.info(key)
            response = cryptography.decrypt(response, key)
            logger.info('Received Response from the Server')
            print("Server response:", response)
        else:
            print('The Text Size Limit is 1024 bytes.')

    def send_file_link(self, client_socket):

        file_location = input("Enter the file's location to send: ")

        try:
            with open(file_location, 'rb') as file:
                file_data = file.read()

            logger.info('File read successfully')

            if sys.getsizeof(file_data) <= 1024:
                logger.info('Sent file to Encryption')
                mes, key = cryptography.encrypt(file_data)
                logger.info('The File is Encrypted')

                client_socket.send(mes)
                client_socket.send(key)

                response = client_socket.recv(1024)
                key = client_socket.recv(1024)

                logger.info(key)
                response = cryptography.decrypt(response, key)
                logger.info('Received Response from the Server')
                print("Server response:", response)
            else:
                print('The File Size Limit is 1024 bytes.')

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            logger.error('Issues in Sending/Receiving the File Data')
            print('Exception:', str(e))
    def start(self):
        global cryptography
        cryptography = Cryptography()

        while self.reconn_attempts < self.max_reconn_attempts:
            server_instance=Server()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (server_instance.get_ip_address(), 8080)

            logger.info(server_instance.get_ip_address())

            try:
                client_socket.connect(server_address)
                logger.info('Server - Client Connection has Occurred')

                while True:
                    message = input("\nEnter a message to send to the server (or '1' to quit): ")

                    if message == '1':
                        sys.exit()

                    if message.lower().endswith('-t'):
                        self.send_text(client_socket)
                    elif message.lower().endswith('-l'):
                        self.send_file_link(client_socket)

                    elif sys.getsizeof(message) <= 1024:
                        logger.info('Sent to Encryption')
                        mes, key = cryptography.encrypt(message.encode())
                        logger.info('The Message is Encrypted')

                        client_socket.send(mes)
                        client_socket.send(key)

                        response = client_socket.recv(1024)
                        key = client_socket.recv(1024)

                        logger.info(key)
                        response = cryptography.decrypt(response, key)
                        logger.info('Received Response from the Server')
                        print("Server response:", response)
                    else:
                        print('The Text Limit is 1024 bytes.')

            except socket.error as e:
                logger.error('Socket error: ' + str(e))
                print("Socket error:", e)
                print("Waiting for the server to restart...")
                time.sleep(5)
                self.reconn_attempts += 1
            except KeyboardInterrupt:
                logger.info('Client stopped by user.')
                print("Client stopped by user.")
            except Exception as e:
                logger.error('Issues in Sending/Receiving the Data')
                print('Exception: ' + str(e))
            finally:
                client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Server-Client Program")
    parser.add_argument('--role', choices=['client', 'server','Server','Client'], required=True, help="Specify whether to run as for 'client' or for 'server'")
    args = parser.parse_args()

    if args.role.lower() == 'client':
        client = Client()
        client.start()
    elif args.role.lower() == 'server':
        server = Server()
        server.start()


'''import socket
from cryptography.fernet import Fernet
import logging as log
import datetime
import sys
import time
import argparse

log.basicConfig(filename="Server-Client.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

class Cryptography:

    def encrypt(message):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        enc_message = fernet.encrypt(message)
        logger.info(f'Returned the Encrypted Text: {enc_message}, Key: {key}')
        return enc_message, key

    def decrypt(enc_message, key):
        try:
            fernet = Fernet(key)
            dec_message = fernet.decrypt(enc_message)
            logger.info(f'Returned the Encrypted Text: {dec_message}, Key: {key}')
            return dec_message.decode()
        except Exception as e:
            print("Error: " + str(e))

class Server:

    def __init__(self):
        self.host = self.get_ip_address()
        self.port = 8080


    def get_ip_address():
        try:
            host_name = socket.gethostname()
            ip_address = socket.gethostbyname(host_name)
            return ip_address
        except socket.error as e:
            print("Error:", e)
            return None

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.host, self.port)
        server_socket.bind(server_address)
        server_socket.listen(1)

        print(f"Server listening on {self.host}:{self.port}")

        client_socket, client_address = server_socket.accept()
        print("Connected by:", client_address)
        logger.info(f'Connection Established by {client_address}')

        cryptography = Cryptography()

        while True:
            rec = client_socket.recv(1024)
            key = client_socket.recv(1024)
            logger.info(f'Key: {key}')

            data = cryptography.decrypt(rec, key)
            if not data:
                break
            print("Received:", data)

            response = data

            response, key = cryptography.encrypt(response.encode())
            client_socket.send(response)
            client_socket.send(key)

        client_socket.close()
        server_socket.close()

class Client:

    def __init__(self):
        self.reconn_attempts = 0
        self.max_reconn_attempts = 5

    def start(self):
        cryptography = Cryptography()

        while self.reconn_attempts < self.max_reconn_attempts:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (Server.get_ip_address(), 8080)

            logger.info(Server.get_ip_address())

            try:
                client_socket.connect(server_address)
                logger.info('Server - Client Connection has Occurred')

                while True:
                    message = input("\nEnter a message to send to the server (or '1' to quit): ")

                    if message == '1':
                        sys.exit()

                    if sys.getsizeof(message) <= 1024:
                        logger.info('Sent to Encryption')
                        mes, key = cryptography.encrypt(message.encode())
                        logger.info('The Message is Encrypted')

                        client_socket.send(mes)
                        client_socket.send(key)

                        response = client_socket.recv(1024)
                        key = client_socket.recv(1024)

                        logger.info(key)
                        response = cryptography.decrypt(response, key)
                        logger.info('Received Response from the Server')
                        print("Server response:", response)
                    else:
                        print('The Text Limit is 1024 bytes.')

            except socket.error as e:
                logger.error('Socket error: ' + str(e))
                print("Socket error:", e)
                print("Waiting for the server to restart...")
                time.sleep(5)
                self.reconn_attempts += 1
            except KeyboardInterrupt:
                logger.info('Client stopped by user.')
                print("Client stopped by user.")
            except Exception as e:
                logger.error('Issues in Sending/Receiving the Data')
                print('Exception: ' + str(e))
            finally:
                client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Server-Client Program")
    parser.add_argument('--role', choices=['client', 'server','Server','Client'], required=True, help="Specify whether to run as for 'client' or for 'server'")
    args = parser.parse_args()

    if args.role.lower() == 'client':
        client = Client()
        client.start()
    elif args.role.lower() == 'server':
        server = Server()
        server.start()


import socket
from cryptography.fernet import Fernet
import logging as log
import datetime
import sys
import time
import argparse

log.basicConfig(filename="Server-Client.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

# GetIP.py
def get_ip_address():

    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except socket.error as e:
        print("Error:", e)
        return None

# Crypt.py
def encryptm(message):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message)
    logger.info(f'Returned the Encrypted Text: {encMessage}, Key: {key}')
    return encMessage, key

def decryptm(encMessage, key):
    try:
        fernet = Fernet(key)
        decMessage = fernet.decrypt(encMessage)
        logger.info(f'Returned the Encrypted Text: {decMessage}, Key: {key}')
        return decMessage.decode()
    except Exception as e:
        print("Error: "+str(e))

# Write.py
def intotxt(message):
    file = open('Server Messages.txt','a')
    str = f"\n{datetime.datetime.now()}\n{message}\n"
    file.write(str)
    file.close()

def start_server():
    host = get_ip_address()
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host,port)
    server_socket.bind(server_address)
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    client_socket, client_address = server_socket.accept()
    print("Connected by:", client_address)
    logger.info(f'Connection Established by {client_address}')

    while True:
        rec = client_socket.recv(1024)
        key = client_socket.recv(1024)
        logger.info(f'Key: {key}')

        data = decryptm(rec, key)
        if not data:
            break
        print("Received:", data)

        response = data

        response, key = encryptm(response.encode())
        client_socket.send(response)
        client_socket.send(key)

        intotxt(data)

    client_socket.close()
    server_socket.close()

def start_client():

    reconn_attempts = 0

    while reconn_attempts < max_reconn_attempts:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (get_ip_address(), 8080)

        logger.info(get_ip_address())

        try:
            client_socket.connect(server_address)
            logger.info('Server - Client Connection has Occurred')

            while True:
                message = input("\nEnter a message to send to the server (or '1' to quit): ")

                if message == '1':
                    sys.exit()

                if sys.getsizeof(message) <= 1024:
                    logger.info('Sent to Encryption')
                    mes, key = encryptm(message.encode())
                    logger.info('The Message is Encrypted')

                    client_socket.send(mes)
                    client_socket.send(key)

                    response = client_socket.recv(1024)
                    key = client_socket.recv(1024)

                    logger.info(key)
                    response = decryptm(response, key)
                    logger.info('Received Response from the Server')
                    print("Server response:", response)
                else:
                    print('The Text Limit is 1024 bytes.')

        except socket.error as e:
            logger.error('Socket error: ' + str(e))
            print("Socket error:", e)
            print("Waiting for the server to restart...")
            time.sleep(5)
            reconn_attempts += 1
        except KeyboardInterrupt:
            logger.info('Client stopped by user.')
            print("Client stopped by user.")
        except Exception as e:
            logger.error('Issues in Sending/Receiving the Data')
            print('Exception: ' + str(e))
        finally:
            client_socket.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Server-Client Program")
    parser.add_argument('--role', choices=['Client', 'Server','client','server'], required=True, help="Specify whether to run as for 'client' or for 'server'")
    args = parser.parse_args()

    max_reconn_attempts = 5

    if args.role.lower() == 'client':
        start_client()
    elif args.role.lower() == 'server':
        start_server()'''