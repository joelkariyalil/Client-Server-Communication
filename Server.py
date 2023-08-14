import socket
import Crypt
import Write

def main():
    server_address = ('localhost', 8080)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Server is listening for connections...")
        
        client_socket, client_address = server_socket.accept()
        print("Connected by:", client_address)
        
        while True:
            data = client_socket.recv(1024)
            data = Crypt.decryptm(data)
            Write.intotxt(data)
            if not data:
                break
            print("Received:", data)
            response = "Server received: " + data
            response=Crypt.encryptm(response)
            client_socket.send(response)
            
    except socket.error as e:
        print("Socket error:", e)
    except KeyboardInterrupt:
        print("Server stopped by user.")
    finally:
        if 'client_socket' in locals():
            client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
