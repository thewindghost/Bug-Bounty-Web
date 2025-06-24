from flask import Blueprint, render_template, session
from app.utils.decorator_admin import admin_required
from app.controllers.admin.read_logs import read_logs_info

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
@admin_required
def admin_panel():

    return render_template('admin/control_panel.html', username=session.get('username'))
    
@admin_bp.route('/logs', methods=['GET'])
@admin_required
def read_logs():

    return read_logs_info()