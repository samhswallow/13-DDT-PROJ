import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket
from lockedbrowser import launch_browser

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

    content_frame = tk.Frame(student_window, bg="black")
    content_frame.pack(fill="both", expand=True)

    try:
        green_photo = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/greensquare.png")
        resized_photo = green_photo.resize((1500, 800)) 
        green_background = ImageTk.PhotoImage(resized_photo)

        image_label = tk.Label(content_frame, image=green_background, bg="black")
        image_label.image = green_background
        image_label.pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load background image:\n{e}")

    button_frame = tk.Frame(student_window, bg="black")
    button_frame.pack(fill="x", pady=10)

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