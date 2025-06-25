

<!-- AUTO-GENERATED: BEGIN -->

# In Process
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

This project is licensed under the [GNU AGPLv3 License](LICENSE).

© 2025 thewindghost. All rights reserved.
---

## 🐞 Vulnerability Catalogue

This repository intentionally includes many security bugs discovered during my bug bounty hunting.
**Do NOT deploy to production, but you can practice in here for pentest skills.**

---
## How can Build ?

### Build for developer
```bash
python => 3.10 version
pip install -r requirements.txt
python3 ./run.py or python.exe ./run.py
```
---

### Build with docker-compose for security researcher
```bash
docker-compose up -d && docker-compose build
```
---

### Note 1: if you have updated the code from local and want docker container to have that code. Run the docker-compose build command again
#### Warning: There is a tool to clean all unused docker containers and docker images, use with caution.
```bash
sh clean_docker_not_using.sh && docker-compose build && docker-compose up -d
```

### Note 2: Since updating code into README.md is quite time consuming, I created a tool to update all code into it and just click run. It will automatically generate README.md summarizing all code in the folder.
```bash
python.exe ./create_readme_md.py or python3 ./create_readme_md.py
```
---

## 📁 Project Structure

```text
├── .dockerignore
├── .env.example
├── .gitattributes
├── .gitignore
├── Dockerfile
├── clean_docker_not_using.sh
├── docker-compose.yml
├── requirements.txt
├── run.py
├── wsgi.py
└── app/
    ├── __init__.py
    ├── config.py
    ├── controllers/
    │   ├── __init__.py
    │   ├── admin/
    │   │   ├── check_login.py
    │   │   └── read_logs.py
    │   ├── api/
    │   │   ├── clear_logs_admin.py
    │   │   ├── get_admin_info_by_post.py
    │   │   ├── get_current_admin_info_id.py
    │   │   ├── get_current_user_info_id.py
    │   │   └── get_user_info_by_post.py
    │   └── user/
    │       ├── update_balance.py
    │       └── update_setting.py
    ├── database/
    │   ├── __init__.py
    │   ├── connect_database.py
    │   └── init_db.py
    ├── http/
    │   ├── nginx.conf
    │   └── ssl/
    ├── logs/
    │   └── logs.txt
    ├── routes/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── api.py
    │   ├── auth.py
    │   ├── error_pages.py
    │   ├── main.py
    │   └── user.py
    ├── services/
    │   ├── __init__.py
    │   ├── get_token.py
    │   ├── send_email.py
    │   ├── update_user_profile.py
    │   └── write_log_entries.py
    ├── static/
    │   ├── robots.txt
    │   ├── script-js/
    │   │   ├── clear_logs_admin.js
    │   │   ├── get_balance_user.js
    │   │   ├── get_information_admin.js
    │   │   ├── get_information_user.js
    │   │   ├── redirect_referer.js
    │   │   └── update_setting_user.js
    │   └── styles/
    │       ├── style1.css
    │       └── style2.css
    ├── templates/
    │   ├── admin/
    │   │   ├── control_panel.html
    │   │   ├── login_admin.html
    │   │   ├── logs.html
    │   │   └── profile_admin.html
    │   ├── auth/
    │   │   ├── login.html
    │   │   ├── logout.html
    │   │   ├── register.html
    │   │   ├── reset_password.html
    │   │   └── reset_token.html
    │   ├── error_pages/
    │   │   └── 403.html
    │   ├── index.html
    │   └── user/
    │       ├── dashboard.html
    │       ├── profile_user.html
    │       ├── setting_user.html
    │       └── wallet.html
    └── utils/
        ├── __init__.py
        ├── check_xml_encoding.py
        ├── decorator_admin.py
        └── decorator_user.py
```

### `clean_docker_not_using.sh`
```sh
#!/bin/sh
docker container prune -f
docker image prune -a -f
```

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  bug_bounty_web:
    build: .
    container_name: bug_bounty_web_app
    restart: always
    expose:
      - 5505
    volumes:
      - .:/bug_bounty_web
    depends_on:
      - nginx

  nginx:
    image: nginx:latest
    container_name: nginx_proxy
    restart: always
    ports:
      - "80:80"
    #  - "443:443"
    volumes:
      - ./app/http/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    # - ./app/http/ssl:/etc/nginx/ssl:ro
```

### `requirements.txt`
```text
Flask
blueprint
Flask-Mail
Flask-Caching
itsdangerous
python-dotenv
bleach
lxml
gunicorn
```

### `run.py`
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5505)
```

### `wsgi.py`
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5505)
```

### `app\__init__.py`
```python
from flask import Flask
from flask_mail import Mail
from flask_caching import Cache
from app.config import Config
from app.database import connect_database

mail = Mail()
cache = Cache()

def create_app():
    app = Flask(__name__, instance_relative_config=False, static_url_path="/static", static_folder="static")

    app.config.from_object(Config)

    # Khởi tạo các extension với app
    Config.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Khởi tạo module database (sẽ tự động tạo DB nếu chưa có)
    connect_database.init_app(app)

    # Đăng ký Blueprints
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.error_pages import error_pages_bp
    from app.routes.main import main_bp
    from app.routes.user import user_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(error_pages_bp, url_prefix='/error_pages')
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    return app
```

### `app\config.py`
```python
from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY')
    CACHE_TYPE = os.getenv('CACHE_TYPE')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT'))

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_SENDER_EMAIL')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')

    LOG_FILE_RELATIVE_PATH = os.getenv('LOG_FILE_RELATIVE_PATH')
    INIT_DB_FILE_RELATIVE_PATH = os.getenv('INIT_DB_FILE_RELATIVE_PATH')
    DB_CONNECTION_FILE_RELATIVE_PATH = os.getenv('DB_CONNECTION_FILE_RELATIVE_PATH')

    @classmethod
    def init_app(cls, app):

        pass
```

### `app\controllers\__init__.py`
```python
```

### `app\controllers\admin\check_login.py`
```python
from flask import session, request, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from app.database.connect_database import get_db_connection
from bleach import clean

def check_login_admin():

    error = None

    username = request.form.get('username', '')
    raw_password = clean(request.form.get('password', ''))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, is_admin, password FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row[2], raw_password):
        session['username'] = row[0]
        session['is_admin'] = bool(row[1])

        if session.get('is_admin') == True:
            return redirect(url_for('admin.admin_panel'))

    else:
        error = "Invalid Username or Password"

    return render_template('admin/login_admin.html', error=error)
```

### `app\controllers\admin\read_logs.py`
```python
from flask import render_template
from app.config import Config
import os


def read_logs_info():
    try:
        if not os.path.exists(Config.LOG_FILE_RELATIVE_PATH):
            return "Not Found File Logs", 404

        with open(Config.LOG_FILE_RELATIVE_PATH, 'r') as f:
            log_data = f.read()

        entries = log_data.strip().split("---------------------------")
        entries = [e.strip() for e in entries if e.strip()]

        return render_template("admin/logs.html", entries=entries)

    except Exception as e:
        return f"Error reading logs: {str(e)}", 500
```

### `app\controllers\api\clear_logs_admin.py`
```python
from flask import jsonify
from app.config import Config
import os

def clear_logs_admin():

    try:
        log_file = Config.LOG_FILE_RELATIVE_PATH

        if not os.path.exists(log_file):
            return jsonify({"status": "error", "message": "Log file not found."}), 404

        open(log_file, 'w').close()

        return jsonify({"status": "success", "message": "Logs cleared successfully."}), 200

    except Exception as e:
        e = "Internal Server Error"
        return jsonify({"status": "error", "message": str(e)}), 500
```

### `app\controllers\api\get_admin_info_by_post.py`
```python
import sqlite3
from flask import request, jsonify
from app.config import Config

def get_information_admin():

    try:
        admin_id_raw = request.form.get('admin_id')

        if admin_id_raw is None:
            return jsonify({"error": "Missing admin_id"}), 400

        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        admin_id = int(admin_id_raw)
        cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            admin_data = {
                "id": row["id"],
                "username": row["username"],
                "password": row["password"],
                "email": row["email"],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'number_phone': row['number_phone'],
                'website_company': row['website_company'],
                'birth_date': row['birth_date'],
                'is_admin': row['is_admin'],
                'balance': row['balance'],
                'created_at': row['created_at']
            }
            return jsonify({"admin_data": admin_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
```

### `app\controllers\api\get_current_admin_info_id.py`
```python
import sqlite3
from flask import jsonify, session
from app.config import Config

def get_current_admin_info():

    try:
        username = session.get('username')
        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            admin_data = {
                "id": row["id"],
                "username": row["username"],
                "password": row["password"],
                "email": row["email"],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'number_phone': row['number_phone'],
                'website_company': row['website_company'],
                'birth_date': row['birth_date'],
                'is_admin': row['is_admin'],
                'balance': row['balance'],
                'created_at': row['created_at']
            }
            return jsonify({"user_data": admin_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
```

### `app\controllers\api\get_current_user_info_id.py`
```python
import sqlite3
from flask import jsonify, session
from app.config import Config

def get_current_user_info():

    try:
        username = session.get('username')
        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user_data = {
                "id": row["id"],
                "username": row["username"],
                "password": row["password"],
                "email": row["email"],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'number_phone': row['number_phone'],
                'website_company': row['website_company'],
                'birth_date': row['birth_date'],
                'is_admin': row['is_admin'],
                'balance': row['balance'],
                'created_at': row['created_at']
            }
            return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
```

### `app\controllers\api\get_user_info_by_post.py`
```python
import sqlite3
from flask import request, jsonify
from app.config import Config

def get_user_info_by_id():

    try:
        user_id_raw_post = request.form.get('user_id')

        if user_id_raw_post is None:
            return jsonify({"error": "Missing user_id"}), 400


        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        user_id_post = int(user_id_raw_post)
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id_post,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user_data = {
                "id": row["id"],
                "username": row["username"],
                "password": row["password"],
                "email": row["email"],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'number_phone': row['number_phone'],
                'website_company': row['website_company'],
                'birth_date': row['birth_date'],
                'is_admin': row['is_admin'],
                'balance': row['balance'],
                'created_at': row['created_at']
            }
            return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
```

### `app\controllers\user\update_balance.py`
```python
from flask import request, render_template

def update_balance_user():

    try:
        if request.method == 'POST':
            balance = request.form.get('balance', '')
            eval(balance)
            return render_template('user/wallet.html', result=balance)

    except Exception as e:
            error = 'Internal Server error', 500
            return render_template('user/wallet.html', error=error)
```

### `app\controllers\user\update_setting.py`
```python
from flask import request, render_template, session, render_template_string
from app.utils.check_xml_encoding import get_xml_encoding_lxml
from app.services.write_log_entries import count_log_entries
from werkzeug.security import generate_password_hash
from app.services.update_user_profile import update_user_profile
from lxml import etree
from app.config import Config
from datetime import datetime
from bleach import clean

def handle_setting_user():

    try:
        if not request.content_type.startswith('application/xml'):
            return render_template('user/setting_user.html', error="Invalid content type. Only application/xml is accepted.")

        raw_data = request.data
        if not raw_data:
            raise ValueError("No XML data provided.")

        encoding = get_xml_encoding_lxml(raw_data)
        if encoding.lower() != 'utf-8':
            return render_template('user/setting_user.html', error=f"Only UTF-8 is allowed. Got: {encoding}")

        update_setting_V1 = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
        root_V1 = etree.fromstring(raw_data, parser=update_setting_V1)
        update_setting_V2 = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
        root_V2 = etree.fromstring(raw_data, parser=update_setting_V2)

        #username = clean(render_template_string(session.get("username")))
        username = session.get("username")
        is_admin = session.get("is_admin")
        new_email = root_V2.findtext("email")
        new_birth_date = root_V2.findtext("birth_date")
        new_setting = root_V1.findtext("setting")
        new_raw_password = root_V2.findtext("password")

        entry_number = count_log_entries(Config.LOG_FILE_RELATIVE_PATH) + 1
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        log_entry = (
            f"\n[Entry #{entry_number}]\n"
            f"Username: {username} | Is_admin: {is_admin}\n"
            f"New Email: {new_email}\n"
            f"Birth Date: {new_birth_date}\n"
            f"Setting: {new_setting}\n"
            f"Password: {new_raw_password}\n"
            f"Time: {timestamp}\n"
            f"---------------------------\n"
        )
        with open(Config.LOG_FILE_RELATIVE_PATH, "a") as f:
            f.write(log_entry)

        new_password = generate_password_hash(new_raw_password)

        success_update = update_user_profile(
            username=username,
            email=new_email,
            birth_date=new_birth_date,
            password=new_password
        )

        if not success_update:
            return render_template("user/setting_user.html", error="No fields updated.")

        return render_template("user/setting_user.html", success="Your settings were updated.")

    except Exception as e:
        e = "Internal Server Error", 500
        return render_template("user/setting_user.html", error=e)
```

### `app\database\__init__.py`
```python
```

### `app\database\connect_database.py`
```python
import sqlite3
import os

from flask import g
from app.config import Config
from app.database.init_db import initialize_database

def get_db_connection():
    """
    Opens a SQLite database connection and caches it on flask.g.
    """
    if 'db_conn' not in g:
        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        g.db_conn = conn
    return g.db_conn


def close_db_connection(e=None):
    """
    Closes the SQLite database connection if it exists.
    """
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()


def _initialize_database_file():
    """
    Creates the database file and initializes schema if it doesn't exist.
    """
    db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
    if not os.path.exists(db_path):
        try:
            initialize_database(db_path)
        except Exception as e:
            print(f"[ERROR] Failed to initialize database: {e}")
            raise


def init_app(app):
    """
    Registers teardown and ensures the database file exists on startup.
    """
    app.teardown_appcontext(close_db_connection)
    with app.app_context():
        _initialize_database_file()
```

### `app\database\init_db.py`
```python
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
        balance FLOAT DEFAULT 10.00,
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
        balance FLOAT DEFAULT 1000.00,
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

    users_data = [
        ("guest", guest_pass, "guest@example.com", "Guest", "User", "095358553", "example.com", "1990-03-11", 0, 10.00)
    ]
    admins_data = [
        ("root", root_pass, "root@example.com", "Root", "User", "092316186", "coding.example.com", "1990-03-11", 1, 1000.00),
        ("admin", admin_pass, "admin@example.com", "Admin", "User", "098285213", "labs.example.com", "1990-03-11", 1, 1000.00)
    ]

    curr.executemany('''
        INSERT OR IGNORE INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)

    curr.executemany('''
        INSERT OR IGNORE INTO admins (username, password, email, first_name, last_name, number_phone, website_company, birth_date, is_admin, balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', admins_data)

    # Lưu và đóng DB
    conn.commit()
    conn.close()
```

### `app\http\nginx.conf`
```config
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://bug_bounty_web:5505;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### `app\logs\logs.txt`
```text
```

### `app\routes\__init__.py`
```python
```

### `app\routes\admin.py`
```python
from flask import Blueprint, render_template, session, request
from app.utils.decorator_admin import admin_required
from app.controllers.admin.read_logs import read_logs_info
from app.controllers.admin.check_login import check_login_admin

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':
        return check_login_admin()

    return render_template('admin/login_admin.html')

@admin_bp.route('/control-panel', methods=['GET', 'POST'])
@admin_required
def admin_panel():

    return render_template('admin/control_panel.html', username=session.get('username'))

@admin_bp.route('/logs', methods=['GET'])
@admin_required
def read_logs():

    return read_logs_info()

@admin_bp.route('/profile', methods=['GET', 'POST'])
@admin_required
def admin_profile():

    return render_template('admin/profile_admin.html', username=session.get('username'))
```

### `app\routes\api.py`
```python
from flask import Blueprint, request
from app.controllers.api.get_admin_info_by_post import get_information_admin
from app.controllers.api.get_user_info_by_post import get_user_info_by_id
from app.controllers.api.get_current_user_info_id import get_current_user_info
from app.controllers.api.get_current_admin_info_id import get_current_admin_info
from app.controllers.api.clear_logs_admin import clear_logs_admin
from app.utils.decorator_admin import admin_required
from app.utils.decorator_user import user_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/v1/information_users', methods=['GET', 'POST'])
@user_required
def information_user():

    if request.method == 'POST':
        return get_user_info_by_id()

    return get_current_user_info()

################################################################
@api_bp.route('/v1/information_admin', methods=['GET', 'POST'])
@admin_required
def information_admin():

    if request.method == 'POST':
        return get_information_admin()

    return get_current_admin_info()

@api_bp.route('/v1/clear_logs', methods=['POST'])
def clear_logs():

    return clear_logs_admin()
```

### `app\routes\auth.py`
```python
from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.connect_database import get_db_connection
from app.services.get_token import get_token_serializer
from itsdangerous import BadSignature, SignatureExpired
from app.services.send_email import send_reset_email
from .. import cache
from bleach import clean

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':

        username = request.form.get('username', '')
        raw_password = clean(request.form.get('password', ''))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, is_admin, password FROM users WHERE username = '" + username + "'")
        row = cursor.fetchone()
        conn.close()

        if row and check_password_hash(row[2], raw_password):
            session['username'] = row[0]
            session['is_admin'] = bool(row[1])
            return redirect(url_for('user.user_dashboard'))

        else:
            error = "Invalid Username or Password"

    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    error = None

    if request.method == 'POST':

        try:
            username = request.form.get('username', '').strip()
            raw_password = clean(request.form.get('password', '')).strip()
            hased_password = generate_password_hash(raw_password)
            email = clean(request.form.get('email', '')).strip()
            first_name = clean(request.form.get('first_name', '')).strip()
            last_name = clean(request.form.get('last_name', '')).strip()
            number_phone = clean(request.form.get('number_phone', '')).strip()
            website_company = clean(request.form.get('website_company', '')).strip()
            birth_date = clean(request.form.get('birth_date', ''))

            # Open connection to database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
            existing_user = cursor.fetchone()

            if existing_user:
                error = "Username already exists. Please a defferent one."
                return render_template('auth/register.html', error=error)

            # Add new user to database
            cursor.execute('''
                INSERT INTO users (username, password, email, first_name, last_name, number_phone, website_company, birth_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, hased_password, email, first_name, last_name, number_phone, website_company, birth_date))

            conn.commit()
            conn.close()

            # Register successfully
            success = 'Register Successfully'
            return render_template('auth/register.html', success=success)

        except Exception as e:
            error = str(e)
            return render_template('auth/register.html', error=error)

    return render_template('auth/register.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        # Check rate limit with cache
        if cache.get(f'reset_mail_sent_{email}'):
            Notification = 'Please wait at least 5 minutes before requesting another password reset email.'
            return render_template('auth/reset_password.html', Notification=Notification)

        conn = get_db_connection()
        account = conn.execute("SELECT id FROM accounts WHERE email = ?", (email,)).fetchone()
        conn.close()

        if account:
            account_id = account['id']
            serializer = get_token_serializer()
            token = serializer.dumps({'account_id': account_id})
            reset_url = url_for('perform_password_reset', token=token, _external=True)

            send_reset_email(email, reset_url)

            # Email is saved in cache and wait 5 minutes before resetting password again
            cache.set(f'reset_mail_sent_{email}', True, timeout=300)

        Notification = 'If that email is registered, you will receive a password reset link shortly'
        return render_template('auth/reset_password.html', Notification=Notification)

    return render_template('auth/reset_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def perform_password_reset(token):

    # Check if token was already used
    if cache.get(f'token_used_{token}'):

        Notification = 'This reset link has already been used.'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    serializer = get_token_serializer()

    try:
        data = serializer.loads(token, max_age=3600)
        account_id = data.get('account_id')

    except SignatureExpired:
        Notification = 'The reset link has expired. Please request a new one'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    except BadSignature:
        Notification = 'The reset link is invalid. Please request a new one.'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    if request.method == 'POST':
        new_password = request.form.get('password', '').strip()

        if not new_password:
            Notification = "Password can't be empty."
            return render_template('auth/reset_token.html', Notification=Notification)

        hashed_password = generate_password_hash(new_password)
        conn = get_db_connection()

        conn.execute(
            'UPDATE accounts SET password = ? WHERE id = ?', (hashed_password, account_id)
        )

        conn.commit()
        conn.close()

        # Mark token as used
        cache.set(f'token_used_{token}', True, timeout=1800)  # Chặn dùng lại trong thời gian token còn hiệu lực

        Notification2 = 'Your Password has been Updated. You may now log in.'
        return render_template('auth/reset_token.html', Notification2=Notification2, show_form=False)

    return render_template('auth/reset_token.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():

    session.clear()
    running_value = request.args.get('running', 'True')
    response = make_response(render_template('auth/logout.html', running=running_value))
    response.delete_cookie('session')
    return response
```

### `app\routes\error_pages.py`
```python
from flask import Blueprint, render_template

error_pages_bp = Blueprint('error_pages', __name__)

@error_pages_bp.route('/403', methods=['GET'])
def page_403():

    return render_template('error_pages/403.html')
```

### `app\routes\main.py`
```python
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')
```

### `app\routes\user.py`
```python
from flask import Blueprint, render_template, request, session
from bleach import clean
from app.utils.decorator_user import user_required
from app.controllers.user.update_setting import handle_setting_user
from app.controllers.user.update_balance import update_balance_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/setting', methods=['GET', 'POST'])
@user_required
def user_parser_info():

    if request.method == 'POST':
        return handle_setting_user()

    return render_template('user/setting_user.html')

@user_bp.route('/wallet', methods=['GET', 'POST'])
@user_required
def user_update_balance():

    if request.method == 'POST':
        error = "Sorry Code Backend Not Found"
        return render_template('user/wallet.html', error=error)

    return render_template('user/wallet.html')

@user_bp.route('/profile', methods=['GET', 'POST'])
@user_required
def user_profile():

    return render_template('user/profile_user.html', template_rendered=session['username'])

@user_bp.route('/dashboard', methods=['GET'])
@user_required
def user_dashboard():

    return render_template('user/dashboard.html', username=session['username'])
```

### `app\services\__init__.py`
```python
```

### `app\services\get_token.py`
```python
from itsdangerous import URLSafeSerializer
from app.config import Config

def get_token_serializer():
    return URLSafeSerializer(Config.SECRET_KEY)
```

### `app\services\send_email.py`
```python
from flask_mail import Message
from threading import Thread
from flask import current_app
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_reset_email(email, reset_url):
    msg = Message(
        subject='Your Account Password Reset',
        recipients=[email]
    )
    msg.body = (
        'Hello, \n\n'
        'You requested a password reset. Click the link below to set a new password. \n'
        f'{reset_url}\n\n'
        'If you did not request this, please ignore this mail'
    )
    thread = Thread(target=send_async_email, args=(current_app._get_current_object(), msg))
    thread.start()
```

### `app\services\update_user_profile.py`
```python
import sqlite3
from app.config import Config

def update_user_profile(username, email=None, birth_date=None, password=None):
    db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    update_fields = []
    values = []

    if email:
        update_fields.append("email = ?")
        values.append(email)
    if birth_date:
        update_fields.append("birth_date = ?")
        values.append(birth_date)
    if password:
        update_fields.append("password = ?")
        values.append(password)

    if not update_fields:
        conn.close()
        return False

    values.append(username)
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE username = ?"

    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return True
```

### `app\services\write_log_entries.py`
```python
from app.config import Config

log_file_path = Config.LOG_FILE_RELATIVE_PATH

def count_log_entries(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        entries = content.split('---------------------------')
        return len([e for e in entries if e.strip()])
    except FileNotFoundError:
        return 0
```

### `app\static\robots.txt`
```text
User-agent: *
Disallow: /admin-panel-131315315211
Disallow: /admin-panel-131315315211/logs

User-agent: *
allow: /
allow: /register
allow: /login
allow: /dashboard
allow: /profile
allow: /parser-info
allow: /balances
allow: /reset-password
allow: /logout
```

### `app\static\styles\style1.css`
```css
/* Light Mode - Harmonized Version */

*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  width: 100%;
  min-height: 100%;
  font-family: 'Roboto', sans-serif;
  background: #f7f9fc;
  color: #2d3e50;
  line-height: 1.5;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  font-size: 16px;
}

.card {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border: 1px solid #d3e3fc;
  border-radius: 12px;
  box-shadow: 0 0 18px rgba(74, 144, 226, 0.2);
  overflow: hidden;
  padding: 25px;
  margin: 0 auto;
}

/* Header */
.card header {
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #d3e3fc;
}
.card header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: #4a90e2;
}
.card header p {
  font-size: 1rem;
  color: #4a5568;
}

/* Menu */
.menu {
  list-style: none;
  padding: 0;
  margin: 25px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu li a {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #2d3e50;
  font-weight: 500;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: #e3edf7;
  transition: background 0.2s, color 0.2s;
}

.menu li a:hover {
  background-color: #d0e2f0;
  color: #4a90e2;
}

.menu li:last-child a {
  background-color: #ffe5e5;
  color: #e74c3c;
}

.menu li:last-child a:hover {
  background-color: #fddede;
  color: #c0392b;
}

/* Profile Info Box */
.profile-info {
  background: #f2f8fd;
  border: 1px solid #d3e3fc;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow-x: auto;
  word-break: break-word;
}
.profile-info p {
  font-size: 1rem;
  color: #2d3e50;
}

/* Form */
.card form {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px 30px;
  align-items: center;
  margin-bottom: 20px;
}
.card form label {
  font-size: 1rem;
  font-weight: 600;
  justify-self: end;
  color: #4a4a4a;
}
.card form input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #c3cfe2;
  border-radius: 10px;
  font-size: 1rem;
  background-color: #fff;
  color: #2d3e50;
}
.card form input:focus {
  border-color: #4a90e2;
  outline: none;
  box-shadow: 0 0 6px rgba(74, 144, 226, 0.4);
}

/* Button */
.card button {
  grid-column: 2 / 3;
  width: 100%;
  padding: 14px;
  background: #4a90e2;
  color: #ffffff;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 10px;
}
.card button:hover {
  background: #357ab8;
}

/* Result Box */
.result-box {
  background: #ffffff;
  border: 1px solid #d3e3fc;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
  overflow-x: auto;
  word-break: break-word;
}
.result-box .label {
  font-weight: 600;
  display: inline-block;
  width: 120px;
  color: #2d3e50;
}

/* Footer */
.card footer {
  text-align: center;
  padding: 15px;
  font-size: 0.95rem;
  color: #7a7a7a;
}

/* Responsive */
@media (max-width: 768px) {
  .card {
    max-width: 95%;
    padding: 20px;
  }
  .card form {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .card form label {
    justify-self: start;
  }
  .card button {
    width: 100%;
    grid-column: auto;
  }
}
.card {
  width: 100%;
  max-width: 650px;
  background: #ffffff;
  border: 1px solid #d0d7de; /* viền sáng rõ */
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08); /* bóng rõ ràng */
  padding: 30px;
  margin: 0 auto;
  transition: box-shadow 0.3s ease;
}
.finance-info {
  background-color: #f9fbfd; /* nhẹ hơn trắng */
  border: 1px solid #cbd6e2;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  color: #2d3e50;
}

.finance-info p {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.finance-info strong {
  color: #2d3e50;
}
.navigation-links a {
  background-color: #f5f7fa;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  padding: 10px 14px;
  color: #2d3e50;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: background 0.2s ease;
}

.navigation-links a:hover {
  background-color: #ffffff;
}

.navigation-links a:last-child {
  border-color: #4a90e2;
  color: #4a90e2;
  background-color: #fdfdfd;
}

.navigation-links a:last-child:hover {
  background-color: #ffffff;
}
```

### `app\static\styles\style2.css`
```css
/* Bug-Bounty-Web — Dark Mode Theme with Responsive Layout */

/* Reset & Base */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  width: 100%;
  min-height: 100%;
  font-family: 'Roboto', sans-serif;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: #e0e0e0;
  line-height: 1.5;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  font-size: 16px;
}

/* Card Wrapper */
.card {
  width: 100%;
  max-width: 650px;
  background: rgba(20, 20, 30, 0.9);
  border: 1px solid #00ffa3;
  border-radius: 12px;
  box-shadow: 0 0 18px #00ffa3;
  overflow: hidden;
  padding: 25px;
  margin: 0 auto;
}

/* Header */
.card header {
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #00ffa366;
}
.card header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 5px;
  color: #00ffa3;
}
.card header p {
  font-size: 1rem;
  color: #b8ffe6;
}

/* Main */
.card main {
  margin-top: 20px;
}

/* Profile Info */
.card .profile-info {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #00ffa3;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow-x: auto;
  word-break: break-word;
}
.card .profile-info p {
  font-size: 1rem;
  color: #e0e0e0;
}

/* Form Styles */
.card form {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px 30px;
  align-items: center;
  margin-bottom: 20px;
}
.card form label {
  font-size: 1rem;
  font-weight: 600;
  justify-self: end;
  color: #a0ffa3;
}
.card form input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #00ffa3;
  border-radius: 10px;
  font-size: 1rem;
  background-color: #121212;
  color: #e0e0e0;
}
.card form input:focus {
  border-color: #00ffa3;
  outline: none;
  box-shadow: 0 0 6px #00ffa3;
}

/* Buttons */
.card button {
  grid-column: 2 / 3;
  width: 100%;
  padding: 14px;
  background: #00ffa3;
  color: #0f2027;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 10px;
}
.card button:hover {
  background: #00cc7a;
}

/* Result Box */
.card .result-box {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #00ffa3;
  padding: 15px;
  border-radius: 8px;
  margin-top: 20px;
  overflow-x: auto;
  word-break: break-word;
}
.card .result-box .label {
  font-weight: 600;
  display: inline-block;
  width: 120px;
  color: #a0ffa3;
}
.card .result-box .value, .card .result-box .error, .card .result-box .success {
  font-size: 1rem;
}

/* Finance Info Box */
.finance-info {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid #00ffa3;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  color: #e0e0e0;
}
.finance-info p {
  color: #e0e0e0;
}
.finance-info strong {
  color: #00ffa3;
}

/* Footer */
.card footer {
  text-align: center;
  padding: 15px;
  font-size: 0.95rem;
  color: #7a7a7a;
}

/* Responsive */
@media (max-width: 768px) {
  .card {
    max-width: 95%;
    padding: 20px;
  }
  .card form {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .card form label {
    justify-self: start;
  }
  .card button {
    width: 100%;
    grid-column: auto;
  }
}
/* Admin Panel Specific */
.menu {
  list-style: none;
  padding: 0;
  margin: 25px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu li a {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #e0e0e0;
  font-weight: 500;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: #1a2b3c;
  transition: background 0.2s, color 0.2s;
}

.menu li a:hover {
  background-color: #00ffa340;
  color: #00ffa3;
}

.menu li:last-child a {
  background-color: #3a1a1a;
  color: #ff4d6d;
}

.menu li:last-child a:hover {
  background-color: #ff4d6d33;
  color: #ff4d6d;
}

/* Admin Panel Title */
.card h1 {
  color: #00ffa3;
  text-align: center;
  margin-bottom: 20px;
}
.navigation-links a {
  background-color: rgb(255, 255, 255);
  border: 1px solid #00ffa3;
  border-radius: 8px;
  padding: 12px 14px;
  transition: background 0.2s ease-in-out;
}

.navigation-links a:hover {
  background-color: rgba(211, 205, 205, 0.459);
}
```

### `app\templates\index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Web Site Ebook</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
</head>
<body>
    <div class="card">
        <h1>Welcome to the Ebook Website</h1>
        <label><p class="info">Hi! If you have an account, you can <a href="/auth/login">Login</a></p></label>
        <label><p class="info">Don't have an account? No worries! You can <a href="/auth/register">Register</a> here.</p></label>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>
</body>
</html>
```

### `app\templates\admin\control_panel.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Control Panel</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Fonts & Material Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
</head>
<body>
    <div class="card">
        {% if username %}
            <h1>Welcome Back {{ username }}!</h1>
        {% endif %}

        <ul class="menu">
            <li>
                <a href="/admin/profile">
                    <span class="material-icons">person</span> Profile
                </a>
            </li>
            <li>
                <a href="/admin/settings">
                    <span class="material-icons">settings</span> Settings
                </a>
            </li>
            <li>
                <a href="/admin/notifications">
                    <span class="material-icons">notifications</span> Update Notification
                </a>
            </li>
            <li>
                <a href="/admin/logs">
                    <span class="material-icons">list_alt</span> Logs
                </a>
            </li>
            <li>
                <a href="/auth/logout?running=True">
                    <span class="material-icons">logout</span> Logout
                </a>
            </li>
        </ul>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>
</body>
</html>
```

### `app\templates\admin\login_admin.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <!-- Google Fonts & Material Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
    <title>Control Panel Login</title>
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
</head>
<body>
    <div class="card">
        <h1>Control Panel Login</h1>
        <form action="/admin/login" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required placeholder="Enter your username">

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required placeholder="Enter your password">

            <button type="submit">Login</button>
        </form>
            {% if error %}
            <p style="color:royalblue;"> {{ error }}</p>
            {% endif %}
        <p>Reset Password? <a href="/auth/reset-password">Reset Password Here</a></p>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>
</body>
</html>
```

### `app\templates\admin\logs.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Logs File</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
  <style>
    body {
      font-family: 'Courier New', monospace;
      background: #121212;
      color: #e0e0e0;
      padding: 20px;
    }
    .entry {
      background: #1e1e1e;
      border: 1px solid #00ffa3;
      border-radius: 8px;
      padding: 15px;
      margin-bottom: 15px;
      white-space: pre-wrap;
    }
    .action-buttons {
      display: flex;
      gap: 16px;
      margin-top: 25px;
    }
    .action-button {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      font-weight: 600;
      padding: 10px 14px;
      border-radius: 6px;
      background-color: #1e1e1e;
      border: 1px solid #4a90e2;
      color: #4a90e2;
      cursor: pointer;
      transition: background 0.2s;
    }
    .action-button:hover {
      background: #2a2a2a;
    }
    .logout-button {
      border-color: #e74c3c;
      color: #e74c3c;
    }
    .logout-button:hover {
      background: #2a2a2a;
    }
    .clear-button {
      border-color: #00ffa3;
      color: #00ffa3;
    }
    .clear-button:hover {
      background: #1b2a24;
    }
    h1 {
      color: #00ffa3;
      text-shadow: 0 0 8px #00ffa3;
      font-weight: 700;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <h1 style="color: #00ffa3; text-shadow: 0 0 8px #00ffa3; font-weight: 700; margin-bottom: 20px;">
    Logs File
  </h1>

  {% for entry in entries %}
    <div class="entry">{{ entry }}</div>
  {% else %}
    <p>No logs found.</p>
  {% endfor %}

  <div class="action-buttons">
    <a href="javascript:window.location.href = document.referrer" class="action-button">
      <span class="material-icons">arrow_back</span> Back
    </a>
    <a href="/auth/logout?running=True" class="action-button logout-button">
      <span class="material-icons">logout</span> Logout
    </a>
    <button class="action-button clear-button" onclick="clearLogs()">
      <span class="material-icons">delete</span> Clear Logs
    </button>
  </div>

  <script src="/static/script-js/clear_logs_admin.js"></script>
</body>
</html>
```

### `app\templates\admin\profile_admin.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Profile</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />

    <!-- Google Fonts & Material Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
    <script src="{{ url_for('static', filename='script-js/get_information_admin.js') }}"></script>
</head>
<body>
    <div class="card" id="card" style="visibility: hidden;">
        {% if username %}
        <h1>Profile {{ username }}</h1>
        {% endif %}

        <div id="result" class="result-box" style="display:none;">Information</div>

        <ul style="list-style: none; padding: 0; margin-top: 20px;">
          <li style="margin-bottom: 12px;">
              <a href="javascript:window.location.href = document.referrer" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #4a90e2; font-weight: 600;">
                  <span class="material-icons">arrow_back</span> Back
              </a>
          </li>
          <li>
              <a href="/auth/logout?running=True" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #e74c3c; font-weight: 600;">
                  <span class="material-icons">logout</span> Logout
              </a>
          </li>
        </ul>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>
</body>
</html>
```

### `app\templates\auth\login.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <title>Login</title>
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
</head>
<body>
    <div class="card">
        <h1>Login</h1>
        <form action="/auth/login" method="POST">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required placeholder="Enter your username">

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required placeholder="Enter your password">

            <button type="submit">Login</button>
        </form>
            {% if error %}
            <p style="color:royalblue;"> {{ error }}</p>
            {% endif %}
        <p>Don't have an account? <a href="/auth/register">Register Here</a></p>
        <p>Reset Password? <a href="/auth/reset-password">Reset Password Here</a></p>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>
</body>
</html>
```

### `app\templates\auth\logout.html`
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <title>Redirecting ...</title>
  <script>
    const style = localStorage.getItem('style') || 'light_mode';
    const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.write(`<link rel="stylesheet" href="${css}">`);
  </script>
</head>
<body>
  <div class="card">
    <div class="message">
      You will redirect to login <span id="countdown">5</span> seconds...
    <footer>
      &copy; 2025 TheWindGhost
    </footer>
    </div>
  </div>
  {% if running %}
  <script>
    let countdown = 5;
    const countdownSpan = document.getElementById('countdown');

    const interval = setInterval(() => {
      countdown--;
      countdownSpan.textContent = countdown;
      if (countdown <= 0) {
        clearInterval(interval);
        running = '{{ running|safe }}';
        window.location.href = '/auth/login';
      }
    }, 1000);

  </script>
  {% endif %}

</body>
</html>
```

### `app\templates\auth\register.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <script>
    const style = localStorage.getItem('style') || 'light_mode';
    const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.write(`<link rel="stylesheet" href="${css}">`);
  </script>
  <title>Registration Form</title>
</head>
<body>
  <div class="card">

    <header>
      <h1>Registration Form</h1>
      <p>Please fill in your details below.</p>
    </header>

    <main>

      <section class="profile">
        <div class="profile-info">
          <p>Welcome! Enter your registration details.</p>
        </div>

        <form id="info-form" method="POST" action="/auth/register">
          <label for="username">Username:</label>
          <input type="text" id="username" name="username" required placeholder="Your username">

          <label for="password">Password:</label>
          <input type="password" id="password" name="password" required placeholder="Your password">

          <label for="email">Email:</label>
          <input type="email" id="email" name="email" required placeholder="Your email">

          <label for="first_name">First Name:</label>
          <input type="text" id="first_name" name="first_name" required placeholder="Your first name">

          <label for="last_name">Last Name:</label>
          <input type="text" id="last_name" name="last_name" required placeholder="Your last name">

          <label for="number_phone">Phone Number:</label>
          <input type="tel" id="number_phone" name="number_phone" required placeholder="Your phone number">

          <label for="website_company">Website:</label>
          <input type="url" id="website_company" name="website_company" placeholder="Your company website">

          <label for="birth_date">Birth Date:</label>
          <input type="date" id="birth_date" name="birth_date" required>

          <button type="submit">Register</button>
        </form>

        {% if error is defined %}
          <p class="error-message">Error: {{ error }}</p>
        {% endif %}
        {% if success is defined %}
          <p class="success-message">{{ success }}, <a href="/auth/login">Login here</a></p>
        {% endif %}
      </section>

    </main>
    <!-- Footer -->
    <footer>
      &copy; 2025 TheWindGhost
    </footer>
  </div>
</body>
</html>
```

### `app\templates\auth\reset_password.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Reset Password</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" rel="stylesheet">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
</head>
<body>
    <div class="card">
        <h1><span class="material-symbols-rounded">mail</span>Reset Password</h1>
        <form method="POST">
            <label for="email">Enter your email address:</label>
            <input type="email" name="email" id="email" required>
            <button type="submit">Send Reset Link</button>
            {% if Notification %}
            <p>{{ Notification }}</p>
            {% endif %}
        </form>
    <!-- Footer -->
    <footer>
        &copy; 2025 TheWindGhost
    </footer>
    </div>
</body>
</html>
```

### `app\templates\auth\reset_token.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Set New Password</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded" rel="stylesheet">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
</head>
<body>
    <div class="card">
        <h1><span class="material-symbols-rounded">lock_reset</span>Set New Password</h1>
        <form method="POST">
            <label for="password">New Password:</label>
            <input type="password" name="password" id="password" required>
            <button type="submit">Reset Password</button>
            {% if Notification %}
            <p>{{ Notification }}</p>
            {% elif Notification2 %}
            <p>{{ Notification2 }}<a href="/login">Login on Here</a></p>
            {% endif %}
        </form>
    </div>
    <!-- Footer -->
    <footer>
        &copy; 2025 TheWindGhost
    </footer>
</body>
</html>
```

### `app\templates\error_pages\403.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <title>403 Forbidden</title>
  <script>
    const style = localStorage.getItem('style') || 'light_mode';
    const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.write(`<link rel="stylesheet" href="${css}">`);
  </script>
  <script src="{{ url_for('static', filename='script-js/redirect_referer.js') }}"></script>
</head>
<body>
  <div class="card">
    <h1>403 - Forbidden</h1>
    <p>You don't have permission to access this page.</p>
    <button onclick="goBack()">Go Back</button>
    <footer>
      &copy; 2025 TheWindGhost
    </footer>
  </div>
</body>
</html>
```

### `app\templates\user\dashboard.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Dashboard</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />

  <!-- Material Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <script>
    const style = localStorage.getItem('style') || 'light_mode';
    const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.write(`<link rel="stylesheet" href="${css}">`);
  </script>
  <script src="{{ url_for('static', filename='script-js/get_balance_user.js') }}" defer></script>

</head>
<body>
  <div class="card">

    <header style="text-align: center; margin-bottom: 20px;">
      <h1 style="font-size: 2rem; display: flex; justify-content: center; align-items: center; gap: 10px;">
        <span class="material-icons">dashboard</span>
        Dashboard
      </h1>
    </header>

    <section class="user-info" style="margin-bottom: 25px;">
      <h2 style="font-size: 1.5rem; font-weight: 600; display: flex; align-items: center; gap: 10px;">
        <span class="material-icons">waving_hand</span>
        Welcome Back, <span class="username" style="color: #4a90e2;">{{ username }}</span>!
      </h2>
      <p style="margin-top: 8px;"><strong>Status:</strong> <span class="status-active" style="color: green; font-weight: 600;">Active</span></p>
    </section>

    <section class="finance-info">
      <p style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
        <span class="material-icons">account_balance</span>
        <strong>Account Balance:</strong> $<span id="balance-amount"></span>
      </p>
      <!-- demo and waiting for code backend-->
      <p style="display: flex; align-items: center; gap: 8px;">
        <span class="material-icons">hourglass_empty</span>
        <strong>Pending:</strong> $200.00
      </p>
    </section>

    <nav>
      <ul class="navigation-links" style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px;">
        <li>
          <a href="/user/profile" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #2d3e50; font-weight: 600;">
            <span class="material-icons">person</span> Profile
          </a>
        </li>
        <li>
          <a href="/user/setting" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #2d3e50; font-weight: 600;">
            <span class="material-icons">settings</span> Setting
          </a>
        </li>
        <li>
          <a href="/user/wallet" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #2d3e50; font-weight: 600;">
            <span class="material-icons">wallet</span> Balances
          </a>
        </li>
        <li>
          <a href="/auth/logout?running=True" style="display: flex; align-items: center; gap: 10px; text-decoration: none; color: #e74c3c; font-weight: 600;">
            <span class="material-icons">logout</span> Logout
          </a>
        </li>
      </ul>
    </nav>

    <footer style="margin-top: 30px; text-align: center; font-size: 0.95rem; color: #7a7a7a;">
      &copy; 2025 TheWindGhost
    </footer>

  </div>
</body>
</html>
```

### `app\templates\user\profile_user.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Profile</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <script>
        const style = localStorage.getItem('style') || 'light_mode';
        const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
        document.write(`<link rel="stylesheet" href="${css}">`);
    </script>
    <script src="{{ url_for('static', filename='script-js/get_information_user.js') }}"></script>
</head>
<body>
    <div class="card" id="card" style="visibility: hidden;">
        {% if template_rendered %}
        <h1>Profile {{ template_rendered }}</h1>
        {% endif %}

        <div id="result" class="result-box" style="display:none;">Information</div>

        <ul style="list-style: none; padding: 0; margin-top: 20px;">
          <li style="margin-bottom: 12px;">
              <a href="javascript:window.location.href = document.referrer" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #4a90e2; font-weight: 600;">
                  <span class="material-icons">arrow_back</span> Back
              </a>
          </li>
          <li>
              <a href="/auth/logout?running=True" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #e74c3c; font-weight: 600;">
                  <span class="material-icons">logout</span> Logout
              </a>
          </li>
        </ul>
        <footer>
            &copy; 2025 TheWindGhost
        </footer>
    </div>

</body>
</html>
```

### `app\templates\user\setting_user.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Settings Update</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <!-- Google Fonts & Material Icons -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
  <script>
    (function(){
      const mode = localStorage.getItem('style') || 'light_mode';
      const href = mode === 'dark_mode'
        ? '/static/styles/style2.css'
        : '/static/styles/style1.css';
      document.write(`<link rel="stylesheet" id="theme-stylesheet" href="${href}">`);
    })();
  </script>

  <script src="{{ url_for('static', filename='script-js/update_setting_user.js') }}"></script>
</head>
<body>
  <div class="card">
    <h1 style="text-align: center;">User Settings</h1>

    <form id="settings-form" method="POST" style="display: flex; flex-direction: column; gap: 14px;">
      <label>Email</label>
      <input type="email" id="email" placeholder="user@example.com" />

      <label>Date of Birth</label>
      <input type="date" id="birth_date" />

      <label>New Password</label>
      <input type="password" id="password" placeholder="Enter new password" />

      <label>Interface Style</label>
      <select id="setting">
        <option value="light_mode">Light Mode</option>
        <option value="dark_mode">Dark Mode</option>
      </select>

      <button type="submit" style="padding: 12px; background-color: #4a90e2; color: white; font-weight: bold; border: none; border-radius: 6px; cursor: pointer;">
        Save Changes
      </button>
    </form>

    <div id="clientError" class="message error" style="display:none; margin-top: 10px;"></div>

    {% if success %}
      <div class="message success" style="margin-top: 15px; color: green; font-weight: 600;">
        {{ success }}
      </div>
    {% endif %}
    {% if error %}
      <div class="message error" style="margin-top: 15px; color: red; font-weight: 600;">
        {{ error }}
      </div>
    {% endif %}

    <ul style="list-style: none; padding: 0; margin-top: 25px; display: flex; flex-direction: column; gap: 12px;">
      <li>
        <a href="javascript:window.location.href = document.referrer" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #4a90e2; font-weight: 600;">
          <span class="material-icons">arrow_back</span> Back
        </a>
      </li>
      <li>
        <a href="/auth/logout?running=True" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #e74c3c; font-weight: 600;">
          <span class="material-icons">logout</span> Logout
        </a>
      </li>
    </ul>

    <footer style="margin-top: 30px; text-align: center; font-size: 0.95rem; color: #7a7a7a;">
      &copy; 2025 TheWindGhost
    </footer>
  </div>

</body>
</html>
```

### `app\templates\user\wallet.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
  <title>Wallet</title>
  <!-- Material Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
  <script>
    const style = localStorage.getItem('style') || 'light_mode';
    const css = style === 'dark_mode' ? '/static/styles/style2.css' : '/static/styles/style1.css';
    document.write(`<link rel="stylesheet" href="${css}">`);
  </script>
</head>
<body>

  <div class="card">
    <h2 style="font-size: 1.8rem; text-align: center; margin-bottom: 20px;">Update Your Balance</h2>

    <form action="/user/wallet" method="POST" style="display: flex; flex-direction: column; gap: 15px;">
      <label for="balance" style="font-weight: 600;">Enter New Balance</label>
      <input type="text" id="balance" name="balance" class="balance-input" required style="padding: 10px; border-radius: 5px; border: 1px solid #ccc;">

      <button type="submit" class="submit-button" style="padding: 12px; background-color: #4a90e2; color: white; font-weight: bold; border: none; border-radius: 6px; cursor: pointer;">
        Update Balance
      </button>
    </form>

    {% if result %}
    <div class="result-message" style="margin-top: 15px; color: green; font-weight: 600;">
      <p>You have: {{ result }} in your wallet</p>
    </div>
    {% elif error %}
    <div class="error-message" style="margin-top: 15px; color: red; font-weight: 600;">
      <p>{{ error }}</p>
    </div>
    {% endif %}

    <ul style="list-style: none; padding: 0; margin-top: 25px; display: flex; flex-direction: column; gap: 12px;">
      <li>
        <a href="javascript:window.location.href = document.referrer" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #4a90e2; font-weight: 600;">
          <span class="material-icons">arrow_back</span> Back
        </a>
      </li>
      <li>
        <a href="/auth/logout?running=True" style="display: flex; align-items: center; gap: 8px; text-decoration: none; color: #e74c3c; font-weight: 600;">
          <span class="material-icons">logout</span> Logout
        </a>
      </li>
    </ul>

    <footer style="margin-top: 30px; text-align: center; font-size: 0.95rem; color: #7a7a7a;">
      &copy; 2025 TheWindGhost
    </footer>

  </div>

</body>
</html>
```

### `app\utils\__init__.py`
```python
```

### `app\utils\check_xml_encoding.py`
```python
import re

def get_xml_encoding_lxml(xml_bytes: bytes) -> str:

    try:
        # decode as ascii to extract encoding declaration
        head = xml_bytes[:100].decode('ascii', errors='ignore')
        match = re.search(r'encoding=[\'"]([\w-]+)[\'"]', head)

        if match:
            return match.group(1).lower()
        return 'utf-8' # default per XML spec

    except Exception:
        return 'Not Allow'
```

### `app\utils\decorator_admin.py`
```python
from functools import wraps
from flask import session, url_for, redirect

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # if client don't have session -> redirect to login():
        if not session.get('username'):
            return redirect(url_for('auth.login'))

        # if client don't have value: is_admin = True -> redirect to 403.html
        if session.get('is_admin') == False:
            return redirect(url_for('error_pages.page_403'))

        return f(*args, **kwargs)
    return decorated_function
```

### `app\utils\decorator_user.py`
```python
from functools import wraps
from flask import session, url_for, redirect

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # if client don't have session -> redirect to login():
        if not session.get('username'):
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    return decorated_function
```

<!-- AUTO-GENERATED: END -->