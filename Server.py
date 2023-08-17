import socket
import Crypt
import Write
import GetIP
import logging as log

log.basicConfig(filename="Server.log", format='%(asctime)s %(message)s', filemode='w')
logger = log.getLogger()
logger.setLevel(log.DEBUG)

def main():

    server_address = (GetIP.get_ip_address(), 8080)
    print(GetIP.get_ip_address())
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(server_address)
        server_socket.listen(1)
        logger.info("\nServer has Begun Listening")
        print("Server is listening for connections...")

        client_socket, client_address = server_socket.accept()
        print("Connected by:", client_address)
        logger.info(f'Connection Established by {client_address}')

        while True:
            rec = client_socket.recv(1024)
            key = client_socket.recv(1024)
            logger.info(f'Key: {key}')
            #print(key)

            data = Crypt.decryptm(rec, key)
            Write.intotxt(data)
            if not data:
                break
            print("\nReceived:", data)

            response = data

            response,key = Crypt.encryptm(response.encode())
            client_socket.send(response)
            client_socket.send(key)

    except socket.error as e:
        print("Socket error:", e)
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print('Exception: '+ str(e))
    finally:
        if 'client_socket' in locals():
            client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
