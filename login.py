import tkinter as tk
import register
from tkinter import messagebox


def login(root, on_success): 
    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        password_check = False

        try:
            with open("users.txt", "r") as file:
                for line in file:
                    if line.strip() == f"{username},{password}":
                        password_check = True
                        break
        except:
            messagebox.showerror("Error", "Could not read users.txt")
            return

        if password_check:
            messagebox.showinfo("Login Approved", "Approved!")
            login_window.destroy()
            on_success()  
        else:
            messagebox.showerror("Login Denied", "Incorrect username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Login Window")
    login_window.geometry("300x200")

    username_label = tk.Label(login_window, text="Enter your username:")
    username_entry = tk.Entry(login_window)

    password_label = tk.Label(login_window, text="Enter your password:")
    password_entry = tk.Entry(login_window, show="*")

    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    register_button = tk.Button(login_window, text="Register", command=lambda: register.register(root))

    teacher_option = tk.Checkbutton(login_window, text ="teacher")
    student_option = tk.Checkbutton(login_window, text ="student")

    username_label.pack(pady=5)
    username_entry.pack(pady=5)
    password_label.pack(pady=5)
    password_entry.pack(pady=5)
    teacher_option.pack(pady=5)
    student_option.pack(pady=5)
    register_button.pack(pady=5)
    login_button.pack(pady=10)