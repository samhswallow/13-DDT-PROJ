import tkinter as tk  # GUI.
from tkinter import messagebox  # Popups.
import subprocess  # Run external scripts.
import sys  # System functions for running studentmain.
import register  # Registration window module.
import socket  # Networking.
from PIL import Image, ImageTk  # Images in Tkinter.
import subprocess
import register

register_window = None

register_window = None  # Single registration window.
temp_ip = None  # Local IP.

 # This function gets the local IP address of the machine.
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

# This function sends the users login inputs to server. I handle this through a sever, my program can allow mutiple users. 
def check_credentials(): 
    get_local_ip()
    username = username_entry.get() # Grab the username and password.
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please fill in username and password.")
        return
    login_data = f"LOGIN,{username},{password}" # Send a login request to the server, 
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.sendall(login_data.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            if response.startswith("SUCCESS"): # If login is successful, close the login window and open the main student window.
                login_window.destroy()
                login_window.after(100, lambda: subprocess.Popen(
                    [sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py"])) # Run studentmain.py.
            else:
                messagebox.showerror("Login Failed", response)
    except Exception as e:
        messagebox.showerror("Network Error", f"Could not connect to server: {e}")

# This function opens the registration window.
def open_register():
    global register_window
    if register_window and register_window.winfo_exists():
        register_window.lift()  # Bring it to front
        return
    register_window = register.register_gui(login_window)
    if register_window:
        register_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: (register_window.destroy(), globals().__setitem__("register_window", None))
        )
    

# This function creates the login GUI.
def gui():
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("Login Window")
    login_window.geometry("600x440")
    login_window.configure(bg="#333333")

    frame = tk.Frame(login_window, bg='#333333')

    # Logo button
    img = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png")
    width = 300
    aspect_ratio = img.height / img.width # Best proportional relationshop.
    height = int(width * aspect_ratio) # Calculate height based on aspect ratio.
    img = img.resize((width, height)) # Resize image to fit nicely in the window.
    login_img = ImageTk.PhotoImage(img) # Convert to PhotoImage for Tkinter.

    login_label = tk.Label(frame, image=login_img, bg='#333333', borderwidth=0)
    login_label.image = login_img  # keep reference to avoid garbage collection

    username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_entry = tk.Entry(frame, font=("Arial", 16), bg="white", highlightbackground="black", highlightcolor="black")

    password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 16), bg="white", highlightbackground="black", highlightcolor="black")

    login_button = tk.Button(frame, text="Login", bg="#333333", fg="black", font=("Arial", 16), command=check_credentials)
    register_button = tk.Button(frame, text="Register", bg="#333333", fg="black", font=("Arial", 16), command=open_register)

    login_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))  # Place logo at top spanning two columns with padding
    frame.grid_columnconfigure(0, weight=1)  # Allow first column to expand equally
    frame.grid_columnconfigure(1, weight=1)  # Allow second column to expand equally
    username_label.grid(row=1, column=0, sticky="e", padx=10)  # Username label left column aligned right
    username_entry.grid(row=1, column=1, sticky="w", pady=10, padx=10)  # Username input right column aligned left
    password_label.grid(row=2, column=0, sticky="e", padx=10)  # Password label left column aligned right
    password_entry.grid(row=2, column=1, sticky="w", pady=10, padx=10)  # Password input right column aligned left
    login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), ipadx=30)  # Login button across two columns with padding
    register_button.grid(row=4, column=0, columnspan=2, pady=(0, 20), ipadx=20)  # Register button across two columns with bottom padding


    frame.pack(expand=True)


if __name__ == "__main__":
    gui()  
    login_window.mainloop()  




