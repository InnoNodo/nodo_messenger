import socket
from threading import Thread

from config import Settings

SERVER = Settings().server.LOCALHOST
PORT = Settings().server.PORT

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
print("You succesfully connected to the server")

def task():
    while True:
        try:
            in_data = client.recv(4096)
            if not in_data:
                print("Connection closed by the server.")
                break
            print("From server: ", in_data.decode())
        except ConnectionError:
            break

def task2():
    while True:
        out_data = input()
        if out_data == 'exit':
            client.sendall(bytes(out_data, 'UTF-8'))
            client.close()
            break
        client.sendall(bytes(out_data, 'UTF-8'))

t1 = Thread(target=task2)
t2 = Thread(target=task)

t1.start()
t2.start()

t1.join()
t2.join()
