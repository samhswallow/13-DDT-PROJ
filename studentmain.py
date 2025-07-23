import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket
from lockedbrowser import launch_browser
from tkinter import ttk
from datetime import datetime

global url
url = None
button_frame = None  


def create_tab():

    if url:
        launch_browser(url)
    else:
        messagebox.showerror("Error", "No URL to launch.")


def establish_connection():
    global url, button_frame
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("172.20.10.2", 6060))  
        url = s.recv(2048).decode("utf-8")
        print(f"Message received: {url}")

       
        authorised_link_button = tk.Button(
            button_frame,
            text="Open Link",
            command=create_tab,
            font=("Arial", 14)
        )
        authorised_link_button.pack(pady=10)

        messagebox.showinfo("Server Message", url)
        s.close()

    except ConnectionRefusedError:
        messagebox.showerror(
            "Connection Error",
            "No server running on this IP and port.\nPlease start the server first."
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def student_menu():
    global student_window, button_frame
    student_window = tk.Tk()
    student_window.title("Student Menu")
    student_window.geometry("1600x1000")
    student_window.configure(bg="black")

   
    header_frame = tk.Frame(student_window, bg="green", height=60)
    header_frame.pack(fill="x")

    greeting_label = tk.Label(header_frame, text="", bg="green", fg="white", font=("Arial", 30))
    greeting_label.pack(side="left", padx=10)

    time_label = tk.Label(header_frame, text="", bg="green", fg="white", font=("Arial", 30))
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

        student_window.after(100, update_clock)  

    update_clock()
    establish_connection_button = tk.Button(
        button_frame,
        text="Establish Connection",
        command=establish_connection,
        font=("Arial", 16)
    )
    establish_connection_button.pack()

    student_window.mainloop()


if __name__ == "__main__":
    student_menu()