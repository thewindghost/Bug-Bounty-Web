from flask import jsonify, request
from app.utils.load_data_json import data_file_admins, load_data

def get_information_admin():
    
        # If Request to API with admin_id
        admin_id = request.form.get('admin_id')
        
        if not admin_id:
            return jsonify({"error": "Missing admin_id"}), 400
        
        data_admin = load_data(data_file_admins)
        admin_data = data_admin.get(str(admin_id))
        
        if admin_data:
            return jsonify({"admin_data": admin_data}), 200
            
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404