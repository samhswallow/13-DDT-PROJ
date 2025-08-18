import socket
import sqlite3


def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
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
    try:
        username, name, surname, form_class, password, ip = data.split(",")
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, name, surname, form_class, password, ip, online_status)
            VALUES (?, ?, ?, ?, ?, ?, 0)
        """, (username, name, surname, form_class, password, ip))

        conn.commit()
        conn.close()
        print(f"[+] Saved {username} to database with online_status = 0.")
    except sqlite3.IntegrityError:
        print(f"[!] Username '{username}' or IP '{ip}' already exists.")
    except Exception as e:
        print(f"[!] Error saving to database: {e}")

def login_protocol(data):
    global login_value
    login_value = False
    parts = data.split(",")
    username = parts[1]
    password = parts[2]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    if user:
        login_value = True
        print("Login successful for user:", username)

        cursor.execute("""
            UPDATE users SET online_status = 0 WHERE username = ?
        """, (username,))
        conn.commit()
    else:
        print("Invalid username or password.")

    conn.close()

def register_online(ip):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE ip = ?", (ip,))
    user = cursor.fetchone()

    if user:
        cursor.execute("""
            UPDATE users SET online_status = 1 WHERE ip = ?
        """, (ip,))
        conn.commit()
        print(f"[+] User with IP {ip} is now online.")
    else:
        print(f"[!] No user found with IP {ip}.")

    conn.close()

def run_server():
    create_database()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 6060))
    s.listen(5)
    print("[*] Server is listening on 10.17.1.39:6060")

    while True:
        client_socket, addr = s.accept()
        print(f"[+] Connection from {addr}")
        data = client_socket.recv(2048).decode("utf-8").strip()
        print("[*] Received:", data)

        if data.startswith("LOGIN"):
            login_protocol(data)
            if login_value:
                client_socket.sendall("SUCCESS Login successful!".encode())
            else:
                client_socket.sendall("Invalid username or password.".encode())

        elif data.startswith("ONLINE,"):
            ip = data.split(",")[1]
            register_online(ip)
            client_socket.sendall(f"IP {ip} registered as online.".encode())

        elif data.startswith("CONNECT"):
            parts = data.split(",", 2)
            if len(parts) == 3:
                command = parts[0]
                username = parts[1].strip()
                saved_link = parts[2].strip()

                conn = sqlite3.connect("students.db")
                cursor = conn.cursor()

                cursor.execute("SELECT ip FROM users WHERE username = ?", (username,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    target_ip = result[0]
                    print(f"[+] Found user '{username}' with IP {target_ip}. Sending saved link...")

                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                            send_sock.connect((target_ip, 6060))  
                            send_sock.sendall(saved_link.encode())
                        client_socket.sendall(f"Link sent to {username}.".encode())
                        print(f"[+] Link sent to {username}")
                    except Exception as e:
                        client_socket.sendall(f"Failed to send link to {username}: {e}".encode())
                        print(f"[!] Failed to send link to {username}: {e}")
                else:
                    client_socket.sendall(f"User '{username}' not found.".encode())
                    print(f"[!] User '{username}' not found.")
            else:
                client_socket.sendall("Invalid CONNECT command format.".encode())
                print("[!] Invalid CONNECT command format")

        elif data == "SCAN_NETWORK":
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()

            cursor.execute("SELECT username, name, surname, form_class, ip FROM users WHERE online_status = 1")
            online_users = cursor.fetchall()

            conn.close()

            if online_users:
                online_data = ""
                for user in online_users:
                    user_info = ",".join(user)
                    online_data += user_info + "\n"

                client_socket.sendall(online_data.encode())
            else:
                client_socket.sendall("No users are online.".encode())

        else:
            print(data)
            save_to_database(data)
            client_socket.sendall("Registration successful!".encode())

        client_socket.close()

if __name__ == "__main__":
    run_server()






