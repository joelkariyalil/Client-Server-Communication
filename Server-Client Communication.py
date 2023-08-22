import socket
from cryptography.fernet import Fernet
import logging as log
import datetime
import sys
import time
import argparse
from tqdm import tqdm
import threading

log.basicConfig(filename="Server-Client.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)


class Cryptography:

    @staticmethod
    def encrypt(message):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        enc_message = fernet.encrypt(message)
        logger.info(f'Returned the Encrypted Text: {enc_message}, Key: {key}')
        return enc_message, key

    @staticmethod
    def decrypt(enc_message, key):
        try:
            fernet = Fernet(key)
            dec_message = fernet.decrypt(enc_message)
            logger.info(f'Returned the Encrypted Text: {dec_message}, Key: {key}')
            return dec_message.decode()
        except Exception as e:
            print("Error: " + str(e))


class Write:
    @staticmethod
    def into_txt(message):
        file = open('Server Messages.txt', 'a')
        str1 = f"\n{datetime.datetime.now()}\n{message}\n"
        file.write(str1)
        file.close()


class Server:

    def __init__(self):
        self.host = self.get_ip_address()
        self.port = 8080

    @staticmethod
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

        print(f"(Server) - Server listening on {self.host}:{self.port}")

        client_socket, client_address = server_socket.accept()
        print("(Server) - Connected by:", client_address)
        logger.info(f'(Sever) - Connection Established by {client_address}')

        crypto = Cryptography()
        w = Write()

        while True:
            rec = client_socket.recv(1024)
            key = client_socket.recv(1024)
            logger.info(f'Key: {key}')
            if not rec:
                break
            data = crypto.decrypt(rec, key)
            if not data:
                break
            print("Received:", data)

            w.into_txt(data)

            response = data

            response, key = crypto.encrypt(response.encode())
            client_socket.send(response)
            client_socket.send(key)

        client_socket.close()
        server_socket.close()


class Client:

    def __init__(self, host, port):
        self.reconnection_attempts = 0
        self.max_reconnection_attempts = 5
        self.server_IP = host
        self.server_Port = port

    @staticmethod
    def send_text(message, client_socket):
        crypt = Cryptography()
        if sys.getsizeof(message) <= 1024:
            logger.info('Sent text to Encryption')
            mes, key = crypt.encrypt(message.encode())
            logger.info('The Text Message is Encrypted')

            client_socket.send(mes)
            client_socket.send(key)

            response = client_socket.recv(1024)
            key = client_socket.recv(1024)

            logger.info(key)
            response = crypt.decrypt(response, key)
            logger.info('Received Response from the Server')
            print("Server response:", response)
        else:
            print('The Text Size Limit is 1024 bytes.')

    @staticmethod
    def send_file_link(message, client_socket):
        crypt = Cryptography()

        max_chunk_size = 400

        try:
            with open(message, 'rb') as file:
                file_data = file.read()

            logger.info('File read successfully')

            total_chunks = (len(file_data) // max_chunk_size) + 1
            logger.info(f'(Client) Total Chunks in File: {total_chunks}')
            chunks_sent = 0

            for i in tqdm(range(0, len(file_data), max_chunk_size), desc="Sending File"):
                chunk = file_data[i:i + max_chunk_size]

                mes, key = crypt.encrypt(chunk)
                client_socket.send(mes)
                client_socket.send(key)

                response = client_socket.recv(1024)
                key = client_socket.recv(1024)

                response = crypt.decrypt(response, key)

                logger.info(f'(Client) Obtained Response from Server: {response}')

                chunks_sent += 1

            print("File sent successfully")

        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            logger.error('Issues in Sending/Receiving the File Data')
            print('Exception:', str(e))

    def start(self):

        crypt = Cryptography()

        while self.reconnection_attempts < self.max_reconnection_attempts:

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.server_IP, self.server_Port)

            logger.info(f'Connected to Server IP: {self.server_IP}')

            try:
                client_socket.connect(server_address)
                logger.info('Server - Client Connection has Occurred')

                while True:
                    message = input("\nEnter a message to send to the server (or '-q' to quit): ")
                    mes = message[3:]

                    if message.lower().startswith('-t'):
                        self.send_text(mes, client_socket)
                    elif message.lower().startswith('-l'):
                        self.send_file_link(mes, client_socket)

                    elif message.lower().startswith('-q'):
                        sys.exit()

                    elif sys.getsizeof(message) <= 1024:
                        logger.info('Sent to Encryption')
                        mes, key = crypt.encrypt(message.encode())
                        logger.info('The Message is Encrypted')

                        client_socket.send(mes)
                        client_socket.send(key)

                        response = client_socket.recv(1024)
                        key = client_socket.recv(1024)

                        logger.info(key)
                        response = crypt.decrypt(response, key)
                        logger.info('Received Response from the Server')
                        print("Server response:", response)
                    else:
                        print('The Text Limit is 1024 bytes.')

            except socket.error as e:
                logger.error('Socket error: ' + str(e))
                print("Socket error:", e)
                print("Waiting for the server to restart...")
                time.sleep(5)
                self.reconnection_attempts += 1
            except KeyboardInterrupt:
                logger.info('Client stopped by user.')
                print("Client stopped by user.")
            except Exception as e:
                logger.error('Issues in Sending/Receiving the Data')
                print('Exception: ' + str(e))
            finally:
                client_socket.close()


class ClientPing:
    def __init__(self):
        self.available_hosts = []

    @staticmethod
    def ping_host(host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.settimeout(1)  # Set a timeout for the connection attempt
            client_socket.connect((host, port))
            logger.info(f"Connected to {host}")
            client_socket.close()
            return True
        except (socket.error, socket.timeout):
            return False

    def scan_host(self, host, port):
        if self.ping_host(host, port):
            logger.info(f"Host {host} is available")
            self.available_hosts.append((host, port))
        else:
            logger.info(f"Host {host} is not available")

    def scan_network(self, network_range, port):
        threads = []
        for third_section in range(20):                    # Preferably be 255; reduced to 20 to ensure better speed.
            for fourth_section in range(256):
                host = f"{network_range}.{third_section}.{fourth_section}"
                thread = threading.Thread(target=self.scan_host, args=(host, port))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        return self.available_hosts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Server-Client Program")
    parser.add_argument('--role', choices=['client', 'server', 'Server', 'Client'], required=True,
                        help="Specify whether to run as for 'client' or for 'server'")
    args = parser.parse_args()

    if args.role.lower() == 'client':
        client_ping = ClientPing()
        hosts_available = client_ping.scan_network('192.168', 8080)
        server_IP = hosts_available[0][0]
        server_Port = hosts_available[0][1]
        log.info(f'(Client) Returned From Client Ping: IP: {server_IP}, Port: {server_Port}')
        client = Client(server_IP, server_Port)
        client.start()

    elif args.role.lower() == 'server':
        server = Server()
        server.start()
        server.start()
