import socket, threading
from multiprocessing.connection import Client

from config import Settings

LOCALHOST = Settings.server.LOCALHOST
PORT = Settings.server.PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((LOCALHOST, PORT))
print("Server was started")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientsock, clientAddress)

