from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
from sqlalchemy.exc import NoResultFound
from database import get_session_maker
from database.entities import User
from werkzeug.security import generate_password_hash, check_password_hash

LOCALHOST = "77.246.102.127"
PORT = 1488

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

session_maker = get_session_maker("sqlite:///./data.sqlite")

server.bind((LOCALHOST, PORT))
print("Server was started")

is_running = True
clients = {}

class ClientThread(threading.Thread):
    def __init__(self, clientsocket, clientaddress):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.username = None
        print("New connection: ", clientaddress)

    def run(self):
        try:
            self.handle_auth()
            self.listen_for_messages()
        except ConnectionError:
            print("Connection closed abruptly.")
        finally:
            if self.username in clients:
                del clients[self.username]
            self.csocket.close()

    def handle_auth(self):
        session = session_maker()
        try:
            while True:
                self.csocket.sendall(b"Do you want to register or login? (r/l): ")
                choice = self.csocket.recv(1024).decode().strip()

                if choice == 'r':
                    self.csocket.sendall(b"Enter username: ")
                    username = self.csocket.recv(1024).decode().strip()

                    self.csocket.sendall(b"Enter password: ")
                    password = self.csocket.recv(1024).decode().strip()

                    hashed_password = generate_password_hash(password)

                    user = session.query(User).filter_by(username=username).first()
                    if user:
                        self.csocket.sendall(b"Username already exists. Try again.\n")
                    else:
                        new_user = User(username=username, password=hashed_password)
                        session.add(new_user)
                        session.commit()
                        self.csocket.sendall(b"Registration successful.\n")
                        self.username = username
                        clients[self.username] = self.csocket
                        break

                elif choice == 'l':
                    self.csocket.sendall(b"Enter username: ")
                    username = self.csocket.recv(1024).decode().strip()

                    self.csocket.sendall(b"Enter password: ")
                    password = self.csocket.recv(1024).decode().strip()

                    try:
                        user = session.query(User).filter_by(username=username).one()
                        if check_password_hash(user.password, password):
                            self.csocket.sendall(b"Login successful.\n")
                            self.username = username
                            clients[self.username] = self.csocket
                            break
                        else:
                            self.csocket.sendall(b"Invalid password. Try again.\n")
                    except NoResultFound:
                        self.csocket.sendall(b"Username not found. Try again.\n")
        finally:
            session.close()

    def listen_for_messages(self):
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()

            if msg == 'exit':
                print(f"{self.username} disconnected.")
                break
            elif msg.startswith("@"):
                recipient, message = msg[1:].split(" ", 1)
                if recipient in clients:
                    recipient_socket = clients[recipient]
                    recipient_socket.sendall(bytes(f"{self.username}: {message}", "UTF-8"))
                else:
                    self.csocket.sendall(b"User not found.\n")
            else:
                response = f"{self.username}: {msg}"
                print(response)
                self.csocket.sendall(bytes(response, "UTF-8"))

def stop_server():
    global is_running
    is_running = False
    for client_socket in clients.values():
        client_socket.sendall(b"Server is shutting down.")
        client_socket.close()
    exit()

while is_running:
    try:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientsock, clientAddress)
        newthread.start()
    except KeyboardInterrupt:
        stop_server()
