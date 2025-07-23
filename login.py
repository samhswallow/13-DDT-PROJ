import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import register 
from tkinter import *
import sqlite3

def login(root, on_success):
    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        password_check = False

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
           password_check = True
        else:
            messagebox.showerror("Error", "Invalid username or password.")

        if password_check:
            if teacher_var.get():
                subprocess.run([sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/teachermain.py"])
                login_window.destroy()
            else:
                subprocess.run([sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py"])
                login_window.destroy()
        else:
            messagebox.showerror("Login Denied", "Incorrect username or password")

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

    teacher_var = tk.IntVar()
    student_var = tk.IntVar()

    teacher_option = tk.Checkbutton(login_window, text="Teacher", variable=teacher_var)
    teacher_option.pack(pady=5)

    student_option = tk.Checkbutton(login_window, text="Student", variable=student_var)
    student_option.pack(pady=5)

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
    login(root, on_success)
    root.mainloop()