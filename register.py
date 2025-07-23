import tkinter as tk
from tkinter import messagebox
global register

def register(root):
    def save_password():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password can't be empty.")
            return

        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")

        messagebox.showinfo("Saved", "User info saved!")
        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x200")

    tk.Label(register_window, text="Enter your username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Enter your password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(register_window, text="Register", command=save_password).pack(pady=10)