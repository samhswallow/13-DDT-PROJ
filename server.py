import socket # For networking
import sqlite3 # For database
from argon2 import PasswordHasher # For password hashing

ph = PasswordHasher() # Initialize Argon2 password hasher

# This function handles the creation of my SQLite database.
def create_database(): 
    conn = sqlite3.connect("students.db") # Connect to (or create) the database file
    cursor = conn.cursor() # Create a cursor object to execute SQL commands
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            name TEXT,
            surname TEXT,
            form_class TEXT,
            password TEXT,
            ip TEXT UNIQUE,
            online_status INTEGER DEFAULT 0
        )
    """) # Create users table if it doesn't exist
    conn.commit() # Save changes
    conn.close() # Close the connection

# This function saves registration data to the database, I also use Argon2 to hash passwords before storing them.
def save_to_database(data):
    try:
        username, name, surname, form_class, password, ip = data.split(",") # Unpack registration data

        password = ph.hash(password)   # Hash the password using Argon2

        conn = sqlite3.connect("students.db")   # Connect to the database
        cursor = conn.cursor() # Create cursor

        cursor.execute("""
            INSERT INTO users (username, name, surname, form_class, password, ip, online_status)
            VALUES (?, ?, ?, ?, ?, ?, 0) 
        """, (username, name, surname, form_class, password, ip)) # Insert user data with online_status = 0 (offline). This is so users can use the online/offline feature.

        conn.commit()
        conn.close()
        print(f"[+] Saved {username} to database with online_status = 0.")
    except sqlite3.IntegrityError: # Eror if username or IP already exists
        print(f"[!] Username '{username}' or IP '{ip}' already exists.")
    except Exception as e: # Error handling
        print(f"[!] Error saving to database: {e}") 


# This function handles login requests, verifies passwords, and updates online status.
def login_protocol(data):

    global login_value
    login_value = False  # Default to False
    parts = data.split(",")
    if len(parts) < 3:
        print("[!] Invalid LOGIN command format")
        return

    username = parts[1] # Extract entered username and password
    entered_password = parts[2] 

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,)) # Fetch stored hash for the username.
    result = cursor.fetchone()

    if not result: # Error handeling
        print("[!] User not found")
        conn.close()
        return

    stored_hash = result[0] # Extract the stored hash

    try:
        if ph.verify(stored_hash, entered_password): # Argon verify to check if the password the user gave to the server matches the stored hash.
            login_value = True
            print(f"[+] Login successful for user: {username}") # Successful login

            cursor.execute("UPDATE users SET online_status = 1 WHERE username = ?", (username,)) # Set user as online on login
            conn.commit()
        else: # Error handling
            print("[!] Incorrect password")
    except: 
        print("[!] Incorrect password or hash verification failed") 

    conn.close()

# This function marks a user as online based on their IP address. Once the user sends a offline ping the user is marked as offline.
def register_offline(ip):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE ip = ?", (ip,))
    user = cursor.fetchone()

    if user:
        cursor.execute("""
            UPDATE users SET online_status = 0 WHERE ip = ?
        """, (ip,))
        conn.commit()
        print(f"[+] User with IP {ip} is now offline.")
    else:
        print(f"[!] No user found with IP {ip}.")

    conn.close()

# This is my central server. Its a core component of my program. Here I handle incoming reuqests from clients, process commands, and interact with the database.
def run_server():
    create_database()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 6060))  # I bind to 0.0.0.0 to allow all users to connect my localhost. There are three kinds of IP connections. The Localhost, the Lan IP, and the Public IP. The Localhost is my own computer. The Lan IP is the wifi network. The Public IP can be connected to by anyone.    
    s.listen(5)  # Listen for incoming connections
    print("[*] Server is listening on 0.0.0.0:6060")

    while True:
        client_socket, addr = s.accept()
        print(f"[+] Connection from {addr}")
        data = client_socket.recv(2048).decode("utf-8").strip()
        print("[*] Received:", data)

        if data.startswith("LOGIN"): # This is how my server speaks to my clients. Once they send over a LOGIN command. The server handles it seperatly. 
            login_protocol(data)  # Runs the login protocol function given the data from the client.
            if login_value:
                client_socket.sendall("SUCCESS Login successful!".encode()) # If login is successful, send success message back to client.
            else:
                client_socket.sendall("Invalid username or password.".encode()) # If login fails, send failure message back to client.

        elif data.startswith("CONNECT"): # This is how the teacher connects to a student. The teacher sends over a CONNECT command with the username and the saved link/input. The server then looks up the username in the database, checks if they are online, and if so, sends the saved link/input to the student's IP address on port 6061.
            parts = data.split(",", 2)
            if len(parts) == 3: # Here I break down the data in chunks. The first chunk is the command, the second chunk is the username, and the third chunk is the saved link/input.
                command = parts[0]
                username = parts[1].strip()
                saved_link = parts[2].strip()

                conn = sqlite3.connect("students.db") # Connect to the database
                cursor = conn.cursor()

                cursor.execute("SELECT ip FROM users WHERE username = ? AND online_status = 1", (username,)) # Check if the user is online before sending the link/input.
                result = cursor.fetchone()
                conn.close()

                if result:
                    target_ip = result[0]
                    print(f"[+] Found user '{username}' with IP {target_ip}, who is Online. Sending saved link...") # If the user is online, send the link/input to their IP address on port 6061.

                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                            send_sock.connect((target_ip, 6061))  # Connect to the student's IP on port 6061
                            send_sock.sendall(saved_link.encode()) # Send the saved link/input
                        print(f"[+] Link sent to {username}") 
                    except Exception as e: # Error handling
                        client_socket.sendall(f"Failed to send link to {username}: {e}".encode()) 
                        print(f"[!] Failed to send link to {username}: {e}") 
                else: 
                    client_socket.sendall(f"User '{username}' not found.".encode()) 
                    print(f"[!] User '{username}' not found.")
            else:
                client_socket.sendall("Invalid CONNECT command format.".encode())
                print("[!] Invalid CONNECT command format")

        elif data.startswith("DELETE"):
            parts = data.split(",", 1)

            command = parts[0]
            username = parts[1].strip()

            conn = sqlite3.connect("students.db") # Connect to the database
            cursor = conn.cursor()

            cursor.execute("SELECT ip FROM users WHERE username = ? AND online_status = 1", (username,)) # Check if the user is online before sending the link/input.
            result = cursor.fetchone()
            conn.close()

            if result:
                    target_ip = result[0]
                    print(f"[+] Found user '{username}' with IP {target_ip}, who is Online. Deleting all links")
                    
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                            send_sock.connect((target_ip, 6061))  # Connect to the student's IP on port 6061
                            send_sock.sendall("DELETE".encode()) # Send the saved link/input

                    except Exception as e: # Error handling
                        client_socket.sendall(f"Failed to delete links for {username}: {e}".encode()) 
                        print(f"[!] Failed to delete links for {username}: {e}") 
            else: 
                    client_socket.sendall(f"User '{username}' not found.".encode()) 
                    print(f"[!] User '{username}' not found.")

        
        elif data.startswith("OFFLINE"): # This is how the student marks themselves as offline. The student sends over an OFFLINE command with their IP address. The server then looks up the IP address in the database and marks the user as offline.
            ip = data.split(",")[1]
            register_offline(ip)
            client_socket.sendall(f"IP {ip} registered as offline.".encode())


        elif data == "SCAN_NETWORK": # This is how the teacher scans for online students. The teacher sends over a SCAN_NETWORK command. The server then looks up all users in the database with online_status = 1 (online) and sends back their details to the teacher.
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            cursor.execute("SELECT username, name, surname, form_class, ip FROM users WHERE online_status = 1")
            online_users = cursor.fetchall()

            conn.close()

            if online_users: 
                online_data = ""
                for user in online_users:
                    user_info = ",".join(user) # Converting to Tuple to a string because I cant send Tuples over a socket.
                    online_data += user_info + "\n"

                client_socket.sendall(online_data.encode())
            else:
                client_socket.sendall("".encode())

        else:
            print (data)
            save_to_database(data)
            client_socket.sendall("Registration successful!".encode())
        
        client_socket.close()

if __name__ == "__main__":
    run_server()    




