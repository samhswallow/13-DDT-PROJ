"""This script runs the student GUI. I use a basic Tkinter GUI combined 
with an advanced API calendar. The student GUI also manages the links the
teacher allows them to access, and creates/deletes the buttons used to 
open the available links."""

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
from locked_browser import launch_browser

# Import backend functions from studentmain
from student_main import get_calendar_info, log_offline, get_local_ip, \
    student_client

student_window = None
button_frame = None
progress = None


def create_button(new_url):
    """Create a button that opens its own URL."""

    def button_command():
        launch_browser(new_url)

    tk.Button(
        button_frame,
        text="Open Link",
        command=button_command,
        font=("Arial", 16),
        bg="blue",
        fg="black",
        width=20
    ).pack(pady=10)


def on_close():
    """Handle GUI close event."""
    try:
        threading.Thread(target=log_offline, daemon=True).start()
    except Exception:
        pass
    student_window.destroy()


def gui():
    """This is the GUI main function. Inside this function I except to load 
    and run the main GUI."""
    global student_window, button_frame, progress, greeting_label, time_label

    get_local_ip()

    student_window = tk.Tk()
    student_window.title("Student Menu")
    student_window.geometry("1600x1000")
    student_window.configure(bg="black")

    # Header Frame
    header_frame = tk.Frame(student_window, bg="green", height=100)
    header_frame.pack(fill="x")

    # Time and greeting labels inside the header frame 
    greeting_label = tk.Label(
        header_frame, text="", bg="green", fg="white", font=("Arial", 30)
    )
    greeting_label.pack(side="left", padx=10)

    time_label = tk.Label(
        header_frame, text="", bg="green", fg="white", font=("Arial", 30)
    )
    time_label.pack(side="right", padx=10)

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

    # Center Frame for event and progress bar
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
        background="blue"
    )

    # Create the progress bar before calling update_event
    progress = ttk.Progressbar(
        center_frame, orient="horizontal", length=350,
        mode="determinate", style="Green.Horizontal.TProgressbar"
    )
    progress.pack(pady=5)

    # Update event information and progress bar every second
    def update_event():
        event = get_calendar_info()
        if not event:
            event_label.config(text="No upcoming events.")
            progress["value"] = 0
            student_window.after(60000, update_event)
            return

        summary = event.get("summary", "No title")
        start_str = event["start"].get("dateTime", event["start"].get("date"))
        end_str = event["end"].get("dateTime", event["end"].get("date"))

        start_time = datetime.datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_time = datetime.datetime.fromisoformat(end_str.replace("Z", "+00:00"))

        # Update event label
        now = datetime.datetime.now(datetime.timezone.utc)
        if start_time <= now <= end_time:
            event_label.config(text=f"On Going Event: {summary}")
        else:
            event_label.config(text=f"Next: {summary}")

        # Progress bar update in separate thread
        def update_progress():
            now = datetime.datetime.now(datetime.timezone.utc)

            if start_time <= now <= end_time:
                total_seconds = (end_time - now).total_seconds()
                remaining = str(datetime.timedelta(seconds=int(total_seconds)))
                event_label.config(
                    text=f"Current Event: {summary} (ends in {remaining})"
                )

                elapsed = (now - start_time).total_seconds()
                total = (end_time - start_time).total_seconds()
                progress["value"] = (elapsed / total) * 100

            elif now < start_time:
                total_seconds = (start_time - now).total_seconds()
                remaining = str(datetime.timedelta(seconds=int(total_seconds)))
                event_label.config(
                    text=f"Next: {summary} (Starts in {remaining})"
                )
                progress["value"] = 0

            else:
                progress["value"] = 0

            student_window.after(1000, update_progress)

        # Start updating progress
        update_progress()

        # Schedule next event fetch in 60 seconds
        student_window.after(60000, update_event)

    # Call it once at the start
    update_event()

    # Header Frame for buttons
    button_frame = tk.Frame(student_window, bg="black")
    button_frame.pack(pady=50, anchor="center")

    header_label = tk.Label(
        button_frame, text="Available Links",
        font=("Arial", 18, "bold"), bg="#2c3e50", fg="white",
        anchor="center"
    )
    header_label.pack(fill="x", pady=(0, 10))

    # Start Student listener
    threading.Thread(
        target=student_client, args=(button_frame, student_window),
        daemon=True
    ).start()

    student_window.protocol("WM_DELETE_WINDOW", on_close)
    student_window.mainloop()


if __name__ == "__main__":
    gui()
