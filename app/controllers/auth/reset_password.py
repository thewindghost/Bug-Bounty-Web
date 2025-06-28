from flask import request, url_for, render_template
from app.services.send_email import send_reset_email
from app.database.connect_database import get_db_connection
from app.services.get_token import get_token_serializer
import time
from ... import cache

def auth_reset_password_user():
    
    try:        
        timestamp = time.time() 
        email = request.form.get('email', '').strip()
        
        # Check rate limit with cache
        if cache.get(f'reset_mail_sent_{email}'):
            Notification = 'Please wait at least 5 minutes before requesting another password reset email.'
            return render_template('auth/reset_password.html', Notification=Notification)
        
        conn = get_db_connection()
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if user:
            
            user_id = user['id']
            serializer = get_token_serializer()
            token = serializer.dumps({
                'user_id': user_id,
                'timestamp': timestamp
            })
            reset_url = url_for('auth.perform_password_reset', token=token, _external=True)
            
            send_reset_email(email, reset_url)
            
            # Email is saved in cache and wait 5 minutes before resetting password again
            cache.set(f'reset_mail_sent_{email}', True, timeout=300)
            
        Notification = 'If that email is registered, you will receive a password reset link shortly'
        return render_template('auth/reset_password.html', Notification=Notification)
    
    except Exception as e:
        return render_template('auth/reset_password.html', error=str(e))