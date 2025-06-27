from flask import render_template

def check_token_used():
    
    Notification = 'This reset link has already been used.'
    return render_template('auth/reset_token.html', Notification=Notification, show_form=False)