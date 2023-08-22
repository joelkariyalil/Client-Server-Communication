# Client-Server-Communication

How to run the code.

Server
> python "Server-Client Communication.py" --role Server
> python "Server-Client Communication.py" --role server

Client
> python "Server-Client Communication.py" --role client
> python "Server-Client Communication.py" --role Client

Run the Server in the Background

> nohup python "Server-Client Communication.py" --role Server


Features of this Code

> Supports Inter-Network Communication (All the Subnets are scanned for a connection) - Threading used for faster surfing
> Data is Encrypted and Decrypted using Fernet Cryptography method
> Files of any size (.txt files) can be sent by copying the link into the terminal.
> The server can run in the background.
> IP Configuration isn't required.
> Extensive Logging has been used.
> Server appends the messages in a Notepad file.
> Diagrammtic display of File sharing percentages (python tqdm module)
