import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import socket
import threading
from lockedbrowser import launch_browser

url = None  
local_ip = None 

def get_local_ip():
    global local_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        local_ip = "127.0.0.1"
        return local_ip

def send_ip():
    global local_ip
    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            message = f"ONLINE,{local_ip}"
            s.sendall(message.encode("utf-8"))
            response = s.recv(4096).decode("utf-8")
            return response
    except Exception as e:
        return f"Error: {e}"

def create_tab():
    if url:
        launch_browser(url)
    else:
        messagebox.showerror("Error", "No URL to launch.")

def server_thread():
    global local_ip
    local_ip = get_local_ip()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip, 6060))
    server_socket.listen(5)
    print(f"[*] Listening on {local_ip}:6060...")

    while True:
        client, addr = server_socket.accept()
        print(f"[+] Connection received from {addr}")
        data = client.recv(2048).decode("utf-8")
        print(f"[+] Data received: {data}")
        client.sendall("Link received successfully.".encode())
        client.close()
        global url
        url = data

def start_server():
    threading.Thread(target=server_thread, daemon=True).start()

def student_client(button_frame):
    global url, local_ip
    try:
        local_ip = get_local_ip()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 6060))

        message = f"ONLINE,{local_ip}"
        s.sendall(message.encode("utf-8"))

        url_received = s.recv(2048).decode("utf-8")
        print(f"Message received: {url_received}")

        url = url_received  

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

        messagebox.showinfo("Server Message", url)
        s.close()

    except ConnectionRefusedError:
        messagebox.showerror(
            "Connection Error",
            "No server running on this IP and port.\nPlease start the server first."
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def log_online():
 
    response = send_ip()
    
    if response.startswith("IP None"):
        messagebox.showerror("Error", "The IP address could not be determined.")
    else:
        messagebox.showinfo("Online Status", response)




def student_menu():
     

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
        text="Log Online",
        command=log_online,
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    )
    log_online_button.pack(pady=10)

    recieve_data_button = tk.Button(
            button_frame,
            text="Start Connection",
            command=start_server,
            font=("Arial", 16),
            bg="blue",
            fg="black",
            width=20
        )
    
    recieve_data_button.pack(pady=10)

    student_window.mainloop()

if __name__ == "__main__":
    student_menu()



