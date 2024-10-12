import socket, threading

from config import Settings
from database import get_session_maker

settings = Settings()

LOCALHOST = settings.server.LOCALHOST
PORT = settings.server.PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

session_maker = get_session_maker(settings.database.connection_string)

server.bind((LOCALHOST, PORT))
print("Server was started")

class ClientThread(threading.Thread):
    def __init__(self, clientsocket, clientaddress):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection: ", clientaddress)

    def run(self):
        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()
            print(msg)

            if msg == 'exit':
                print("Unconnection")
                break

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientsock, clientAddress)
    newthread.run()

