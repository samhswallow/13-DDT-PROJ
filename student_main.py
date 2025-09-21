"""
This module contains all backend logic for the student GUI.
It handles networking, Google Calendar API access, offline logging,
and launching the locked browser. All GUI elements are passed
from the GUI file to allow safe interaction.
"""

# File system path handling
import os.path  

# Networking with TCP/UDP sockets
import socket  

# Running processes in parallel if needed
import multiprocessing  

# Running the lockedbrowser in its own process when needed
from multiprocessing import Process

# Working with dates and times
import datetime  

# GUI alerts and dialogs
from tkinter import messagebox  

# Handling Google API requests
from google.auth.transport.requests import Request  

# OAuth2 credentials for Google APIs
from google.oauth2.credentials import Credentials  

# Handling OAuth2 authentication flow
from google_auth_oauthlib.flow import InstalledAppFlow  

# Building Google API client services (e.g., Calendar)
from googleapiclient.discovery import build  

# Launching the custom locked browser
from locked_browser import launch_browser 

# Global variables
url = None         # Stores the URL to launch in locked browser
local_ip = None    # Stores the local IP of this machine
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Ports
SERVER_PORT = 6060            # Server listening port
STUDENT_LISTENER_PORT = 6061  # Student local listener port


def get_local_ip():
    """Get the local IP address of the machine.

    Tries to connect to an external server to determine
    the outgoing IP. Shows an error message if connection fails.
    """
    global local_ip
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))   
        local_ip = s.getsockname()[0]  
        s.close()
        return local_ip
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to server: {e}")
        return None


def get_calendar_info():
    """Use the Google Calendar API to fetch the next calendar event.

    Connects using OAuth2 credentials and retrieves the earliest
    upcoming event from the primary calendar. Returns None if
    there are no upcoming events.

    Workflow:
        1. Load credentials from `token.json` if they exist.
        2. Refresh the credentials if expired and refreshable.
        3. Otherwise, request new credentials from `credentials.json`
           via a local OAuth2 flow and save them.
        4. Build the Google Calendar API service client.
        5. Fetch the next upcoming event from the primary calendar.

    Returns:
        dict, None: A dictionary containing the next event's details if
        available, otherwise `None`.

    Raises:
        FileNotFoundError: If `credentials.json` is missing and no valid
            token file exists.
        google.auth.exceptions.GoogleAuthError: If authentication fails.
        googleapiclient.errors.HttpError: If the Calendar API request fails.

    Note:
        Requires the Google Calendar API to be enabled in the linked
        Google Cloud project and a valid OAuth2 JSON file.
    """
    creds = None

    # Load saved credentials if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Refresh or obtain new credentials if needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # Force new login if refresh fails
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
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
    displays the server's response in a messagebox.
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


def open_browser_process(url):
    """Launch the locked browser in a separate process."""
    launch_browser(url)


def student_client(button_frame, student_window):
    """Create a socket listener to receive messages from the server.

    Uses a TCP socket bound to the local IP and port 6061
    to receive URLs or commands and update the GUI.
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
                # Add new button safely using after()
                student_window.after(0, lambda u=info_received: create_button(button_frame, u))
        except Exception as e:
            print(f"[CLIENT] Error receiving data: {e}")
        finally:
            conn.close()


def create_button(button_frame, new_url):
    """Create a button that opens its own URL when clicked."""

    import tkinter as tk
    tk.Button(
        button_frame,
        text="Open Link",
        command=lambda: Process(target=open_browser_process, args=(new_url,)).start(),  # Unique Link
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    ).pack(pady=10)

