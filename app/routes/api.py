from flask import Blueprint, request
from app.controllers.api.get_admin_info_by_id import get_information_admin
from app.controllers.api.get_user_info_by_id import get_user_info_by_id
from app.controllers.api.get_current_user_info import get_current_user_info
from app.controllers.api.get_current_admin_info import get_current_admin_info
from app.utils.decorator_admin import admin_required
from app.utils.decorator_user import user_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/v1/information_users', methods=['GET', 'POST'])
@user_required
def information_user():

    if request.method == 'POST':
        return get_user_info_by_id()

    return get_current_user_info()

################################################################
@api_bp.route('/v1/information_admin', methods=['GET', 'POST'])
@admin_required
def information_admin():
    
    if request.method == 'POST':
        return get_information_admin()

    return get_current_admin_info()