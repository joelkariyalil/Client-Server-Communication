import socket
import Crypt
import GetIP
import sys
import logging as log

log.basicConfig(filename="Client.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

def sendserver():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (GetIP.get_ip_address(), 8080)

    logger.info(GetIP.get_ip_address())

    while 1:                                            #used to wait for the server to resume connection.
        try:
            client_socket.connect(server_address)
            logger.info('Server - Client Connection has Occurred')

            while True:

                message = input("\nEnter a message to send to the server (or '1' to quit): ")
                print(sys.getsizeof(message))
                if sys.getsizeof(message) <= 1024:

                    if message == '1':
                        break

                    logger.info('Sent to Encryption')
                    mes, key = Crypt.encryptm(message.encode())
                    logger.info('The Message is Encrypted')

                    #Sending Data
                    client_socket.send(mes)
                    client_socket.send(key)

                    #Receiving Data
                    response = client_socket.recv(1024)
                    key = client_socket.recv(1024)

                    logger.info(key)
                    response = Crypt.decryptm(response, key)
                    logger.info('Received Response from the Server')
                    print("Server response:", response)

                else:
                    print('The Text Limit is 1024 bytes.')

                #client_socket.connect(server_address)


        except OSError as e:
            print('Connected Loss with Server! Waiting for reconnection')



        except socket.error as e:
            print("Socket error:", e)

        except KeyboardInterrupt:
            print("Client stopped by user!")

        except ConnectionRefusedError as e:
            print('Connection Refused!')

        except ConnectionAbortedError as e:
            print('Connection Aborted!')

        except Exception as e:
            logger.error('Issues in Sending/Receiving the Data')
            print('Exception: ' + str(e))

        finally:
            client_socket.close()
            break


sendserver()