from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.connect_database import get_db_connection
from app.services.get_token import get_token_serializer
from itsdangerous import BadSignature, SignatureExpired
from app.services.send_email import send_reset_email
from .. import cache
from bleach import clean

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    error = None
    if request.method == 'POST':
        
        username = request.form.get('username', '')
        raw_password = clean(request.form.get('password', ''))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, is_admin, password FROM accounts WHERE username = '" + username + "'")
        row = cursor.fetchone()
        conn.close()
        
        if row and check_password_hash(row[2], raw_password):
            session['username'] = row[0]
            session['is_admin'] = bool(row[1])
            
            if session.get('is_admin') == True:
                return redirect(url_for('admin.admin_panel'))
            else:
                return redirect(url_for('user.dashboard'))
        
        else:
            error = "Invalid Username or Password"
        
    return render_template('auth/login.html', error=error)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    error = None
    
    if request.method == 'POST':

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
            cursor.execute("SELECT * FROM accounts WHERE username = '" + username + "'")
            existing_user = cursor.fetchone()
            
            if existing_user:
                error = "Username already exists. Please a defferent one."
                return render_template('auth/register.html', error=error)
            
            # Add new user to database
            cursor.execute('''
                INSERT INTO accounts (username, password, email, first_name, last_name, number_phone, website_company, birth_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, hased_password, email, first_name, last_name, number_phone, website_company, birth_date))

            conn.commit()
            conn.close()
            
            # Register successfully
            success = 'Register Successfully'
            return render_template('auth/register.html', success=success)
        
        except Exception as e:
            error = str(e)
            return render_template('auth/register.html', error=error)
        
    return render_template('auth/register.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        # Check rate limit with cache
        if cache.get(f'reset_mail_sent_{email}'):
            Notification = 'Please wait at least 5 minutes before requesting another password reset email.'
            return render_template('auth/reset_password.html', Notification=Notification)
        
        conn = get_db_connection()
        account = conn.execute("SELECT id FROM accounts WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if account:
            account_id = account['id']
            serializer = get_token_serializer()
            token = serializer.dumps({'account_id': account_id})
            reset_url = url_for('perform_password_reset', token=token, _external=True)
            
            send_reset_email(email, reset_url)
            
            # Email is saved in cache and wait 5 minutes before resetting password again
            cache.set(f'reset_mail_sent_{email}', True, timeout=300)
            
        Notification = 'If that email is registered, you will receive a password reset link shortly'
        return render_template('auth/reset_password.html', Notification=Notification)
    
    return render_template('auth/reset_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def perform_password_reset(token):

    # Check if token was already used
    if cache.get(f'token_used_{token}'):

        Notification = 'This reset link has already been used.'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    serializer = get_token_serializer()

    try:
        data = serializer.loads(token, max_age=3600)
        account_id = data.get('account_id')

    except SignatureExpired:
        Notification = 'The reset link has expired. Please request a new one'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    except BadSignature:
        Notification = 'The reset link is invalid. Please request a new one.'
        return render_template('auth/reset_token.html', Notification=Notification, show_form=False)

    if request.method == 'POST':
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

    return render_template('auth/reset_token.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():

    session.clear()
    running_value = request.args.get('running', 'True')
    response = make_response(render_template('auth/logout.html', running=running_value))
    response.delete_cookie('session')
    return response