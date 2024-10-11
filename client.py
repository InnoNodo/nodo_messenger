import socket
import threading

from config import Settings

SERVER = Settings().server.LOCALHOST
PORT = Settings().server.PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("Hello", "UTF-8"))