"""This script handles the login system. I collec the user data before sending
it to the server for processesing. Once the server sends back a result the 
script denies or accept the login. """

# Run external scripts
import subprocess
# System functions for running studentmain
import sys
# Networking
import socket
# GUI
import tkinter as tk
# Popups
from tkinter import messagebox
# Images in Tkinter
from PIL import Image, ImageTk
# Registration window module
import register

register_window = None
temp_ip = None

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
                
                login_window.after( 100, 
                    subprocess.Popen( 
                        [
                            sys.executable,
                            "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py",
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
        register_window.lift()  # Bring it to front
        return

    register_window = register.register_gui(login_window)

    # Check if the registration window exists (is currently open)
    register_window.protocol(
        # Set a custom action for when the window's close button is clicked
        "WM_DELETE_WINDOW", 
        lambda: (
            # Close the window and free its resources
            register_window.destroy(), 
             # Reset the global variable so Python knows the window is closed 
            globals().__setitem__("register_window", None),
        ),
    )


def gui():
    """Handels the login GUI"""
    global username_entry, password_entry, login_window

    login_window = tk.Tk()
    login_window.title("Login Window")
    login_window.geometry("600x440")
    login_window.configure(bg="#333333")

    frame = tk.Frame(login_window, bg="#333333")

    # Logo button
    img = Image.open(
        "/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png"
    )
    width = 300

    # Best proportional relationship
    aspect_ratio = img.height / img.width  

     # Calculate height based on aspect ratio
    height = int(width * aspect_ratio)  
    
    # Resize image to fit nicely in the window
    img = img.resize((width, height))      

    # Convert to PhotoImage for Tkinter
    login_img = ImageTk.PhotoImage(img)    

    login_label = tk.Label(frame, image=login_img, bg="#333333", borderwidth=0)

    # Keep reference to avoid garbage collection
    login_label.image = login_img  

    # Username input
    username_label = tk.Label(
        frame, text="Username", bg="#333333", fg="#FFFFFF", font=("Arial", 16)
    )
    username_entry = tk.Entry(
        frame, font=("Arial", 16), bg="white",
        highlightbackground="black", highlightcolor="black"
    )

    # Password input
    password_label = tk.Label(
        frame, text="Password", bg="#333333", fg="#FFFFFF", font=("Arial", 16)
    )
    password_entry = tk.Entry(
        frame, show="*", font=("Arial", 16), bg="white",
        highlightbackground="black", highlightcolor="black"
    )

    # Buttons
    login_button = tk.Button(
        frame, text="Login", bg="#333333", fg="black",
        font=("Arial", 16), command=check_credentials
    )
    register_button = tk.Button(
        frame, text="Register", bg="#333333", fg="black",
        font=("Arial", 16), command=open_register
    )

    # Layout
    login_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    username_label.grid(row=1, column=0, sticky="e", padx=10)
    username_entry.grid(row=1, column=1, sticky="w", pady=10, padx=10)
    password_label.grid(row=2, column=0, sticky="e", padx=10)
    password_entry.grid(row=2, column=1, sticky="w", pady=10, padx=10)
    login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), ipadx=30)
    register_button.grid(row=4, column=0, columnspan=2, pady=(0, 20), ipadx=20)

    frame.pack(expand=True)

if __name__ == "__main__":
    gui()
    login_window.mainloop()



