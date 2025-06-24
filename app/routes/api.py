from flask import Blueprint, request
from app.controllers.api.get_information_json_admin import get_information_admin
from app.controllers.api.get_information_json_user import get_information_user
from app.utils.decorator_admin import admin_required
from app.utils.decorator_user import user_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/v1/information_users', methods=['GET', 'POST'])
@user_required
def information_user():
    
    if request.method == 'POST':
        return get_information_user()

    return '', 204 # No Contnet

################################################################
@api_bp.route('/v1/information_admin', methods=['GET', 'POST'])
@admin_required
def information_admin():
    
    if request.method == 'POST':
        return get_information_admin()

    return '', 204 # No Contnet