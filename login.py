import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import register 
from tkinter import *
import sqlite3
import socket

def get_local_ip():
    global temp_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        temp_ip = s.getsockname()[0]
        s.close()
        return temp_ip
    except Exception as e:
        return f"Error getting IP: {e}"
    
def check_credentials():
    get_local_ip()
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in username and password.")
        return

    
    login_data = f"LOGIN,{username},{password},{temp_ip}"

    try:
        print(login_data)
        server_ip = "127.0.0.1" 
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.sendall(login_data.encode('utf-8'))

            response = client_socket.recv(1024).decode('utf-8')
            if response.startswith("SUCCESS"):
                subprocess.run([sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py"])
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", response)

    except Exception as e:
        messagebox.showerror("Network Error", f"Could not connect to server: {e}")


def login(): 
    global username_entry
    global password_entry
    global login_window

    login_window = tk.Toplevel(root)
    login_window.title("Login Window")
    login_window.geometry("300x250")

    username_label = tk.Label(login_window, text="Enter your username:")
    username_label.pack(pady=5)

    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Enter your password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    login_button.pack(pady=10)

    register_button = tk.Button(login_window, text="Register", command=lambda: register.register(root))
    register_button.pack(pady=5)

if __name__ == "__main__":
    def on_success(role):
        import tkinter.messagebox as mb
        mb.showinfo("Logged in as", role)

    root = tk.Tk()
    root.withdraw()
    login()
    root.mainloop()
