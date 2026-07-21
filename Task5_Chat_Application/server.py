import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

print(f"Server started on {HOST}:{PORT}")

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            time = datetime.now().strftime("%H:%M")

            final_message = f"[{time}] {message.decode()}"

            print(final_message)

            broadcast(final_message.encode(), client)

        except:
            break

    print("A client disconnected.")
    if client in clients:
        clients.remove(client)
    client.close()

while True:
    client, address = server.accept()

    print(f"Connected with {address}")

    clients.append(client)

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()