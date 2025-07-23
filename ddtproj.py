import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import subprocess


url_list = []
name_list = []


def login_process():
   username = username_entry.get()
   password = password_entry.get()
   password__check = False


   try:
       with open("users.txt", "r") as file:
           for line in file:
               if line.strip() == f"{username},{password}":
                   password_check = True
                   break
   except:
       messagebox.showerror("Error")
       return


   if password_check:
       main_menu()
       messagebox.showinfo("Login Approved", "Approved")
   else:
       messagebox.showerror("Login Denied")




def save_password():
   username = register_username_entry.get()
   password = register_password_entry.get()


   if not username or not password:
       messagebox.showerror("Error", "Username and password can't be empty.")
       return


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


   save_button = tk.Button(register_window, text="Register", command=save_password)


   username_label.pack(pady=5)
   register_username_entry.pack(pady=5)
   password_label.pack(pady=5)
   register_password_entry.pack(pady=5)
   save_button.pack(pady=10)
  
def create_tab():
   create_tab_window = tk.Toplevel(root)
   create_tab_window.title("Create Tab")
   create_tab_window.geometry("300x250")


   create_tab_label = tk.Label(create_tab_window, text="Enter URL")
   create_tab_entry = tk.Entry(create_tab_window)


   create_tab_label_name = tk.Label(create_tab_window, text="Enter URL's name")
   create_tab_label_entry = tk.Entry(create_tab_window)


   create_tab_label.pack(pady=(10, 0))
   create_tab_entry.pack(pady=(0, 10))
   create_tab_label_name.pack(pady=(10, 0))
   create_tab_label_entry.pack(pady=(0, 10))


   def save_tab():
       global url
       url = create_tab_entry.get()
       name = create_tab_label_entry.get()


       if url and name:
           url_list.append(url)
           name_list.append(name)
           messagebox.showinfo("Success", f"Saved tab '{name}'")


           def open_tab():
               from lockedbrowser import launch_browser
               launch_browser(url)


           authorised_link_button = tk.Button(main_window, text=name, command=open_tab, font=("Arial", 14))
           authorised_link_button.pack(pady=10)
       else:
           messagebox.showerror("Error", "Both fields are required")


   save_tab_button = tk.Button(create_tab_window, text="Save", command=save_tab, font=("Arial", 14))
   save_tab_button.pack(pady=10)







   create_tab_label.pack(pady=(10, 0))
   create_tab_entry.pack(pady=(0, 10))
   create_tab_label_name.pack(pady=(10, 0))
   create_tab_label_entry.pack(pady=(0, 10))
   save_tab_button.pack()
  


def main_menu():
   global main_window
   main_window = tk.Toplevel(root)
   main_window.title("Register")
   main_window.geometry("1600x1000")
   main_window.configure(bg="black")


 
   green_photo = Image.open("/Users/samswallow/Desktop/greensquare.png")
   resized_photo = green_photo.resize((1500, 900))
   green_background = ImageTk.PhotoImage(resized_photo)
   green_background_label = tk.Label(main_window, image=green_background, bg="black")
   green_background_label.place(x = 20, y=20)


   create_link = tk.Button(main_window, text = "Create Link", command = create_tab, font = ("Arial", 16))
   create_link.place(x= 700,y= 850)
  
   main_window.green_background = green_background




root = tk.Tk()
root.title("Login Window")
root.geometry("300x200")


username_label = tk.Label(root, text="Enter your username:")
password_label = tk.Label(root, text="Enter your password:")


username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")


login_button = tk.Button(root, text="Login", command=login_process)
register_button = tk.Button(root, text="Register", command=register)


username_label.pack(pady=5)
username_entry.pack(pady=5)
password_label.pack(pady=5)
password_entry.pack(pady=5)
login_button.pack(pady=5)
register_button.pack(pady=5)


root.mainloop()