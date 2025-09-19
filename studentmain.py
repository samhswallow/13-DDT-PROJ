"""This script runs the student GUI. I use a basic Tkinter GUI combined 
with a advanced API calander. The student GUI also manages the links the
teacher allows them to access, and creates/deletes the buttons used to 
open the aviailble links"""

# For Python 2/3 compatibility
from __future__ import print_function

# Date and time handling
import datetime

# Launch browser in separate process / not disrupting mainloop
import multiprocessing

# File paths
import os.path

# Networking
import socket

# Running tasks in background / not disrupting mainloops
import threading

# GUI library
import tkinter as tk

# GUI popups
from tkinter import messagebox

# Themed Tkinter widgets
from tkinter import ttk

# For requesting Google credentials
from google.auth.transport.requests import Request

# Handling Google OAuth2 credentials
from google.oauth2.credentials import Credentials

# Handling OAuth2 flow
from google_auth_oauthlib.flow import InstalledAppFlow

# Building the Google Calendar service
from googleapiclient.discovery import build

# Custom module to launch a locked browser
from lockedbrowser import launch_browser

url = None
local_ip = None
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Ports
SERVER_PORT = 6060            # Server listening port
STUDENT_LISTENER_PORT = 6061  # Student local listener port

def get_local_ip():
    """Get the local IP address of the machine.

    Tries to connect to an external server to determine
    the outgoing IP. Shows an error message if connection fails.
    """
    # Store the IP globally for use elsewhere
    global local_ip  

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")


def get_calendar_info():
    """Use the Google Calendar API to fetch the next calendar event.

    Connects using OAuth2 credentials and retrieves the earliest
    upcoming event from the primary calendar. Returns None if
    there are no upcoming events.
    """
    creds = None

    # Load saved credentials if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Refresh or obtain new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the new credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Google Calendar service
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.utcnow().isoformat() + 'Z'

    # Fetch the next upcoming event
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=1,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return None
    return events[0]


def log_offline():
    """Send a request to the server to set this client as offline.

    Uses a TCP socket connection to send the offline message and
    displays the server's response.
    """
    global local_ip

    try:
        server_ip = "172.20.10.3"

        # Connect to the server and send offline message
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, SERVER_PORT))
            offline_message = f"OFFLINE,{local_ip}"
            s.sendall(offline_message.encode("utf-8"))

            # Receive and display server response
            response = s.recv(4096).decode("utf-8")
            messagebox.showinfo("Offline Status", response)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")


def create_tab():
    """Launch the locked browser in a separate process using the given URL.

    Uses multiprocessing to start the browser from lockedbrowser.py
    without blocking the main GUI thread.
    """
    global url

    if url:
        # Launch the browser in a separate daemon process
        multiprocessing.Process(
            target=launch_browser,
            args=(url,),
            daemon=True
        ).start()
    else:
        messagebox.showerror("Error", "No URL to launch.")


def student_client(button_frame):
    """Create a socket listener to receive messages from the server.

    Uses a TCP socket bound to the local IP and STUDENT_LISTENER_PORT
    to receive URLs or commands and update the GUI accordingly.
    """
    global url, local_ip

    # Create socket with address reuse enabled
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind the socket and start listening
        s.bind((local_ip, STUDENT_LISTENER_PORT))
        s.listen(1)
        print(f"[CLIENT] Listening on {local_ip}:{STUDENT_LISTENER_PORT}")
    except OSError as e:
        # Handle errors such as port already in use
        print(f"[CLIENT] Failed to bind listener: {e}")
        return

    while True:
        conn, addr = s.accept()
        print(f"[CLIENT] Connection from {addr}")
        try:
            info_received = conn.recv(2048).decode("utf-8")
            print(f"[CLIENT] Received URL: {info_received}")
            if info_received.startswith("DELETE"):

                # Remove all buttons except the first one
                for widget in button_frame.winfo_children()[1:]:
                    widget.destroy()
            else:
                # Add new button in the GUI safely using after()
                student_window.after(0, 
                                     lambda u=info_received: create_button(u)
                )
        except Exception as e:
            # Print any data-receiving errors
            print(f"[CLIENT] Error receiving data: {e}")
        finally:
            conn.close()


def create_button(new_url):
    """ Create a button that opens its own URL when clicked """
    tk.Button(
        button_frame,
        text="Open Link",
        command=lambda: launch_browser(new_url), # Unique Link 
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    ).pack(pady=10)


def on_close():
    """Handle GUI close event."""
    # First, send offline message
    log_offline()
    
    # Then destroy the window
    student_window.destroy()


def gui():
    """ This function handels everything to do with my student 
    GUI. I use Tkinter, as well several other libaries like time 
    to manage and build everything on the GUI."""

    global student_window, button_frame, progress

    get_local_ip()

    student_window = tk.Tk()  
    student_window.title("Student Menu")  
    student_window.geometry("1600x1000")  
    student_window.configure(bg="black")  

    header_frame = tk.Frame(student_window, bg="green", height=100)
    header_frame.pack(fill="x")  

    greeting_label = tk.Label(
        header_frame, text="Hello!", bg="green", fg="white",
        font=("Arial", 30)
    )
    greeting_label.pack(side="left", padx=10)

    time_label = tk.Label(
        header_frame, text="", bg="green", fg="white",
        font=("Arial", 30)
    )
    time_label.pack(side="right", padx=10)

    center_frame = tk.Frame(header_frame, bg="green")
    center_frame.pack(side="top", pady=5, expand=True)

    event_label = tk.Label(
        center_frame, text="Fetching next event...",
        font=("Arial", 12), bg="green", fg="white"
    )
    event_label.pack()

    # Style for the progress bar
    style = ttk.Style()  
    style.theme_use("clam")  
    style.configure(
        "Green.Horizontal.TProgressbar",
        troughcolor="white",
        bordercolor="black",
        background="blue",
        lightcolor="blue",
        darkcolor="blue"
    )

    # Progress bar
    progress = ttk.Progressbar(
        center_frame, orient="horizontal", length=350, mode="determinate",
        style="Green.Horizontal.TProgressbar"
    )
    progress.pack(pady=5)


    # Update event information and progress bar every second
    def update_event():
        event = get_calendar_info()
        if not event:
            event_label.config(text="No upcoming events.")
            return

        summary = event.get("summary", "No title")
        start_str = event["start"].get(
            "dateTime", event["start"].get("date")
        )
        end_str = event["end"].get(
            "dateTime", event["end"].get("date")
        )

        start_time = datetime.datetime.fromisoformat(
            start_str.replace("Z", "+00:00")
        )
        end_time = datetime.datetime.fromisoformat(
            end_str.replace("Z", "+00:00")
        )
        now = datetime.datetime.now(datetime.timezone.utc)

        if start_time <= now <= end_time:
            event_label.config(text=f"On Going Event: {summary}")
        else:
            event_label.config(text=f"Next: {summary}")


        #  Updates the progress bar based on the calander info.
        def update_progress():
            while True:

                now = datetime.datetime.now(datetime.timezone.utc)

                if start_time <= now <= end_time:

                    # Calculate remaining time in seconds.
                    total_seconds = (end_time - now).total_seconds() 

                    # Format remaining time as HH:MM:SS
                    remaining = str(
                    datetime.timedelta(seconds=int(total_seconds))
                    )

                    event_label.config(
                        text=( f"Current Event: {summary}"
                        f"(ends in {remaining})")
                    )

                    #Calculate elapsed time in seconds.
                    elapsed = (now - start_time).total_seconds() 

                    total = (end_time - start_time).total_seconds() 
                    progress["value"] = (elapsed / total) * 100 # 

                elif now < start_time:

                    total_seconds = (start_time - now).total_seconds() 

                    # Format remaining time as HH:MM:SS.
                    remaining = str(
                        datetime.timedelta(seconds=int(total_seconds))
                    ) 

                    event_label.config(
                        text=f"Next: {summary} (Starts in {remaining})"
                    )
                     
                     # Reset progress bar to 0% until event starts.
                    progress["value"] = 0

                else:

                    # Reset progress bar to 0% if event has ended.
                    progress["value"] = 0 

                    break

                # Update every second.
                student_window.after(1000, update_event) 
               
        # update progress in a separate thread to avoid blocking the mainloop.
        threading.Thread(target=update_progress,
                         daemon=True).start() 


    # This function updates the greeting and time every second.
    def update_clock(): 

        # Get current date and time
        now = datetime.datetime.now()  

        # Extract current hour
        hour = now.hour  
        greeting = (
        "Good Morning" if 5 <= hour < 12
        else "Good Afternoon" if 12 <= hour < 17
        else "Good Evening"
        )


        # Update greeting label
        greeting_label.config(text=greeting)  
        time_label.config(text=now.strftime("%H:%M:%S")) 

        # Call this function again after 1 second
        student_window.after(1000, update_clock)  

    update_clock()

    # Buttons
    button_frame = tk.Frame(student_window, 
                            bg="black"
    )
    
    button_frame.pack(pady=50, 
                      anchor="center"
    )


    tk.Button(button_frame, 
              text="Log Offline", 
              command=log_offline, 
              font=("Arial", 16), 
              bg="blue", 
              fg="black", 
              width=20).pack(pady=10
    )
    
    header_label = tk.Label(
    button_frame,
    text="Available Links",
    font=("Arial", 18, "bold"),
    bg="#2c3e50",  
    fg="white",     
    anchor="center"
    ) 

    student_window.protocol("WM_DELETE_WINDOW", on_close)
    
    header_label.pack(fill="x", pady=(0, 10))

    # Start Student listener
    threading.Thread(target=student_client, 
                     args=(button_frame,),
                     daemon=True).start()

    # Start Tkinter mainloop
    student_window.mainloop()

if __name__ == "__main__":
    
    """Tkinter runs its own thread which can disrupted when you run a seperate 
    program as that creates a blocking call. So I use mutliprocessing to
    start a new thread. However, mutliprocessing and starting a new thread 
    'inherits' everything from the parent thread. Tkinter does't comply with
    this and crashes.
    """
    multiprocessing.set_start_method('spawn')

    gui()







