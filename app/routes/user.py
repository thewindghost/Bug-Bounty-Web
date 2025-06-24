from flask import Blueprint, render_template, request, session, render_template_string
from bleach import clean
from app.utils.decorator_user import user_required
from app.controllers.user.xml_parser import handle_parser_info


user_bp = Blueprint('user', __name__)

@user_bp.route('/parser-info', methods=['GET', 'POST'])
@user_required
def parser_info():
    
    if request.method == 'POST':
        return handle_parser_info()
    return render_template('user/parser_info.html')

@user_bp.route('/balances', methods=['GET', 'POST'])
@user_required
def update_balance():
    
    try:
        if request.method == 'POST':
            balance = request.form.get('balance', '')
            eval(balance)
            return render_template(f'user/wallet.html', result=balance)

    except Exception as e:
        if 'username' in session:
            error = None
            error = str(e)
            return render_template('user/wallet.html', error=error)

    return render_template('user/wallet.html')

@user_bp.route('/profile', methods=['GET', 'POST'])
@user_required
def profile():
    
    return render_template('user/profile_user.html', template_rendered=clean(render_template_string(session['username'])))

@user_bp.route('/dashboard', methods=['GET'])
@user_required
def dashboard():

    return render_template('user/dashboard.html', username=session['username'])