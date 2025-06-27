import sqlite3
from werkzeug.security import generate_password_hash
from app.config import Config

database_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH

def initialize_database(database_path):
    conn = sqlite3.connect(database_path)
    curr = conn.cursor()

    # ----------------------------
    # USERS
    # ----------------------------
    curr.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        number_phone TEXT NOT NULL,
        website_company TEXT NOT NULL,
        birth_date DATE NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE,
        balance FLOAT DEFAULT 10.00,
        pending_loan_amount FLOAT DEFAULT 0.00,
        pending_loan_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # ----------------------------
    # ADMINS
    # ----------------------------
    curr.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        number_phone TEXT NOT NULL,
        website_company TEXT NOT NULL,
        birth_date DATE NOT NULL,
        is_admin BOOLEAN DEFAULT TRUE,
        balance FLOAT DEFAULT 1000.00,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # ----------------------------
    # Sample Data
    # ----------------------------
    root_pass = generate_password_hash("root123")
    admin_pass = generate_password_hash("admin123")
    guest_pass = generate_password_hash("guest123")

    users_data = [
        ("guest", guest_pass, "guest@example.com", "Guest", "345", "095358553", "example.com", "1990-03-11", 0, 10.00, 0.00, 0)
    ]
    
    admins_data = [
        ("root", root_pass, "root@example.com", "Root", "123", "092316186", "coding.example.com", "1990-03-11", 1, 1000.00),
        ("admin", admin_pass, "admin@example.com", "Admin", "898", "098285213", "labs.example.com", "1990-03-11", 1, 1000.00 ) #balance = 1e100
    ]

    curr.executemany('''
        INSERT OR IGNORE INTO users (
            username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin, balance, pending_loan_amount, pending_loan_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)

    curr.executemany('''
        INSERT OR IGNORE INTO admins (
            username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin, balance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', admins_data)

    conn.commit()
    conn.close()
