from flask import request, render_template
from bleach import clean
from werkzeug.security import generate_password_hash
from app.database.connect_database import get_db_connection
  
def auth_register_user():
    
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
        error = "Internal Server Error"
        return render_template('auth/reset_password.html', error=error)