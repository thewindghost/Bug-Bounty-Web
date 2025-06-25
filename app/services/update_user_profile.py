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
