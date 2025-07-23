import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import socket
import threading


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


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(("172.20.10.2", 6060))  
    except OSError as e:
        print(f"Could not bind socket: {e}")
        return

    s.listen(1)
    print("Server listening on 172.20.10.2:6060...")

    while True:
        clientSocket, address = s.accept()
        print(f"Connection established from {address}")
        if current_url:
            message = current_url
            clientSocket.sendall(message.encode())  
        else:
            clientSocket.send("No URL provided.".encode("utf-8"))
        clientSocket.close()



def teacher_menu():
    global main_window
    main_window = tk.Toplevel()
    main_window.title("Teacher Main Menu")
    main_window.geometry("1600x1000")
    main_window.configure(bg="black")

    
    main_window.rowconfigure(0, weight=1)
    main_window.rowconfigure(1, weight=0)
    main_window.columnconfigure(0, weight=1)

    content_frame = tk.Frame(main_window, bg="black")
    content_frame.grid(row=0, column=0, sticky="nsew")
    content_frame.rowconfigure(0, weight=1)
    content_frame.columnconfigure(0, weight=1)

    try:
        green_photo = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/greensquare.png")
        resized_photo = green_photo.resize((1500, 900))
        green_background = ImageTk.PhotoImage(resized_photo)
        background_label = tk.Label(content_frame, image=green_background, bg="black")
        background_label.image = green_background 
        background_label.grid(row=0, column=0, sticky="nsew")
        main_window.green_background = green_background
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not load image:\n{e}")

  
    button_frame = tk.Frame(main_window, bg="black")
    button_frame.grid(row=1, column=0, pady=20)

    connect_button = tk.Button(
        button_frame,
        text="Start Connection",
        command=begin_data,
        font=("Arial", 16)
    )
    connect_button.pack(pady=10)

    
    threading.Thread(target=server, daemon=True).start()


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