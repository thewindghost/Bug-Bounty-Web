from flask import request, render_template
from werkzeug.security import generate_password_hash
from app.database.connect_database import get_db_connection
from ... import cache

def reset_password_check_token_user_by_post(account_id, token):

        new_password = request.form.get('password', '').strip()

        if not new_password:
            Notification = "Password can't be empty."
            return render_template('auth/reset_token.html', Notification=Notification)

        hashed_password = generate_password_hash(new_password)
        conn = get_db_connection()

        conn.execute(
            'UPDATE accounts SET password = ? WHERE id = ?', (hashed_password, account_id)
        )

        conn.commit()
        conn.close()

        # Mark token as used
        cache.set(f'token_used_{token}', True, timeout=1800)  # Chặn dùng lại trong thời gian token còn hiệu lực

        Notification2 = 'Your Password has been Updated. You may now log in.'
        return render_template('auth/reset_token.html', Notification2=Notification2, show_form=False)