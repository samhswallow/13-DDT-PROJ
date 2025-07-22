import tkinter as tk
from tkinter import messagebox


def savepassword():
 
   username = register_username_entry.get()
   password = register_password_entry.get()
  
   with open("users.txt", "a") as file:
       file.write(f"{username},{password}\n")
  
   messagebox.showinfo("Saved", "User info saved!")
   register_window.destroy()  


def register():
   global register_window, register_username_entry, register_password_entry
  
   register_window = tk.Toplevel(root)
   register_window.title("Register")
   register_window.geometry("300x200")


   username_label = tk.Label(register_window, text="Enter your username:")
   password_label = tk.Label(register_window, text="Enter your password:")


   register_username_entry = tk.Entry(register_window)
   register_password_entry = tk.Entry(register_window, show="*")  
  
   save_button = tk.Button(register_window, text="Register", command=savepassword)


   username_label.pack(pady=5)
   register_username_entry.pack(pady=5)
   password_label.pack(pady=5)
   register_password_entry.pack(pady=5)
   save_button.pack(pady=10)


root = tk.Tk()
root.title("Login Window")
root.geometry("300x200")


username_label = tk.Label(root, text="Enter your username:")
password_label = tk.Label(root, text="Enter your password:")


username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")


login_button = tk.Button(root, text="Login", command=lambda: print("Login pressed"))
register_button = tk.Button(root, text="Register", command=register)


username_label.pack(pady=5)
username_entry.pack(pady=5)
password_label.pack(pady=5)
password_entry.pack(pady=5)
login_button.pack(pady=5)
register_button.pack(pady=5)


root.mainloop()
