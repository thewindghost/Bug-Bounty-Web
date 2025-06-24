import sqlite3
from werkzeug.security import generate_password_hash
from app.config import Config

database_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH

def initialize_database(database_path):
    # Kết nối DB
    conn = sqlite3.connect(database_path)
    curr = conn.cursor()

    # ----------------------------
    # TẠO BẢNG USERS
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
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # ----------------------------
    # TẠO BẢNG ADMINS
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
        is_admin INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # ----------------------------
    # TẠO USER VÀ ADMIN DỮ LIỆU MẪU
    # ----------------------------
    # Tạo mật khẩu đã hash
    root_pass = generate_password_hash("root123")
    admin_pass = generate_password_hash("admin123")
    guest_pass = generate_password_hash("guest123")

    # Thêm admin: root, admin
    curr.execute('''
    INSERT OR IGNORE INTO admins (username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("root", root_pass, "root@example.com", "Root", "User", "092316186", "coding.example.com", "1990-03-11", 1))

    curr.execute('''
    INSERT OR IGNORE INTO admins (username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("admin", admin_pass, "admin@example.com", "Admin", "User", "098285213", "labs.example.com", "1990-03-11", 1))

    # Thêm user: guest
    curr.execute('''
    INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("guest", guest_pass, "guest@example.com", "Guest", "User", "095358553", "example.com", "1990-03-11", 0))

    # Lưu và đóng DB
    conn.commit()
    conn.close()
