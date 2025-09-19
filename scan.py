import tkinter as tk  # Main GUI library
from tkinter import messagebox  # Popup dialogs / alerts
from PIL import Image, ImageTk  # Handle images in Tkinter
import socket  # Networking / TCP connections


saved_link = None
input_window = None
scan_window = None
list_frame = None
canvas = None



# This function connects to the server and retrieves the list of online users.
def get_online_users():
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            s.connect((server_ip, server_port))
            s.sendall("SCAN_NETWORK".encode()) # Use the SCAN_NETWORK command to get online users.
            response = s.recv(4096).decode("utf-8")
            return response
    except Exception as e: # Error handling.
        return f"Error: {e}"

# This function connects to a specific user and sends them the saved link or input.
def connect_to_user(username, ip):
    global saved_link
    if not saved_link:
        messagebox.showwarning("No Link", "Please enter a link or input first by clicking 'Send Link / Input'.")
        return
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            s.connect((server_ip, server_port))
            s.sendall(f"CONNECT,{username},{saved_link}".encode()) # Use the CONNECT command to send the link/input.
            response = s.recv(4096).decode("utf-8") 
            messagebox.showinfo("Server Response", response)
    except Exception as e: # Error handling.
        messagebox.showerror("Connection Error", str(e))

def delete_user_tab(username,ip):
    try:
        server_ip = "172.20.10.3"
        server_port = 6060
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            s.connect((server_ip, server_port))
            s.sendall(f"DELETE,{username}".encode()) # Use the DELETE command to wipe avaible links.
            response = s.recv(4096).decode("utf-8") 
            messagebox.showinfo("Server Response", response)
    except Exception as e: # Error handling.
        messagebox.showerror("Connection Error", str(e))

# This function opens a new window to input a link or text.
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

    tk.Label(frame, text="Enter your link or input:", bg="#333333", fg="#FFFFFF", font=("Arial", 16)).grid(row=0, column=0, sticky="e", padx=10)
    entry = tk.Entry(frame, font=("Arial", 16), bg="white", fg="black",
                     highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=2)
    entry.grid(row=0, column=1, sticky="w", pady=10, padx=10)

    tk.Button(frame, text="Save", command=save_input, font=("Arial", 12), bg="#FF3399", fg="black").grid(row=1, column=0, columnspan=2, pady=10)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

# This function saves the input from the input window.
def save_input():
    global saved_link
    saved_link = entry.get().strip()
    if saved_link == "":
        messagebox.showwarning("Empty Input", "Input cannot be empty.")
        return
    input_window.destroy()

# This function fetches and displays the list of online users in the scan window. It can be resued to refresh the list.
def show_online_users():
    global list_frame, canvas # Ensure these are defined. The list frame holds user entries, canvas enables scrolling.
    if not list_frame or not list_frame.winfo_exists():
        messagebox.showerror("Error", "Scan window has been closed.")
        return

    for widget in list_frame.winfo_children():
        widget.destroy() # Clear previous entries.

    users_response = get_online_users()

    if users_response.startswith("Error"):
        tk.Label(list_frame, text="Error fetching users.", font=("Arial", 12), fg="red", bg="#333333").pack(pady=10)
        return # Error handling.

    user_entries = [u.strip() for u in users_response.split("\n") if u.strip()] # Split response into lines and clean up.

    if not user_entries:
        tk.Label(list_frame, text="No users online.", font=("Arial", 14), fg="#FFFFFF", bg="#333333").pack(pady=10) # No users online.
    else:
        for entry_data in user_entries:
            data = entry_data.split(",")
            if len(data) < 5:
                continue 
            username, name, surname, form_class, ip = data[:5] # Unpack user data.

            row_frame = tk.Frame(list_frame, bg="#333333", highlightbackground="#555555", highlightthickness=1, height=50) # Making a row for each user in the list.
            row_frame.pack(fill="x", pady=5, padx=5)
            row_frame.pack_propagate(False)

            tk.Label(row_frame, text=f"{name} {surname} | {ip} | {form_class}", font=("Arial", 14), fg="#FFFFFF", bg="#333333").pack(side="left", padx=10) # User info label
            tk.Button(row_frame, text="Connect", 
                      command=lambda u=username, i=ip: connect_to_user(u, i), # Connect button. Connecits to user when clicked so links can be passed through.
                      font=("Arial", 12), bg="#FF3399", fg="black",
                      activebackground="#FF66AA", activeforeground="black",
                      relief="flat", bd=0, padx=15, pady=5).pack(side="right", padx=10)
            
            tk.Button(row_frame, text="Delete", 
                      command=lambda u=username, i=ip: delete_user_tab(u, i), 
                      font=("Arial", 12), bg="#FF3399", fg="black",
                      activebackground="#FF66AA", activeforeground="black",
                      relief="flat", bd=0, padx=15, pady=5).pack(side="right", padx=10)


 # This function builds and shows the main scan window GUI.
def gui():
    global list_frame, canvas
    root = tk.Tk()  # Create the main scan window
    root.title("Scan Network - Online Users")
    root.geometry("600x600")
    root.configure(bg="#333333")

    # Top logo
    top_frame = tk.Frame(root, bg="#333333")
    top_frame.pack(fill="x", pady=10)

    img = Image.open("/Users/samswallow/Desktop/13_ddt_proj/the files/38394572444-removebg-preview (1).png")
    width = 300
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    img = img.resize((width, height))
    scan_img = ImageTk.PhotoImage(img)

    tk.Label(top_frame, image=scan_img, bg="#333333", borderwidth=0).pack()
    # keep reference
    top_frame.image = scan_img

    # Middle scrollable frame to store user list
    middle_frame = tk.Frame(root, bg="#333333")  # Container frame inside main window
    middle_frame.pack(expand=True, fill="both", padx=10, pady=10)

    canvas = tk.Canvas(middle_frame, bg="#333333", highlightthickness=0)  # Canvas for scrolling and holding widgets
    scrollbar = tk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)  # Vertical scrollbar linked to canvas

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    list_frame = tk.Frame(canvas, bg="#333333")  # Frame inside canvas to hold user entries

    list_frame_id = canvas.create_window((0, 0), window=list_frame, anchor="nw")  # Embed frame in canvas at top-left

    def on_frame_configure(event):  
        canvas.configure(scrollregion=canvas.bbox("all"))  # Update scrollable area when inner frame changes. Uses bbox to get bounding box of all items in canvas.

    def on_canvas_configure(event):  
        canvas.itemconfig(list_frame_id, width=event.width)  # Match frame width to canvas width when resized by looking at the width of the variable event.

    list_frame.bind("<Configure>", on_frame_configure)  # Trigger scrollregion update when frame resizes
    canvas.bind("<Configure>", on_canvas_configure)  # Adjust frame width whenever canvas resizes


    # Bottom buttons
    bottom_frame = tk.Frame(root, bg="#333333")
    bottom_frame.pack(fill="x", pady=10)

    tk.Button(bottom_frame, text="Send Link / Input", command=open_input_window, font=("Arial", 12), bg="purple", fg="black").pack(side="left", padx=10)
    tk.Button(bottom_frame, text="Refresh List", command=show_online_users, font=("Arial", 12), bg="blue", fg="black").pack(side="left", padx=10)
    tk.Button(bottom_frame, text="Close", command=root.destroy, font=("Arial", 12), bg="#FF3399", fg="black").pack(side="right", padx=10)


   
 
    

    return root

if __name__ == "__main__":
    root = gui()    
    show_online_users()  
    root.mainloop() 


