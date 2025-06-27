import sqlite3
from flask import jsonify, session
from app.config import Config

def get_current_user_info():
    
    try:
        user_id = session.get('user_id')
        db_path = Config.DB_CONNECTION_FILE_RELATIVE_PATH
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user_data = {
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
                "password": row["password"],
                "pending_loan_amount": float(row["pending_loan_amount"]),
                "pending_loan_count": int(row["pending_loan_count"])
            }
            return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500