import socket
import tkinter as tk
from tkinter import messagebox

def get_online_users():
    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall("SCAN_NETWORK".encode())
            response = s.recv(4096).decode("utf-8")
            return response
    except Exception as e:
        return f"Error: {e}"

def show_online_users():
    users = get_online_users()
    messagebox.showinfo("Online Users", users)

def main_gui():
    root = tk.Tk()
    root.title("Scan Network - Online Users")
    root.geometry("400x200")

    scan_button = tk.Button(root, text="Scan Network", command=show_online_users, font=("Arial", 14))
    scan_button.pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    main_gui()