import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import login

def student_menu():
    student_window = tk.Toplevel(root)
    student_window.title("Student Menu")
    student_window.geometry("1600x1000")
    student_window.configure(bg="black")

    
    green_photo = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/greensquare.png")
    resized_photo = green_photo.resize((1500, 900))
    green_background = ImageTk.PhotoImage(resized_photo)
    green_background_label = tk.Label(student_window, image=green_background, bg="black")
    green_background_label.place(x=20, y=20)

    
    student_window.green_background = green_background

   
    view_info_button = tk.Button(student_window, text="View Info", font=("Arial", 16))
    view_info_button.place(x=700, y=850)


root = tk.Tk()
root.withdraw()  
login.login(root, student_menu)
root.mainloop()