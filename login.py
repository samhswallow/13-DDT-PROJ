import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import register 
from tkinter import *
import sqlite3
import socket
from PIL import Image, ImageTk
register_window = None

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
                login_window.destroy() 
                login_window.after(100, lambda: subprocess.Popen(
        [sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py"]))
                      
            else:
                messagebox.showerror("Login Failed", response)

    except Exception as e:
        messagebox.showerror("Network Error", f"Could not connect to server: {e}")



def open_register():
    global register_window

    if register_window and register_window.winfo_exists():
        register_window.lift()
        return

    register_window = register.register(root)

    if register_window:
        register_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: (register_window.destroy(), globals().__setitem__("register_window", None)),
        )


def login(): 
    import tkinter as tk
    from PIL import Image, ImageTk

    global username_entry
    global password_entry
    global login_window

    login_window = tk.Toplevel(root)
    login_window.title("Login Window")
    login_window.geometry("600x440")
    login_window.configure(bg="#333333")

    frame = tk.Frame(login_window, bg='#333333')  

    
    img = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png")
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)

    img = img.resize((width, height))
    login_img = ImageTk.PhotoImage(img)

    login_label = tk.Label(frame, image=login_img, bg='#333333', borderwidth=0)
    login_label.image = login_img  

    
    username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_entry = tk.Entry(frame, font=("Arial", 16), bg="white", highlightbackground="black", highlightcolor="black")

    password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 16), bg="white", highlightbackground="black", highlightcolor="black")

   
    login_button = tk.Button(frame, text="Login", bg="#333333", fg="black", font=("Arial", 16), command=check_credentials)
    register_button = tk.Button(frame, text="Register", bg="#333333", fg="black", font=("Arial", 16), command=open_register)

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
    def on_success(role):
        import tkinter.messagebox as mb
        mb.showinfo("Logged in as", role)

    root = tk.Tk()
    root.withdraw()
    login()
    root.mainloop()
