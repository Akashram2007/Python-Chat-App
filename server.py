import socket
import threading

HOST = "127.0.0.1"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            client.send(msg)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            clients.remove(client)
            client.close()
            break

print("Server running...")
while True:
    client, addr = server.accept()
    clients.append(client)
    threading.Thread(target=handle_client, args=(client,), daemon=True).start()