import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import socket
import threading
from lockedbrowser import launch_browser
import time
import multiprocessing

url = None  
local_ip = None 

def get_local_ip():
    global local_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 6060))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        local_ip = "127.0.0.1"
        return local_ip
    

def log_offline():
    global local_ip
    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            offline_message = f"OFFLINE,{local_ip}"
            s.sendall(offline_message.encode("utf-8"))
            offline_response = s.recv(4096).decode("utf-8")

            if offline_response.startswith("IP None"):
                messagebox.showerror("Error", "The IP address could not be determined.")
            else:
                messagebox.showinfo("Offline Status", offline_response)
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def create_tab():
    global url
    if url:
        multiprocessing.Process(target=launch_browser, args=(url,), daemon=True).start()
    else:
        messagebox.showerror("Error", "No URL to launch.")

def student_client(button_frame):
    print("[CLIENT] Starting student client...")
    global url, local_ip
    print(f"[CLIENT] Starting server on IP: {local_ip} and port 6060")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((local_ip, 6060))
    s.listen(1)
    print("[CLIENT] Waiting for link...")
    print(f"This is the local IP: {local_ip}")

    while True:
        conn, addr = s.accept()
        print(f"[CLIENT] Connection from {addr}")
        
        try:
            url_received = conn.recv(2048).decode("utf-8")
            print(f"[CLIENT] Received URL: {url_received}")
            if url_received:
                student_window.after(0, lambda u=url_received: create_button(u))
        except Exception as e:
            print(f"[CLIENT] Error receiving data: {e}")
        finally:
            conn.close()

def create_button(new_url):
    global url
    url = new_url  
    
    authorised_link_button = tk.Button(
        button_frame,
        text="Open Link",
        command=create_tab,
        font=("Arial", 14),
        bg="green",
        fg="white",
        width=15
    )
    authorised_link_button.pack(pady=10)

def log_online(button_frame):
    get_local_ip()
    global local_ip
    threading.Thread(target=student_client, args=(button_frame,), daemon=True).start()
    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))

            online_message = f"ONLINE,{local_ip}"
            s.sendall(online_message.encode("utf-8"))

            online_response = s.recv(4096).decode("utf-8")
            
            if online_response.startswith("IP None"):
                messagebox.showerror("Error", "The IP address could not be determined.")
            else:
                messagebox.showinfo("Online Status", online_response)

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

def student_menu():
    get_local_ip()
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
        timestamp = now.strftime("%H:%M:%S")

        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"

        greeting_label.config(text=greeting)
        time_label.config(text=timestamp)

        student_window.after(1000, update_clock)

    update_clock()

    button_frame = tk.Frame(student_window, bg="black")
    button_frame.pack(pady=50)

    log_online_button = tk.Button(
        button_frame,
        text="Establish Connection",
        command=lambda: log_online(button_frame),
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    )
    log_online_button.pack(pady=10)

    log_offline_button = tk.Button(
        button_frame,
        text="Log Offline",
        command=log_offline,
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    )
    log_offline_button.pack(pady=10)

    delete_offline_button = tk.Button(
        button_frame,
        text="Link One",
        command=log_offline,
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    )
    delete_offline_button.pack(pady=10)

    student_window.mainloop()

if __name__ == "__main__":
    student_menu()



