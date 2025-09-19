"""This code is the simple teacher GUI which is acts as the home page for the 
teacher. I had big plans to include more features on this GUI, however I had 
to reduce my expectations given time. While this GUI is practically useless
it can be used by future developers to upscale my program. """

# OS-level functions
import os  

# Networking
import socket 

# Run external programs
import subprocess  

# System-level access
import sys 

# Run tasks in background
import threading  

# Main GUI library
import tkinter as tk  

# Date and time functions
from datetime import datetime  

# Popup dialogs
from tkinter import messagebox

# Themed Tkinter widgets
from tkinter import ttk  

# Handle images in Tkinter
from PIL import Image, ImageTk 

scan_window = None 
current_url = None
current_name = None
scan_process = None

def open_scan_register():
    """Open scan.py in a separate process if not already running."""
    global scan_process

    # If scan.py is already running, just notify user
    if scan_process and scan_process.poll() is None:
        messagebox.showinfo("Scan Window", "Scan window is already running!")
        return

    # Launch scan.py as a separate Python process
    scan_process = subprocess.Popen([
        sys.executable,  # Path to current Python interpreter
        "/Users/samswallow/Desktop/13_ddt_proj/the files/scan.py"
    ])


def gui():
    """Main teacher menu GUI."""
    teacher_window = tk.Tk()
    teacher_window.title("Teacher Main Menu")
    teacher_window.geometry("1600x1000")
    teacher_window.configure(bg="black")

    # Header frame
    header_frame = tk.Frame(teacher_window, bg="#2c3e50", height=60)
    header_frame.pack(fill="x")

    # Greeting label
    greeting_label = tk.Label(
        header_frame, text="Hello!", bg="#2c3e50",
        fg="white", font=("Arial", 30)
    )
    greeting_label.pack(side="left", padx=10)

    # Time label
    time_label = tk.Label(
        header_frame, text="00:00:00", bg="#2c3e50",
        fg="white", font=("Arial", 30)
    )
    time_label.pack(side="right", padx=10)

    def update_clock():
        """Update greeting and time every second."""
        now = datetime.now()
        hour = now.hour
        greeting = (
            "Good Morning" if 5 <= hour < 12
            else "Good Afternoon" if 12 <= hour < 17
            else "Good Evening"
        )
        greeting_label.config(text=greeting)
        time_label.config(text=now.strftime("%H:%M:%S"))
        teacher_window.after(1000, update_clock)

    update_clock()

    # Scan button
    scan_students_button = tk.Button(
        teacher_window,
        text="Scan for Students!",
        command=open_scan_register,
        font=("Arial", 16)
    )
    scan_students_button.pack(pady=10)

    teacher_window.mainloop()

if __name__ == "__main__":
    gui()






