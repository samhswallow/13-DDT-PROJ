import tkinter as tk  # For GUI.
from tkinter import messagebox # For alerting the user.
import socket # For connecting to the server.
from PIL import Image, ImageTk # For holding the Logo.
from tkinter import ttk # Using more advanced Tkinter widgets
import threading # To avoid disrupting the mainloop.

register_window = None
user_data = None

# This function collects the user IP so it can store it for the register process. 
def get_local_ip():  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error getting IP: {e}"

# This function sends the users login details to the server.
def send_to_server():
    try:
        server_ip = "172.20.10.3"  
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_ip, server_port))
            client_socket.sendall(user_data.encode('utf-8'))
    except Exception as e: # Error handeling. 
        messagebox.showerror("Network Error", f"Could not send data to server: {e}")

# This function compiles the users data before sending it to the server.
def save_user_data():
    global user_data
    username = username_entry.get()
    password = password_entry.get()
    surname = surname_entry.get()
    formclass = formclass_entry.get()
    name = name_entry.get()

    if not username or not password or not surname or not formclass or not name:
        messagebox.showerror("Error", "You did not fill all inputs.")
        return
    
    if " " in username or " " in surname or " " in formclass or " " in name:
        messagebox.showerror("Error", "Inputs cannot contain spaces.")
        return

    ip = get_local_ip()
    user_data = f"{username},{name},{surname},{formclass},{password},{ip}"
    threading.Thread(target=send_to_server, daemon=True).start()

    messagebox.showinfo("Success", "Registration sent to server!")
    register_window.destroy()

# This function creates a Top Level GUI which can run from login.py.
def register_gui(parent):
    global username_entry, password_entry, surname_entry, formclass_entry, name_entry, register_window

    register_window = tk.Toplevel(parent)
    register_window.title("Register Window")
    register_window.geometry("600x500")
    register_window.configure(bg="#333333")

    frame = tk.Frame(register_window, bg='#333333')

    # Load and resize logo
    img = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png")
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    img = img.resize((width, height))
    login_img = ImageTk.PhotoImage(img)

    logo_label = tk.Label(frame, image=login_img, bg='#333333', borderwidth=0, highlightthickness=0)
    logo_label.image = login_img
    logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    # Username
    username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    username_entry = tk.Entry(frame, font=("Arial", 16), bg="white", fg="black", highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)

    # Name
    name_label = tk.Label(frame, text="Name", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    name_entry = tk.Entry(frame, font=("Arial", 16), bg="white", fg="black", highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)

    # Surname
    surname_label = tk.Label(frame, text="Surname", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    surname_entry = tk.Entry(frame, font=("Arial", 16), bg="white", fg="black",highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)

    # Form Class
    formclass_label = tk.Label(frame, text="Form Class", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    formclass_options = ["9ASID", "9BRQP", "9XZLK", "10QWER", "10PLMK", "11ASDF", "11ZXCV", "12MNOP", "13AUFG", "13JKLH"]
    
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Black.TCombobox", fieldbackground="white", background="white", bordercolor="black", lightcolor="black", darkcolor="black", borderwidth=1,padding=4)
    
    formclass_entry = ttk.Combobox(frame, values=formclass_options, font=("Arial", 16), state="readonly", style="Black.TCombobox")
    formclass_entry.configure(width=17)

    # Password
    password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 16), bg="white", fg="black", highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)

    # Register button
    register_button = tk.Button(frame, text="Register", bg="#FF3399", fg="black", font=("Arial", 16), command=save_user_data)

    # Layout grid
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # This is the grid I use to store inputs into the Register GUI. 
    username_label.grid(row=1, column=0, sticky="e", padx=10) 
    username_entry.grid(row=1, column=1, sticky="w", pady=10, padx=10)

    name_label.grid(row=2, column=0, sticky="e", padx=10)
    name_entry.grid(row=2, column=1, sticky="w", pady=10, padx=10)

    surname_label.grid(row=3, column=0, sticky="e", padx=10)
    surname_entry.grid(row=3, column=1, sticky="w", pady=10, padx=10)

    formclass_label.grid(row=4, column=0, sticky="e", padx=10)
    formclass_entry.grid(row=4, column=1, sticky="w", pady=10, padx=10)

    password_label.grid(row=5, column=0, sticky="e", padx=10)
    password_entry.grid(row=5, column=1, sticky="w", pady=10, padx=10)

    register_button.grid(row=6, column=0, columnspan=2, pady=(20, 20), ipadx=30)

    frame.pack(expand=True)

    return register_window




    



