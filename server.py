import socket, threading
from multiprocessing.connection import Client

from config import Settings

LOCALHOST = Settings.server.LOCALHOST
PORT = Settings.server.PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((LOCALHOST, PORT))
print("Server was started")


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("Новое подключение: ", clientAddress)

    def run(self):
        print("Подключение с клиента : ", clientAddress)

        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()
            print(msg)

            if msg == '':
                print("Отключение")
                break

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientsock, clientAddress)

