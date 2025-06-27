import sqlite3
from flask import jsonify, session
from app.config import Config

def get_current_admin_info():
    
    try:
        admin_id = session.get('admin_id')
        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE id = ?", (admin_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            admin_data = {
                "id": int(row["id"]),
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                "email": row["email"],
                'number_phone': row['number_phone'],
                'website_company': row['website_company'],
                'birth_date': row['birth_date'],
                'created_at': row['created_at'],
                "username": row["username"],
                'is_admin': bool(row['is_admin']),
                'balance': row['balance'],
                "password": row["password"]
            }
            return jsonify({"admin_data": admin_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500