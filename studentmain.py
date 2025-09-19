from __future__ import print_function # For Python 2/3 compatibility
import tkinter as tk # GUI library
from tkinter import messagebox # GUI library
import datetime # Date and time handling
import socket # Networking
import threading # Running tasks in background / not disrupting mainloops
from lockedbrowser import launch_browser # Custom module to launch a locked browser
from tkinter import ttk # Themed Tkinter widgets
import multiprocessing # Used to launch browser in separate process / not disrupting mainloop (strogner than )
from google.auth.transport.requests import Request # For reqesting creds
from google.oauth2.credentials import Credentials  # Handling Google OAuth2 credentials
from google_auth_oauthlib.flow import InstalledAppFlow # For actually handling OAuth2 flow in Google 
from googleapiclient.discovery import build # For building the calendar service
import os.path # File paths 

url = None
local_ip = None
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Ports
SERVER_PORT = 6060            # Server listening port
STUDENT_LISTENER_PORT = 6061  # Student local listener port

# This function uses sockets to get the local IP address of the device running this code.
def get_local_ip():
    global local_ip  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Here I use sockets. I create a socket for connecting to another server. I open the connection with AF_INET to acess IPv4 addresses and SOCK_DGRAM to use UDP packets which is a secure protocol for conections.
        s.connect(("8.8.8.8", 80)) # Connecting to a random IP with a random port. This does not send any data, it just opens the connection so I can get my local IP.
        local_ip = s.getsockname()[0] # Getting the local IP of my device from the socket connection.
        s.close()
        return local_ip
    except Exception as e :
        messagebox.showerror("Error", f"Failed to connect to server: {e}") # Try and except error handeling. Try to get the IP, if it fails show a detailed error message.

# This function interacts with the Google Calendar API to fetch the next upcoming event.
def get_calendar_info():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES) # Loads the user's credentials from the token.json file if it exists. SCOPES defines the level of access the application is requesting. 
 
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # If the credentials are expired but have a refresh token, refresh them.
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) # If there are no (valid) credentials available, let the user log in and authorize access.
            creds = flow.run_local_server(port=0) # Run the OAuth2 flow to get new credentials.
        with open('token.json', 'w') as token:
            token.write(creds.to_json()) # After obtaining new credentials, save them to token.json for future use.

    service = build('calendar', 'v3', credentials=creds) # Build the Google Calendar service object using Calendar API v3 and the obtained credentials. This is actually what im using from the API.
    now = datetime.datetime.utcnow().isoformat() + 'Z' # Grab the date and time in ISO format with a 'Z' suffix to indicate UTC time.
    events_result = service.events().list(
        calendarId='primary', # Acess the primary calendar of the user.
        timeMin=now, # Only fetch events that are scheduled to start after the current time.
        maxResults=1, # Limit the results to just one event.
        singleEvents=True, # Avoid recurring Calendar events.
        orderBy='startTime' # Ensures the earliest event is fetched.
    ).execute()
    events = events_result.get('items', []) # Opening a dictionary to get the list of events. If there are no events, return an empty list.
    if not events:
        return None
    return events[0]

# This function connects to the main server and marks the student as offline. 
def log_offline():
    global local_ip
    try:
        server_ip = "172.20.10.3"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect((server_ip, SERVER_PORT)) 
            offline_message = f"OFFLINE,{local_ip}"
            s.sendall(offline_message.encode("utf-8"))
            response = s.recv(4096).decode("utf-8")
            messagebox.showinfo("Offline Status", response)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")

# This function creates a new browser tab with the given URL.
def create_tab():
    global url
    if url:
        multiprocessing.Process(target=launch_browser, args=(url,), daemon=True).start() # Use Mulitprocessing to launch the browser in a separate process so it does not disrupt the mainloop.
    else:
        messagebox.showerror("Error", "No URL to launch.")

# This function sets up a socket listener on the student's device to receive URLs from the teacher.
def student_client(button_frame):
    global url, local_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set up the socket to allow address reuse to avoid "Address already in use" errors.
    try:
        s.bind((local_ip, STUDENT_LISTENER_PORT)) # Bind the socket to the local IP and a specific port.
        s.listen(1) # Listen for incoming connections.
        print(f"[CLIENT] Listening on {local_ip}:{STUDENT_LISTENER_PORT}") 
    except OSError as e:  #Handle OS erros, really just for the bind failing.
        print(f"[CLIENT] Failed to bind listener: {e}")
        return

    while True:
        conn, addr = s.accept()
        print(f"[CLIENT] Connection from {addr}")
        try:
            info_received = conn.recv(2048).decode("utf-8")
            print(f"[CLIENT] Received URL: {info_received}")

            if info_received.startswith("DELETE"): 
                for widget in button_frame.winfo_children()[1:]:
                    widget.destroy()
            else:
                student_window.after(0, lambda u=info_received: create_button(u))

        except Exception as e:
            print(f"[CLIENT] Error receiving data: {e}")
        finally:
            conn.close()
    

# This function creates button for URL. This is just used becuase I am handeling variables that are outside of the mainloop.
def create_button(new_url):
    global url
    url = new_url
    tk.Button(
        button_frame,
        text="Open Link",
        command=create_tab,
        font=("Arial", 16), bg="blue", fg="black", width=20).pack(pady=10)


# This function opens the student main menu GUI.
def student_menu():
    global student_window, button_frame, progress
    get_local_ip()
    student_window = tk.Tk() # Makiung the main window using the Tkinter library.
    student_window.title("Student Menu") # Title of the window.
    student_window.geometry("1600x1000") # Size of the window.
    student_window.configure(bg="black") # Background color of the window.

    header_frame = tk.Frame(student_window, bg="green", height=100) # Making the header frame.
    header_frame.pack(fill="x") # Fill the frame across the x axis. Using pack geometry manager to decide where to place the widget.

    greeting_label = tk.Label(header_frame, text="Hello!", bg="green", fg="white", font=("Arial", 30)) # Making a simple Tkinter label for the greeting.
    greeting_label.pack(side="left", padx=10)

    time_label = tk.Label(header_frame, text="", bg="green", fg="white", font=("Arial", 30))
    time_label.pack(side="right", padx=10)

    center_frame = tk.Frame(header_frame, bg="green")
    center_frame.pack(side="top", pady=5, expand=True)

    event_label = tk.Label(center_frame, text="Fetching next event...", font=("Arial", 12), bg="green", fg="white")
    event_label.pack()

    style = ttk.Style() # Creating a style for the progress bar. This is a resuable format for the progress bar. I only use it once becuase editing the progress bar on Tkinter MacOS was problematic but this worked.
    style.theme_use("clam") # Using the "clam" theme for the progress bar.
    style.configure(
        "Green.Horizontal.TProgressbar",
        troughcolor="white",
        bordercolor="black",
        background="blue",
        lightcolor="blue",
        darkcolor="blue"
    )

    progress = ttk.Progressbar(center_frame, orient="horizontal", length=350, mode="determinate", style="Green.Horizontal.TProgressbar") # Creating the progress bar widget.
    progress.pack(pady=5)

    # This function updates the event information and progress bar every second.
    def update_event():
        event = get_calendar_info()
        if not event:
            event_label.config(text="No upcoming events.")
            return

        summary = event.get("summary", "No title") # Get event summary or default to "No title".
        start_str = event["start"].get("dateTime", event["start"].get("date")) # Get start time, handling both dateTime and all-day events.
        end_str = event["end"].get("dateTime", event["end"].get("date")) # Get end time, handling both dateTime and all-day events.

        start_time = datetime.datetime.fromisoformat(start_str.replace("Z", "+00:00")) # Convert to datetime object, handling 'Z' for UTC. Google has it own way for handeling time which is difficult for me to understand.
        end_time = datetime.datetime.fromisoformat(end_str.replace("Z", "+00:00")) # Convert to datetime object, handling 'Z' for UTC. 
        now = datetime.datetime.now(datetime.timezone.utc) # Current time in UTC.

        if start_time <= now <= end_time: # Check if the event is currently ongoing.
            event_label.config(text=f"On Going Event: {summary}") 
        else: # Event is upcoming
            event_label.config(text=f"Next: {summary}")

        # This function updates the progress bar based on the event timing.
        def update_progress():
            while True:
                now = datetime.datetime.now(datetime.timezone.utc)
                if start_time <= now <= end_time:
                    total_seconds = (end_time - now).total_seconds() # Calculate remaining time in seconds.
                    remaining = str(datetime.timedelta(seconds=int(total_seconds))) # Format remaining time as HH:MM:SS.
                    event_label.config(text=f"Current Event: {summary} (ends in {remaining})") 
                    elapsed = (now - start_time).total_seconds() # Calculate elapsed time in seconds.
                    total = (end_time - start_time).total_seconds() # Total event duration in seconds.
                    progress["value"] = (elapsed / total) * 100 # Update progress bar percentage.
                elif now < start_time:
                    total_seconds = (start_time - now).total_seconds() # Calculate time until event starts in seconds.
                    remaining = str(datetime.timedelta(seconds=int(total_seconds))) # Format remaining time as HH:MM:SS.
                    event_label.config(text=f"Next: {summary} (Starts in {remaining})") 
                    progress["value"] = 0 # Reset progress bar to 0% until event starts.
                else:
                    progress["value"] = 0 # Reset progress bar to 0% if event has ended.
                    break

                student_window.after(1000, update_event) # Update every second.
               

        threading.Thread(target=update_progress, daemon=True).start() # Run progress update in a separate thread to avoid blocking the mainloop.

    threading.Thread(target=update_event, daemon=True).start() # Initial call to update event in a separate thread.

    # This function updates the greeting and time every second.
    def update_clock(): 
        now = datetime.datetime.now()  # Get current date and time
        hour = now.hour  # Extract current hour
        greeting = "Good Morning" if 5 <= hour < 12 else "Good Afternoon" if 12 <= hour < 17 else "Good Evening"  
        greeting_label.config(text=greeting)  # Update greeting label
        time_label.config(text=now.strftime("%H:%M:%S"))  # Update time label in HH:MM:SS format
        student_window.after(1000, update_clock)  # Call this function again after 1 second

    update_clock()

    # Buttons
    button_frame = tk.Frame(student_window, bg="black")
    button_frame.pack(pady=50, anchor="center")


    tk.Button(button_frame, text="Log Offline", command=log_offline, font=("Arial", 16), bg="blue", fg="black", width=20).pack(pady=10)
    header_label = tk.Label(
    button_frame,
    text="Available Links",
    font=("Arial", 18, "bold"),
    bg="#2c3e50",   # Dark background for header
    fg="white",     # White text for contrast
    anchor="center" # Center text horizontally
)
    header_label.pack(fill="x", pady=(0, 10))
    # Start Student listener
    threading.Thread(target=student_client, args=(button_frame,), daemon=True).start()

    # Start Tkinter mainloop
    student_window.mainloop()



if __name__ == "__main__":
    student_menu()



