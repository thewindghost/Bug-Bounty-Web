from flask import Blueprint, render_template, request, session
from bleach import clean
from app.utils.decorator_user import user_required
from app.controllers.user.update_setting import handle_setting_user
from app.controllers.user.update_balance import update_balance_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/setting', methods=['GET', 'POST'])
@user_required
def user_parser_info():

    if request.method == 'POST':
        return handle_setting_user()
    
    return render_template('user/setting_user.html')

@user_bp.route('/wallet', methods=['GET', 'POST'])
@user_required
def user_update_balance():
    
    if request.method == 'POST':
        error = "Sorry Code Backend Not Found"
        return render_template('user/wallet.html', error=error)
    
    return render_template('user/wallet.html')

@user_bp.route('/profile', methods=['GET', 'POST'])
@user_required
def user_profile():

    return render_template('user/profile_user.html', username=session['username'])

@user_bp.route('/dashboard', methods=['GET'])
@user_required
def user_dashboard():

    return render_template('user/dashboard.html', username=session['username'])