"""This script handles the login GUI and links it to the backend."""

# Tkinter: for building the GUI elements 
import tkinter as tk

# PIL (Pillow): for opening, resizing, and displaying images in Tkinter
from PIL import Image, ImageTk

# Backend module: contains login logic, server and, communication
import login as backend



def gui():
    """Handles the login GUI."""
    global username_entry, password_entry, login_window

    # Create main window and link it to backend
    login_window = tk.Tk()
    backend.login_window = login_window
    login_window.title("Login Window")
    login_window.geometry("600x440")
    login_window.configure(bg="#333333")

    frame = tk.Frame(login_window, bg="#333333")

    # Logo image
    img = Image.open(
        "/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png"
    )
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    img = img.resize((width, height))
    login_img = ImageTk.PhotoImage(img)
    login_label = tk.Label(frame, image=login_img, bg="#333333", borderwidth=0)
    login_label.image = login_img  # Keep reference to prevent garbage collection

    # Username input
    username_label = tk.Label(
        frame, 
        text="Username", 
        bg="#333333", 
        fg="#FFFFFF", 
        font=("Arial", 16)
    )
    username_entry = tk.Entry(
        frame, 
        font=("Arial", 16), 
        bg="white", 
        highlightbackground="black", 
        highlightcolor="black"
    )
    backend.username_entry = username_entry  # Assign backend reference

    # Password input
    password_label = tk.Label(
        frame, text="Password", bg="#333333", fg="#FFFFFF", font=("Arial", 16)
    )
    password_entry = tk.Entry(
        frame, 
        show="*", 
        font=("Arial", 16), 
        bg="white", 
        highlightbackground="black", 
        highlightcolor="black"
    )
    backend.password_entry = password_entry  # Assign backend reference

    # Buttons
    login_button = tk.Button(
        frame,
        text="Login",
        bg="#333333",
        fg="black",
        font=("Arial", 16),
        command=backend.check_credentials,
    )
    register_button = tk.Button(
        frame,
        text="Register",
        bg="#333333",
        fg="black",
        font=("Arial", 16),
        command=backend.open_register,
    )

    # Layout
    login_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    username_label.grid(row=1, column=0, sticky="e", padx=10)
    username_entry.grid(row=1, column=1, sticky="w", pady=10, padx=10)
    password_label.grid(row=2, column=0, sticky="e", padx=10)
    password_entry.grid(row=2, column=1, sticky="w", pady=10, padx=10)
    login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), ipadx=30)
    register_button.grid(row=4, column=0, columnspan=2, pady=(0, 20), ipadx=20)

    frame.pack(expand=True)

# Run the GUI if this script is executed directly
if __name__ == "__main__":
    gui()
    backend.login_window.mainloop()
