from flask import Flask
from flask_mail import Mail
from flask_caching import Cache
from app.config import Config
from app.database import connect_database

mail = Mail()
cache = Cache()

def create_app():
    app = Flask(__name__, instance_relative_config=False, static_url_path="/static", static_folder="static")

    app.config.from_object(Config)

    # Khởi tạo các extension với app
    Config.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Khởi tạo module database (sẽ tự động tạo DB nếu chưa có)
    connect_database.init_app(app)

    # Đăng ký Blueprints
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.error_pages import error_pages_bp
    from app.routes.main import main_bp
    from app.routes.user import user_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(error_pages_bp, url_prefix='/error_pages')
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    return app