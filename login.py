"""This script handles the login system backend: networking, IP retrieval,
sending/receiving data from the server, and opening the registration window."""

# Run external scripts
import subprocess

# System functions for running studentmain
import sys

# Networking
import socket

# Popups
from tkinter import messagebox

# Registration window module
import register

# Global placeholders for GUI elements (set by login_gui.py)
register_window = None
temp_ip = None
login_window = None
username_entry = None
password_entry = None

def on_close_register():
    """Handle the register window being closed."""
    global register_window
    register_window.destroy()
    register_window = None


def get_local_ip():
    """Get the local IP address of the machine.

    Tries to connect to an external server to determine
    the outgoing IP. Shows an error message if connection fails.
    """
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
    """Handle user login info and send it to the server."""
    get_local_ip()

    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror(
            "Error", "Please fill in username and password."
        )
        return

    # Send a login request to the server
    login_data = f"LOGIN,{username},{password}"

    try:
        server_ip = "172.20.10.3"
        server_port = 6060

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.sendall(login_data.encode("utf-8"))

            response = client_socket.recv(1024).decode("utf-8")

            # Login successful
            if response.startswith("SUCCESS"):
                
                login_window.after(
                    100,
                    subprocess.Popen(
                        [
                            sys.executable,
                            "/Users/samswallow/Desktop/13_ddt_proj/the files/student_gui.py",
                        ]
                    ),
                )
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", response)

    except Exception as e:
        messagebox.showerror(
            "Network Error", f"Could not connect to server: {e}"
        )


def open_register():
    """Open the registration window if not already open."""
    global register_window

    if register_window and register_window.winfo_exists():

        # Bring it to front
        register_window.lift()  

        return

    register_window = register.register_gui(login_window)

    # Custom close action that also closes register 
    register_window.protocol("WM_DELETE_WINDOW", on_close_register)
