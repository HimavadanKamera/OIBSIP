import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

name = input("Enter your name: ")

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print("\n" + message)
        except:
            print("Disconnected from server.")
            client.close()
            break

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

while True:
    msg = input()

    if msg.lower() == "exit":
        client.send(f"{name} left the chat.".encode())
        client.close()
        break

    client.send(f"{name}: {msg}".encode())