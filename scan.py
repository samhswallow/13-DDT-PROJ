import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import socket

saved_link = None
input_window = None
scan_window = None
list_frame = None


def get_online_users():
    try:
        server_ip = "10.17.1.40"
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
    try:
        server_ip = "10.17.1.40"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            s.sendall(f"CONNECT,{username},{saved_link}".encode())
            response = s.recv(4096).decode("utf-8")
            print(f"[DEBUG] Connect response: {response}")
            messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))

def open_input_window():
    global entry, input_window

    if input_window and input_window.winfo_exists():
        input_window.lift()
        return

    input_window = tk.Toplevel()
    input_window.title("Enter Link or Input")
    input_window.geometry("470x150")
    input_window.configure(bg="#333333")

    frame = tk.Frame(input_window, bg="#333333")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    link_label = tk.Label(frame, text="Enter your link or input:", bg="#333333", fg="#FFFFFF", font=("Arial", 16))
    link_label.grid(row=0, column=0, sticky="e", padx=10)

    entry = tk.Entry(frame, font=("Arial", 16), bg="white", fg="black",
                     highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)
    entry.grid(row=0, column=1, sticky="w", pady=10, padx=10)

    save_button = tk.Button(frame, text="Save", command=save_input, font=("Arial", 12), bg="#FF3399", fg="black")
    save_button.grid(row=1, column=0, columnspan=2, pady=10)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

def save_input():
    global saved_link
    saved_link = entry.get().strip()
    if saved_link == "":
        messagebox.showwarning("Empty Input", "Input cannot be empty.")
        return
    print(f"[DEBUG] Saved link: {saved_link}")
    input_window.destroy()

def show_online_users():
    global list_frame
    for widget in list_frame.winfo_children():
        widget.destroy()

    users_response = get_online_users()
    print(f"[DEBUG] Raw server response:\n{users_response}")

    if users_response.startswith("Error"):
        error_label = tk.Label(list_frame, text="Error fetching users.", font=("Arial", 12), fg="red", bg="#333333")
        error_label.pack(pady=10)
        return

    user_entries = [u.strip() for u in users_response.split("\n") if u.strip()]
    print(f"[DEBUG] Parsed user entries: {user_entries}")

    if not user_entries:
        empty_label = tk.Label(list_frame, text="No users online.", font=("Arial", 14), fg="#FFFFFF", bg="#333333")
        empty_label.pack(pady=10)
    else:
        for entry in user_entries:
            data = entry.split(",")
            if len(data) >= 5:
                username, name, surname, form_class, ip = data[:5]

                row_frame = tk.Frame(list_frame, bg="#333333", highlightbackground="#555555", highlightthickness=1, height=50)
                row_frame.pack(fill="x", pady=5, padx=5)
                row_frame.pack_propagate(False)

                info_label = tk.Label(row_frame, text=f"{username} | {ip} | {form_class}",
                                      font=("Arial", 14), fg="#FFFFFF", bg="#333333")
                info_label.pack(side="left", padx=10)

                connect_button = tk.Button(row_frame, text="Connect",
                                           command=lambda u=username, i=ip: connect_to_user(u, i),
                                           font=("Arial", 12), bg="#FF3399", fg="black",
                                           activebackground="#FF66AA", activeforeground="black",
                                           relief="flat", bd=0, padx=15, pady=5)
                connect_button.pack(side="right", padx=10)
            else:
                print(f"[DEBUG] Malformed entry skipped: {entry}")


def gui(parent):
    global scan_window, list_frame
    scan_window = tk.Toplevel(parent)
    scan_window.title("Scan Network - Online Users")
    scan_window.geometry("600x600")
    scan_window.configure(bg="#333333")

    top_frame = tk.Frame(scan_window, bg="#333333")
    top_frame.pack(fill="x", pady=10)

    img = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png")
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    img = img.resize((width, height))
    scan_img = ImageTk.PhotoImage(img)

    scan_label = tk.Label(top_frame, image=scan_img, bg="#333333", borderwidth=0)
    scan_label.image = scan_img
    scan_label.pack()

    middle_frame = tk.Frame(scan_window, bg="#333333")
    middle_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(middle_frame, bg="#333333", highlightthickness=0)
    scrollbar = tk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#333333")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    list_frame = scrollable_frame

    bottom_frame = tk.Frame(scan_window, bg="#333333")
    bottom_frame.pack(fill="x", pady=10)

    send_link_button = tk.Button(bottom_frame, text="Send Link / Input", command=open_input_window,
                                 font=("Arial", 12), bg="purple", fg="black")
    send_link_button.pack(side="left", padx=10)

    refresh_button = tk.Button(bottom_frame, text="Refresh List", command=show_online_users,
                               font=("Arial", 12), bg="blue", fg="black")
    refresh_button.pack(side="left", padx=10)

    close_button = tk.Button(bottom_frame, text="Close", command=scan_window.destroy,
                             font=("Arial", 12), bg="#FF3399", fg="black")
    close_button.pack(side="right", padx=10)

    return scan_window


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  
    gui(root)
    root.mainloop()
   
