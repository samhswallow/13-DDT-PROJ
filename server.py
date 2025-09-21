"""This code builds a SOCKET server running on a TCP protocol using a IPv4
connection. I use a command dispatch system where I have stylised commands 
that the student sends to the server. These commands request access to certain 
types of data needed to run and process the software. The server also handels 
login data and stores the passwords hashed. """ 


# Networking
import socket

# Database
import sqlite3

# Password hashing
from argon2 import PasswordHasher


# Initialize Argon2 password hasher
ph = PasswordHasher()


def create_database():
    """Create the SQLite database and users table if not exists."""
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Create users table if it does not already exist
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
    """)

    conn.commit()
    conn.close()


def save_to_database(data):
    """Save registration data to the database, hashing passwords."""
    try:
        # Split comma-separated values into fields
        username, name, surname, form_class, password, ip = data.split(",")

        # Hash the password with Argon2
        password = ph.hash(password)

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        # Insert new user record (online_status set to 0 initially)
        cursor.execute("""
            INSERT INTO users (
                username, name, surname, form_class,
                password, ip, online_status
            )
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (username, name, surname, form_class, password, ip))

        conn.commit()
        conn.close()
        print(f"[+] Saved {username} with online_status = 0.")
    except sqlite3.IntegrityError:
        print(f"[!] Username '{username}' or IP '{ip}' already exists.")
    except Exception as e:
        print(f"[!] Error saving to database: {e}")


def login_protocol(data):
    """Handle login requests and update online status."""
    global login_value
    login_value = False

    # Expecting format: LOGIN,username,password
    parts = data.split(",")
    if len(parts) < 3:
        print("[!] Invalid LOGIN command format")
        return

    username = parts[1]
    entered_password = parts[2]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Get stored password hash for user
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    if not result:
        print("[!] User not found")
        conn.close()
        return

    stored_hash = result[0]

    try:
        # Verify password
        if ph.verify(stored_hash, entered_password):
            login_value = True
            print(f"[+] Login successful: {username}")

            # Mark user as online
            cursor.execute("""
                UPDATE users
                SET online_status = 1
                WHERE username = ?
            """, (username,))
            conn.commit()
        else:
            print("[!] Incorrect password")
    except Exception:
        print("[!] Password check failed")

    conn.close()


def register_offline(ip):
    """Mark a user as offline by IP address."""
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE ip = ?", (ip,))
    user = cursor.fetchone()

    if user:
        # Set online_status to 0
        cursor.execute("""
            UPDATE users
            SET online_status = 0
            WHERE ip = ?
        """, (ip,))
        conn.commit()
        print(f"[+] User with IP {ip} is now offline.")
    else:
        print(f"[!] No user found with IP {ip}.")

    conn.close()


def run_server():
    """
    Runs the central server. Uses TCP connections to handle client 
    requests on a IPv4 connection. 

    The server listens on port 6060 and accepts TCP connections. The server 
    supports connections, requesting links, authetication , user info 
    and registration. The user data is stored in the SQLite database, 
    `students.db`.

    Commands:
        LOGIN,<username>,<password>:
            Validates login credentials and returns success or failure.
        CONNECT,<username>,<link>:
            Sends a saved link to the target user if they are online.
        DELETE,<username>:
            Instructs the target user's client to delete its saved links.
        OFFLINE,<ip>:
            Marks the given IP address as offline in the database.
        SCAN_NETWORK:
            Returns a list of all currently online users with their details.
        <other>:
            Treated as a new user registration attempt and stored in the database.

    Raises:
        OSError: If the server socket fails to bind or accept connections.
        sqlite3.Error: If there is a database access issue.
        Exception: For unexpected errors when handling client requests.

    Note:
        This function runs an infinite loop and does not return. It should
        be running in its own process behind other programs. 
    """

    create_database()

    # TCP socket server on port 6060 using IPV4
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 6060))
    s.listen(5)
    print("[*] Server listening on 0.0.0.0:6060")

    while True:
        client_socket, addr = s.accept()
        print(f"[+] Connection from {addr}")

        # Receive command from client
        data = client_socket.recv(2048).decode("utf-8").strip()
        print("[*] Received:", data)

        # Handle commands
        if data.startswith("LOGIN"):
            login_protocol(data)
            if login_value:
                client_socket.sendall("SUCCESS Login successful!".encode())
            else:
                client_socket.sendall("Invalid username or password.".encode())

        elif data.startswith("CONNECT"):
            # CONNECT,<username>,<link>
            parts = data.split(",", 2)
            if len(parts) == 3:
                _, username, saved_link = parts
                username = username.strip()
                saved_link = saved_link.strip()

                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()

                # Find target user IP if online
                cursor.execute("""
                    SELECT ip
                    FROM users
                    WHERE username = ?
                      AND online_status = 1
                """, (username,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    target_ip = result[0]
                    print(f"[+] Found '{username}' ({target_ip}) Online.")

                    try:
                        # Send link to target user's client (port 6061)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                            send_sock.connect((target_ip, 6061))
                            send_sock.sendall(saved_link.encode())
                        print(f"[+] Link sent to {username}")
                    except Exception as e:
                        client_socket.sendall(f"Failed to send link: {e}".encode())
                        print(f"[!] Failed to send link: {e}")
                else:
                    client_socket.sendall(f"User '{username}' not found.".encode())
                    print(f"[!] User '{username}' not found.")
            else:
                client_socket.sendall("Invalid CONNECT command format.".encode())
                print("[!] Invalid CONNECT command format")

        elif data.startswith("DELETE"):
            # DELETE,<username>
            parts = data.split(",", 1)
            username = parts[1].strip()

            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            # Get IP of target user if online
            cursor.execute("""
                SELECT ip
                FROM users
                WHERE username = ?
                  AND online_status = 1
            """, (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                target_ip = result[0]
                print(f"[+] Deleting links for '{username}'.")

                try:
                    # Tell client to delete links
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                        send_sock.connect((target_ip, 6061))
                        send_sock.sendall("DELETE".encode())
                except Exception as e:
                    client_socket.sendall(f"Failed to delete links: {e}".encode())
                    print(f"[!] Failed to delete links: {e}")
            else:
                client_socket.sendall(f"User '{username}' not found.".encode())
                print(f"[!] User '{username}' not found.")

        elif data.startswith("OFFLINE"):
            # OFFLINE,<ip>
            ip = data.split(",")[1]
            register_offline(ip)
            client_socket.sendall(f"IP {ip} registered as offline.".encode())

        elif data == "SCAN_NETWORK":
            # Return list of all online users
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT username, name, surname, form_class, ip
                FROM users
                WHERE online_status = 1
            """)
            online_users = cursor.fetchall()
            conn.close()

            if online_users:
                online_data = "\n".join(",".join(user) for user in online_users)
                client_socket.sendall(online_data.encode())
            else:
                client_socket.sendall("".encode())

        else:
            # Treat anything else as a registration attempt
            print(data)
            save_to_database(data)
            client_socket.sendall("Registration successful!".encode())

        client_socket.close()


if __name__ == "__main__":
    run_server()



