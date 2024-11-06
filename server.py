# server.py
import socket
import ssl
import threading

# Define server parameters
HOST = '127.0.0.1'  # Localhost for testing
PORT = 12345

# List to keep track of connected clients
clients = []

# Broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:  # Don't send the message back to the sender
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle each client connection
def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break
    print(f"Connection closed from {addr}")
    client_socket.close()
    clients.remove(client_socket)

# Set up the server socket with SSL
def start_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server started on {HOST}:{PORT}")

        with context.wrap_socket(server_socket, server_side=True) as secure_socket:
            while True:
                client_socket, addr = secure_socket.accept()
                clients.append(client_socket)
                threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    start_server()
