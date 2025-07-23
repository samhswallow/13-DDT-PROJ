import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import register 

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
        except Exception as e:
            messagebox.showerror("Error", f"Could not read users.txt:\n{e}")
            return

        if not (teacher_var.get() or student_var.get()):
            messagebox.showerror("Error", "Please select Teacher or Student")
            return

        if password_check:

            if teacher_var.get():
            
               subprocess.run([sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/teachermain.py"])
            else:
               
                subprocess.run([sys.executable, "/Users/samswallow/Desktop/13_ddt_proj/the files/studentmain.py"])
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