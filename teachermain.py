import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket
import threading
from tkinter import ttk
from datetime import datetime
import scan
import os 
import subprocess
import sys 
scan_window = None

def run_program():
    import scan  
    scan.gui()  
    



current_url = None
current_name = None


def begin_data():
    create_tab_window = tk.Toplevel(main_window)
    create_tab_window.title("Create Tab")
    create_tab_window.geometry("300x250")
    create_tab_window.resizable(False, False)

    create_tab_label = tk.Label(create_tab_window, text="Enter URL")
    create_tab_entry = tk.Entry(create_tab_window)

    create_tab_label_name = tk.Label(create_tab_window, text="Enter URL's name")
    create_tab_label_entry = tk.Entry(create_tab_window)

    def send_data():
        global current_url, current_name
        url = create_tab_entry.get()
        name = create_tab_label_entry.get()

        if url and name:
            current_url = url
            current_name = name
            messagebox.showinfo("Success", f"Saved tab '{name}'")
            create_tab_window.destroy()
        else:
            messagebox.showerror("Error", "Both fields are required")

    save_tab_button = tk.Button(
        create_tab_window,
        text="Save",
        font=("Arial", 14),
        command=send_data
    )

    create_tab_label.pack(pady=(10, 0))
    create_tab_entry.pack(pady=(0, 10))
    create_tab_label_name.pack(pady=(10, 0))
    create_tab_label_entry.pack(pady=(0, 10))
    save_tab_button.pack(pady=10)

def open_scan_register():
    global scan_window

    if scan_window and scan_window.winfo_exists():
        scan_window.lift()
        return

    scan_window = scan.gui(root)

    if  scan_window:
        scan_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: (scan_window.destroy(), globals().__setitem__("scan_window", None)),
        )

def teacher_client():
   
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.17.1.40", 6060))  
       
    except ConnectionRefusedError:
        messagebox.showerror(
            "Connection Error",
            "No server running on this IP and port.\nPlease start the server first."
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



def teacher_menu():
    global main_window
    main_window = tk.Toplevel()
    main_window.title("Teacher Main Menu")
    main_window.geometry("1600x1000")
    main_window.configure(bg="black")

    header_frame = tk.Frame(main_window, bg="#2c3e50", height=60)
    header_frame.pack(fill="x")

    greeting_label = tk.Label(header_frame, text="", bg="#2c3e50", fg="white", font=("Arial", 30))
    greeting_label.pack(side="left", padx=10)

    time_label = tk.Label(header_frame, text="", bg="#2c3e50", fg="white", font=("Arial", 30))
    time_label.pack(side="right", padx=10)

    def update_clock():
        now = datetime.now()
        hour = now.hour
        timestamp = now.strftime(" %H:%M:%S")  

       
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        greeting_label.config(text=greeting)
        time_label.config(text=timestamp)

        main_window.after(100, update_clock)  

    update_clock()  


    scan_students_button = tk.Button(
        main_window,
        text="Scan for Students!",
        command= open_scan_register,
        font=("Arial", 16)
    )
    scan_students_button.pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    teacher_menu()
    root.mainloop()





# def open_tab():
#     from lockedbrowser import launch_browser
#     launch_browser(url)

# authorised_link_button = tk.Button(link_frame, text=name, command=open_tab, font=("Arial", 14))
# authorised_link_button.pack(pady=5)

# else:
#     messagebox.showerror("Error", "Both fields are required")

