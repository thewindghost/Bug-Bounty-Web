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
                'created_at': row['created_at']
            }
            return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
