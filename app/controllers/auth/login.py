from flask import request, session, redirect, url_for, render_template
from bleach import clean
from werkzeug.security import check_password_hash
from app.database.connect_database import get_db_connection

def auth_login_user():

    try: 
        username = request.form.get('username', '')
        raw_password = clean(request.form.get('password', ''))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, is_admin, password, id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row and check_password_hash(row[2], raw_password):
            session['username'] = row[0]
            session['is_admin'] = bool(row[1])
            session['user_id'] = int(row[3])
            return redirect(url_for('user.user_dashboard'))
        
        else:
            error = "Invalid Username or Password"
            return render_template('auth/login.html', error=error)
            
    except Exception as e:
        e = "Internal Server Error", 500
        return render_template('auth/login', error=e)