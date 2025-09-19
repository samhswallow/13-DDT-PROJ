import tkinter as tk  # Main GUI library
from tkinter import messagebox  # Popup dialogs
from PIL import ImageTk, Image  # Handle images in Tkinter
import socket  # Networking
import threading  # Run tasks in background
from tkinter import ttk  # Themed Tkinter widgets
from datetime import datetime  # Date and time functions
import os  # OS-level functions
import subprocess  # Run external programs
import sys  # System-level access

scan_window = None  # Track single scan window instance


   
current_url = None  
current_name = None 

scan_process = None

def open_scan_register():
    global scan_process

    # If scan.py is already running, just bring its window to front (cannot do easily across processes)
    if scan_process and scan_process.poll() is None:
        messagebox.showinfo("Scan Window", "Scan window is already running!")
        return

    # Launch scan.py as a separate Python process
    scan_process = subprocess.Popen([
        sys.executable,  # Path to current Python interpreter
        "/Users/samswallow/Desktop/13_ddt_proj/the files/scan.py"  # Path to scan.py
    ])

    

# Connect to main server justo before opening teacher menu.
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
        messagebox.showerror("Error", f"An error occurred: {e}")  # Other socket errors

# Main teacher menu GUI
def gui():  
    teahcer_window = tk.Tk()  
    teahcer_window.title("Teacher Main Menu")  
    teahcer_window.geometry("1600x1000")  
    teahcer_window.configure(bg="black")  

    header_frame = tk.Frame(teahcer_window, bg="#2c3e50", height=60) # Header frame
    header_frame.pack(fill="x")

    # Header labels with initial placeholder text
    # Header labels with initial placeholder text
    greeting_label = tk.Label(header_frame, text="Hello!", bg="#2c3e50", fg="white", font=("Arial", 30))
    greeting_label.pack(side="left", padx=10)  # Pack to left

    time_label = tk.Label(header_frame, text="00:00:00", bg="#2c3e50", fg="white", font=("Arial", 30))
    time_label.pack(side="right", padx=10)  # Pack to right

    # Function to update greeting and time every second
    def update_clock():  
        now = datetime.now()  # Get current time
        hour = now.hour  # Extract hour
        greeting = "Good Morning" if 5 <= hour < 12 else "Good Afternoon" if 12 <= hour < 17 else "Good Evening"
        greeting_label.config(text=greeting)  # Update greeting text
        time_label.config(text=now.strftime("%H:%M:%S"))  # Update clock
        teahcer_window.after(1000, update_clock)  # Repeat every second


    update_clock()  # Start the clock and greeting updates
    scan_students_button = tk.Button(
        teahcer_window,
        text="Scan for Students!",  # Button text
        command=open_scan_register,  # Trigger scan GUI
        font=("Arial", 16)
    )
    scan_students_button.pack(pady=10)  

    teahcer_window.mainloop()  

if __name__ == "__main__": 
    gui()
    








