import tkinter as tk
from tkinter import messagebox

def login():
    username = name_userentry.get()
    password = password_userentry.get()
    if username == "admin" and password == "1234":
        messagebox.showinfo("Login Successful", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")
        
def register():
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x200")
    registerusername_label = tk.Label(root, text="Enter your username:")
    registerpassword_label = tk.Label(root, text="Enter your password:")
    
    register_userentry = tk.Entry(root) 
    registerpassword_entry = tk.Entry(root)
    register_button = tk.Button(root, text="Save")
    registerusername_label.pack(pady=5)
    registerpassword_label.pack(pady=5)
    register_userentry.pack(pady=5)
    registerpassword_entry.pack(pady=5)

root = tk.Tk()
root.title("Login Window")
root.geometry("300x200")

username_label = tk.Label(root, text="Enter your username:")
name_userentry = tk.Entry(root)
password_label = tk.Label(root, text="Enter your password:")
password_userentry = tk.Entry(root, show="*")  
login_button = tk.Button(root, text="Login", command=login)
register_button = tk.Button(root, text="Register", command=register)

username_label.pack(pady=5)
name_userentry.pack(pady=5)
password_label.pack(pady=5)
password_userentry.pack(pady=5)
login_button.pack(pady=5)
register_button.pack(pady=5)

root.mainloop()
