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
