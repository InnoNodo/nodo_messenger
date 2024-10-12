import socket
import threading

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

is_running = True
clients = []

class ClientThread(threading.Thread):
    def __init__(self, clientsocket, clientaddress):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        clients.append(clientsocket)
        print("New connection: ", clientaddress)

    def run(self):
        msg = ''
        try:
            while True:
                data = self.csocket.recv(4096)
                msg = data.decode()
                if not data:
                    break

                if msg == 'exit':
                    print("Client was unconnected")
                    break
                else:
                    print(f"Client says: {msg}")
        except ConnectionError:
            print("Connection closed abruptly.")
        finally:
            clients.remove(self.csocket)
            self.csocket.close()

def broadcast_message():
    while is_running:
        try:
            message = input()
            if message.lower() == 'exit':
                stop_server()
                break
            for client in clients:
                try:
                    client.sendall(bytes(message, 'UTF-8'))
                except ConnectionError:
                    clients.remove(client)
        except KeyboardInterrupt:
            stop_server()
            break

def stop_server():
    global is_running
    is_running = False
    server.close()
    exit()

admin_thread = threading.Thread(target=broadcast_message)
admin_thread.start()

while is_running:
    try:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientsock, clientAddress)
        newthread.start()
    except OSError:
        print("Server stopped listening.")
