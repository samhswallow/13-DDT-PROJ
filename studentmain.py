import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket


def establish_connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.17.1.39", 6060))  # connect to server IP and port


        message = s.recv(2048).decode("utf-8")
        print(f"Message received: {message}")
        messagebox.showinfo("Server Message", message)


        s.close()
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "No server running on this IP and port.\nPlease start the server first.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




def student_menu():
    student_window = tk.Tk()  
    student_window.title("Student Menu")
    student_window.geometry("1600x1000")
    student_window.configure(bg="black")


    green_photo = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/greensquare.png")
    resized_photo = green_photo.resize((1500, 900))
    green_background = ImageTk.PhotoImage(resized_photo)
    green_background_label = tk.Label(student_window, image=green_background, bg="black")
    green_background_label.place(x=20, y=20)


   
    student_window.green_background = green_background


   
    establish_connection_button = tk.Button(student_window, text="establish connection", command = establish_connection,font=("Arial", 16))
    establish_connection_button.place(x=700, y=850)


    student_window.mainloop()


if __name__ == "__main__":
    student_menu()