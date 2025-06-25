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
                'created_at': row['created_at']
            }
            return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500