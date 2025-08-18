import socket
import tkinter as tk
from tkinter import messagebox

saved_link = None 

def get_online_users():
    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall("SCAN_NETWORK".encode())
            response = s.recv(4096).decode("utf-8")
            print(f"[DEBUG] Response: {response}")  
            return response
    except Exception as e:
        return f"Error: {e}"

def connect_to_user(username, ip):
    global saved_link
    if not saved_link:
        messagebox.showwarning("No Link", "Please enter a link or input first by clicking 'Send Link / Input'.")
        return

    print(f"[DEBUG] Connecting to {username} at {ip} with link: {saved_link}")

    try:
        server_ip = "127.0.0.1"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
           
            s.sendall(f"CONNECT,{username},{saved_link}".encode())
            response = s.recv(4096).decode("utf-8")
            print(f"[DEBUG] Connect response: {response}")
            messagebox.showinfo("Server Response", response)
            return response
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
        return f"Error: {e}"

def open_input_window():
    global saved_link

    def save_input():
        global saved_link
        saved_link = entry.get().strip()
        if saved_link == "":
            messagebox.showwarning("Empty Input", "Input cannot be empty.")
            return
        print(f"[DEBUG] Saved link: {saved_link}")
        input_window.destroy()

    input_window = tk.Toplevel()
    input_window.title("Enter Link or Input")
    input_window.geometry("400x150")

    label = tk.Label(input_window, text="Enter your link or input:", font=("Arial", 12), fg="black")
    label.pack(pady=10)

    entry = tk.Entry(input_window, font=("Arial", 12), width=40, fg="black")
    entry.pack(pady=5)

    save_button = tk.Button(input_window, text="Save", command=save_input, font=("Arial", 12), bg="blue", fg="black")
    save_button.pack(pady=10)

def load_buttons():
    send_link_button = tk.Button(
        list_frame,
        text="Send Link / Input",
        command=open_input_window,
        font=("Arial", 12),
        bg="purple",
        fg="black"
    )
    send_link_button.pack(pady=20)

    refresh_button = tk.Button(
        list_frame,
        text="Refresh List",
        command=show_online_users,
        font=("Arial", 12),
        bg="blue",
        fg="black"
    )
    refresh_button.pack(pady=10)

def show_online_users():
        for widget in list_frame.winfo_children():
            widget.destroy()

        users_response = get_online_users()
        print(f"[DEBUG] Raw server response:\n{users_response}")

        if users_response.startswith("Error"):
            error_label = tk.Label(list_frame, text="Error fetching users.", font=("Arial", 12), fg="red")
            error_label.pack(pady=10)
            return

        user_entries = [u.strip() for u in users_response.split("\n") if u.strip()]
        print(f"[DEBUG] Parsed user entries: {user_entries}")  

        if not user_entries:
            empty_label = tk.Label(list_frame, text="No users online.", font=("Arial", 12), fg="black")
            empty_label.pack(pady=10)
        else:
            for entry in user_entries:
                data = entry.split(",")
                if len(data) >= 5:
                    username, name, surname, form_class, ip = data[:5]

                    row_frame = tk.Frame(list_frame, bd=1, relief="solid")
                    row_frame.pack(fill="x", pady=5)

                    info_label = tk.Label(row_frame, text=f"{username} | {ip} | {form_class}", font=("Arial", 12), fg="black")
                    info_label.pack(side="left", padx=5)

                    connect_button = tk.Button(
                        row_frame,
                        text="Connect",
                        command=lambda u=username, i=ip: connect_to_user(u, i),
                        font=("Arial", 10),
                        bg="green",
                        fg="black"
                    )
                    connect_button.pack(side="right", padx=5)
                else:
                    print(f"[DEBUG] Malformed entry skipped: {entry}")
        load_buttons()

def gui():
    global root, list_frame
    root = tk.Tk()
    root.title("Scan Network - Online Users")
    root.geometry("600x600")

    label = tk.Label(root, text="Currently Online Users", font=("Arial", 16), fg="black")
    label.pack(pady=10)

    global list_frame
    list_frame = tk.Frame(root)
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    close_button = tk.Button(
        root,
        text="Close",
        command=root.destroy,
        font=("Arial", 12),
        fg="black"
    )
    close_button.pack(pady=10)

    load_buttons()
    root.mainloop()          

if __name__ == "__main__":
    gui()
