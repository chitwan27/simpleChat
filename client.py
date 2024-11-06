# client.py
import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext

# Define client parameters
HOST = '127.0.0.1'
PORT = 12345

# Create a secure SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations("cert.pem")

# GUI Class for Tkinter Chat
class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("400x500")

        # Text area for chat messages
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(pady=10)

        # Entry box for sending messages
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack(pady=10)
        self.message_entry.bind("<Return>", self.send_message)

        # Connect to server
        self.client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
        self.client_socket.connect((HOST, PORT))

        # Start a thread to receive messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
            self.display_message(f"You: {message}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message)
                else:
                    break
            except:
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

# Run the chat client
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
