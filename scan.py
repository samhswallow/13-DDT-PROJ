"""This script runs a scan system that overlays over the teacher GUI. 
When the teacher wants to connect to the student and send a link over a socket 
connection, they will use this scan syststem to achieve this. The scan script 
discovers which students are online and then displays this in a list to the
teacher before allowing them to connect and send a link."""

# GUI library
import tkinter as tk

# Popup dialogs / alerts
from tkinter import messagebox  

# Themed Tkinter widgets
from tkinter import ttk  

# Image handling
from PIL import Image, ImageTk

# Networking
import socket


# Globals for managing state
saved_link = None
input_window = None
scan_window = None
list_frame = None
canvas = None


def get_online_users():
    """Connect to the server and retrieve the list of online users."""
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((server_ip, server_port))
            s.sendall("SCAN_NETWORK".encode())
            response = s.recv(4096).decode("utf-8")
            return response
    except Exception as e:
        return f"Error: {e}"


def connect_to_user(username, ip):
    """Connect to a specific user and send them the saved link/input."""
    global saved_link
    if not saved_link:
        messagebox.showwarning(
            "No Link",
            "Please enter a link first by clicking 'Send Link / Input'."
        )
        return

    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((server_ip, server_port))
            s.sendall(f"CONNECT,{username},{saved_link}".encode())
            response = s.recv(4096).decode("utf-8")
            messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))


def delete_user_tabs(username, ip):
    """Delete a user's available links."""
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((server_ip, server_port))
            s.sendall(f"DELETE,{username}".encode())
            response = s.recv(4096).decode("utf-8")
            messagebox.showinfo("Server Response", response)
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))


def open_input_window():
    """Open a new window to input a link or text."""
    global entry, input_window
    if input_window and input_window.winfo_exists():
        input_window.lift()
        return

    # GUI info
    input_window = tk.Toplevel()
    input_window.title("Enter Link or Input")
    input_window.geometry("470x150")
    input_window.configure(bg="#333333")

    # Frame
    frame = tk.Frame(input_window, bg="#333333")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Widgets
    tk.Label(
        frame,
        text="Enter your link or input:",
        bg="#333333",
        fg="#FFFFFF",
        font=("Arial", 16)
    ).grid(row=0, column=0, sticky="e", padx=10)

    entry = tk.Entry(
        frame,
        font=("Arial", 16),
        bg="white",
        fg="black",
        highlightbackground="black",
        highlightcolor="black",
        highlightthickness=2,
        bd=2
    )
    entry.grid(row=0, column=1, sticky="w", pady=10, padx=10)

    tk.Button(
        frame,
        text="Save",
        command=save_input,
        font=("Arial", 12),
        bg="#FF3399",
        fg="black"
    ).grid(row=1, column=0, columnspan=2, pady=10)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)


def save_input():
    """Save the input from the input window."""
    global saved_link
    saved_link = entry.get().strip()
    if saved_link == "":
        messagebox.showwarning("Empty Input", "Input cannot be empty.")
        return
    input_window.destroy()


def show_online_users():
    """Fetch and display the list of online users in the scan window."""
    global list_frame, canvas
    if not list_frame or not list_frame.winfo_exists():
        messagebox.showerror("Error", "Scan window has been closed.")
        return

    # Clear previous entries
    for widget in list_frame.winfo_children():
        widget.destroy()

    users_response = get_online_users()

    if users_response.startswith("Error"):
        tk.Label(
            list_frame,
            text="Error fetching users.",
            font=("Arial", 12),
            fg="red",
            bg="#333333"
        ).pack(pady=10)
        return

    # Split response into lines and clean up
    user_entries = [u.strip() for u in users_response.split("\n") if u.strip()]

    if not user_entries:
        tk.Label(
            list_frame,
            text="No users online.",
            font=("Arial", 14),
            fg="#FFFFFF",
            bg="#333333"
        ).pack(pady=10)
    else:
        for entry_data in user_entries:
            data = entry_data.split(",")
            if len(data) < 5:
                continue

            username, name, surname, form_class, ip = data[:5]

            # Row for each user
            row_frame = tk.Frame(
                list_frame,
                bg="#333333",
                highlightbackground="#555555",
                highlightthickness=1,
                height=50
            )
            row_frame.pack(fill="x", pady=5, padx=5)
            row_frame.pack_propagate(False)

            # Widget storing user info
            tk.Label(
                row_frame,
                text=f"{name} {surname} | {ip} | {form_class}",
                font=("Arial", 14),
                fg="#FFFFFF",
                bg="#333333"
            ).pack(side="left", padx=10)

            # Connect button
            tk.Button(
                row_frame,
                text="Connect",
                command=lambda u=username, i=ip: connect_to_user(u, i),
                font=("Arial", 12),
                bg="#FF3399",
                fg="black",
                activebackground="#FF66AA",
                activeforeground="black",
                relief="flat",
                bd=0,
                padx=15,
                pady=5
            ).pack(side="right", padx=10)

            # Delete Button
            tk.Button(
                row_frame,
                text="Delete",
                command=lambda u=username, i=ip: delete_user_tabs(u, i),
                font=("Arial", 12),
                bg="#FF3399",
                fg="black",
                activebackground="#FF66AA",
                activeforeground="black",
                relief="flat",
                bd=0,
                padx=15,
                pady=5
            ).pack(side="right", padx=10)


def gui():
    """Build and show the main scan window GUI."""
    global list_frame, canvas

    # Main GUI 
    scan_window = tk.Tk()
    scan_window.title("Scan Network - Online Users")
    scan_window.geometry("600x600")
    scan_window.configure(bg="#333333")

    # Top logo
    top_frame = tk.Frame(scan_window, bg="#333333")
    top_frame.pack(fill="x", pady=10)

    img = Image.open(
        "/Users/samswallow/Desktop/13_ddt_proj/the files/"
        "38394572444-removebg-preview (1).png"
    )
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    img = img.resize((width, height))
    scan_img = ImageTk.PhotoImage(img)

    # Adding the logo to the GUI
    tk.Label(top_frame, image=scan_img, bg="#333333", borderwidth=0).pack()
    top_frame.image = scan_img  # Keep reference

    # Middle scrollable frame for user list
    middle_frame = tk.Frame(scan_window, bg="#333333")
    middle_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Create a Canvas widget inside middle_frame.
    # - Used to display and scroll other widgets/content.
    canvas = tk.Canvas(middle_frame, bg="#333333", highlightthickness=0)

    # Create a vertical Scrollbar inside middle_frame.
# - Linked to the canvas so users can scroll vertically.
    scrollbar = tk.Scrollbar(
        middle_frame,
        orient="vertical",
        command=canvas.yview
    )

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    list_frame = tk.Frame(canvas, bg="#333333")
    list_frame_id = canvas.create_window(
        (0, 0),
        window=list_frame,
        anchor="nw"
    )

    def on_frame_configure(event):
       # Adjust scrollable area when the frame size changes.
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
       # Make the frame width match the canvas width.
        canvas.itemconfig(list_frame_id, width=event.width)

    list_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    # Bottom buttons
    bottom_frame = tk.Frame(scan_window, bg="#333333")
    bottom_frame.pack(fill="x", pady=10)

    tk.Button(
        bottom_frame,
        text="Send Link / Input",
        command=open_input_window,
        font=("Arial", 12),
        bg="purple",
        fg="black"
    ).pack(side="left", padx=10)

    tk.Button(
        bottom_frame,
        text="Refresh List",
        command=show_online_users,
        font=("Arial", 12),
        bg="blue",
        fg="black"
    ).pack(side="left", padx=10)

    tk.Button(
        bottom_frame,
        text="Close",
        command=scan_window.destroy,
        font=("Arial", 12),
        bg="#FF3399",
        fg="black"
    ).pack(side="right", padx=10)

    return scan_window


if __name__ == "__main__":
    scan_window = gui()
    show_online_users()
    scan_window.mainloop()
