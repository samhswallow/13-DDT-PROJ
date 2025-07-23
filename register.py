import tkinter as tk
from tkinter import messagebox
import sqlite3
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Error getting IP: {e}"

def save_password():
    username = username_entry.get()
    password = password_entry.get()
    surname = surname_entry.get()
    formclass = formclass_entry.get()
    name = name_entry.get()

    if not username or not password or not surname or not formclass or not name:
        messagebox.showerror("Error", "You did not fill all inputs.")
        return

    
    ip = get_local_ip()
    print("Local IP Address:", ip)

   
    try:
        global conn
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        name TEXT,
        surname TEXT,
        form_class TEXT,
        password TEXT,
        ip TEXT
    )
""")

        cursor.execute("""
            INSERT INTO users (username, name, surname, form_class, password, ip)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, name, surname, formclass, password, ip))
        conn.commit()

        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        conn.close()

def register(root):
    global username_entry, password_entry, surname_entry, formclass_entry, name_entry, register_window

    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("300x350")

    tk.Label(register_window, text="Enter your username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Enter your name:").pack(pady=5)
    name_entry = tk.Entry(register_window)
    name_entry.pack(pady=5)

    tk.Label(register_window, text="Enter your surname:").pack(pady=5)
    surname_entry = tk.Entry(register_window)
    surname_entry.pack(pady=5)

    tk.Label(register_window, text="Enter your form class:").pack(pady=5)
    formclass_entry = tk.Entry(register_window)
    formclass_entry.pack(pady=5)

    tk.Label(register_window, text="Enter your password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(register_window, text="Register", command=save_password).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    register(root)
    root.mainloop()