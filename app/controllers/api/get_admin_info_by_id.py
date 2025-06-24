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
                "email": row["email"]
            }
            return jsonify({"admin_data": admin_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500