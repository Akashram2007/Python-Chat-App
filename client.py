import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

HOST = "127.0.0.1"
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

incoming_messages = []
msg_lock = threading.Lock()

root = tk.Tk()
root.geometry("500x600")
root.title("Chat App")
root.config(bg="#121212")

title = tk.Label(
    root, text="GROUP CHAT",
    font=("sans-serif", 20),
    bg="#270BFF", fg="white"
)
title.pack(fill="x")

main = tk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=10)

# CHAT AREA
chat_area = tk.Frame(main, bg="#2A2A2A")
chat_area.pack(fill="both", expand=True)

chat_display = scrolledtext.ScrolledText(
    chat_area, wrap="word",
    state="disabled",
    font=("Segoe UI", 11)
)
chat_display.pack(fill="both", expand=True, padx=5, pady=5)

chat_display.tag_configure(
    "you",
    background="#1458F7",foreground="white",
    justify="right",
    lmargin1=120, lmargin2=120, rmargin=10
)

chat_display.tag_configure(
    "other",
    background="white",foreground="black",
    justify="left",
    lmargin1=10, lmargin2=10, rmargin=120
)

chat_input = tk.Frame(chat_area)
chat_input.pack(fill="x")

text_input = tk.Entry(chat_input, font=("sans-serif", 14))
text_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)

def send_msg(event=None):
    msg = text_input.get().strip()
    if msg:
        client.send(msg.encode())

        chat_display.config(state="normal")
        chat_display.insert("end", msg + "\n", "you")
        chat_display.config(state="disabled")
        chat_display.see("end")

        text_input.delete(0, "end")

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode()
            with msg_lock:
                incoming_messages.append(msg)
        except:
            break

def update_chat():
    with msg_lock:
        while incoming_messages:
            msg = incoming_messages.pop(0)
            chat_display.config(state="normal")
            chat_display.insert("end", msg + "\n", "other")
            chat_display.config(state="disabled")
            chat_display.see("end")

    root.after(100, update_chat)

threading.Thread(target=receive_messages, daemon=True).start()
update_chat()

send_button = tk.Button(
    chat_input, text="Send",
    bg="#2B00FF", fg="white",
    command=send_msg
)
send_button.pack(side="right", padx=5, pady=5)

text_input.bind("<Return>", send_msg)

root.mainloop()