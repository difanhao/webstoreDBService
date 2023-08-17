from flask import Flask
from app.routes.vip_users import vip_users_bp
from app.routes.vip_orders import vip_orders_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(vip_users_bp, url_prefix="/vip_users")
    app.register_blueprint(vip_orders_bp, url_prefix="/vip_orders")
    return app