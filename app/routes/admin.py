from flask import Blueprint, render_template, session, jsonify, request, make_response
from app.utils.load_data_json import load_data, data_file_users, data_file_admins
from app.utils.decorator_admin import admin_required
from app.config import Config
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
@admin_required 
def admin_panel():

    if request.method == 'POST':
        # If Request to API with user_id
        user_id = request.form.get('user_id', '')
        if user_id and not admin_id:
            data_user = load_data(data_file_users)
            user_data = data_user.get(str(user_id))
            if user_data:
                return jsonify({"user_data": user_data}), 200
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404
            
        # If Request to API with admin_id
        admin_id = request.form.get('admin_id', '')
        if admin_id and not user_id:
            data_admin = load_data(data_file_admins)
            admin_data = data_admin.get(str(admin_id))
            if admin_data:
                return jsonify({"admin_data": admin_data}), 200
            
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404
    
    return render_template('admin/control_panel.html', username=session.get('username'))
    
@admin_bp.route('/logs', methods=['GET'])
@admin_required
def read_logs():

    try:
        with open(Config.LOG_FILE_RELATIVE_PATH, 'r') as f:
            log_data = f.read()
        response= make_response(log_data)
        response.headers['Content-Type'] = 'text/html'
        return response
    
    except FileNotFoundError:
        return "Not Found File Logs", 404