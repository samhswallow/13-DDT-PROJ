import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import subprocess
import login
 
url_list = []
name_list = []

def create_tab():
    create_tab_window = tk.Toplevel(root)
    create_tab_window.title("Create Tab")
    create_tab_window.geometry("300x250")

    create_tab_label = tk.Label(create_tab_window, text="Enter URL")
    create_tab_entry = tk.Entry(create_tab_window)

    create_tab_label_name = tk.Label(create_tab_window, text="Enter URL's name")
    create_tab_label_entry = tk.Entry(create_tab_window)

    def save_tab():
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

    create_tab_label.pack(pady=(10, 0))
    create_tab_entry.pack(pady=(0, 10))
    create_tab_label_name.pack(pady=(10, 0))
    create_tab_label_entry.pack(pady=(0, 10))
    save_tab_button.pack()

def main_menu():
    global main_window
    main_window = tk.Toplevel(root)
    main_window.title("Main Menu")
    main_window.geometry("1600x1000")
    main_window.configure(bg="black")

    green_photo = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/greensquare.png")
    resized_photo = green_photo.resize((1500, 900))
    green_background = ImageTk.PhotoImage(resized_photo)
    green_background_label = tk.Label(main_window, image=green_background, bg="black")
    green_background_label.place(x=20, y=20)

    create_link = tk.Button(main_window, text="Create Link", command=create_tab, font=("Arial", 16))
    create_link.place(x=700, y=850)

    main_window.green_background = green_background  

root = tk.Tk()
root.withdraw()  
login.login(root, main_menu)

root.mainloop()