from flask import Blueprint, render_template, request, session, make_response
from app.controllers.auth.register import auth_register_user
from app.controllers.auth.login import auth_login_user
from app.controllers.auth.reset_password import auth_reset_password_user
from app.controllers.auth.check_token_used import check_token_used
from app.controllers.auth.get_account_id_from_token import get_account_id_user_from_token
from app.controllers.auth.reset_password_check_token_post import reset_password_check_token_user_by_post
from app.controllers.auth.logout import auth_logout_user
from .. import cache

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        return auth_login_user()

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        return auth_register_user()
        
    return render_template('auth/register.html')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    
    if request.method == 'POST':
        return auth_reset_password_user()
    
    return render_template('auth/reset_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def perform_password_reset(token):

    account_id = get_account_id_user_from_token(token)
    if isinstance(account_id, str):
        return account_id

    if cache.get(f'token_used_{token}'):
        return check_token_used()
    
    if request.method == 'POST':
        return reset_password_check_token_user_by_post(account_id, token)

    return render_template('auth/reset_token.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():

    return auth_logout_user()