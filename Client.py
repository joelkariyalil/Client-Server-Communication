import socket
import Crypt
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)

    try:
        client_socket.connect(server_address)
        
        while True:
            message = input("\nEnter a message to send to the server (or '1' to quit): ")
            if message == '1':
                break
            message = Crypt.encryptm(message)
            client_socket.send(message)

            response = client_socket.recv(1024)
            response = Crypt.decryptm(response)
            print("Server response:", response)
            
    except socket.error as e:
        print("Socket error:", e)
    except KeyboardInterrupt:
        print("Client stopped by user.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
