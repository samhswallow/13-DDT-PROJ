# Kura Teach

Kura Teach is a classroom management software that helps teachers control and monitor students' internet usage during class time. Built entirely in Python, it features a user-friendly Tkinter GUI, networking capabilities, and optional Google Calendar integration for scheduling.

---

## Features

- Internet Control: Restrict or allow internet usage for students during class.  
- Google Calendar Integration: Students can dynamically see there calander move throuhgout the day. 
- User-Friendly GUI: Intuitive interface built with Tkinter for easy classroom management.  
- Online Logging: Displays a list of students currently using the software.  
- Password Hashing: All passwords are securely hashed for safety.

---

## How to install

1. Install Python  
2. Clone the GitHub repository:  
   ```bash
   git clone https://github.com/samhswallow/13-DDT-PROJ

---
## How to use (student)

1. Edit all IPs to match the IP of your server
2. Start server.py
2. Run login_gui.py

---
## How to use (teacher)

1. Edit all IPs to match the IP of your server
2. Run teacher_main.py

---
## Project structure

project/

|-- pycache/

|-- 3839457244...png

|-- credentials.json

|-- token.json

|-- students.db

|-- locked_browser.py

|-- login.py

|-- login_gui.py

|-- register.py

|-- scan.py

|-- server.py

|-- student_gui.py

|-- student_main.py

|-- teacher_main.py
