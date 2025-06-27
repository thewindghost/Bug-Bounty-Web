from flask import render_template
from app.services.get_token import get_token_serializer
from itsdangerous import BadSignature, SignatureExpired
    
def get_account_id_user_from_token(token):
    
    serializer = get_token_serializer()

    try:
        data = serializer.loads(token, max_age=3600)
        return data.get('account_id')
    
    except SignatureExpired:
        return render_template('auth/reset_token.html', Notification='The reset link has expired. Please request a new one', show_form=False)

    except BadSignature:
        return render_template('auth/reset_token.html', Notification='The reset link is invalid. Please request a new one.', show_form=False)