from flask import request, jsonify
from app.utils.load_data_json import data_file_users, load_data

def get_information_user():
    
        # If Request to API with user_id
        user_id = request.form.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
            
        data_user = load_data(data_file_users)
        user_data = data_user.get(str(user_id))
            
        if user_data:
            return jsonify({"user_data": user_data}), 200
            
        else:
            return jsonify({"error": "No data found or invalid ID"}), 404