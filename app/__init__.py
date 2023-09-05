from flask import Flask
from app.api.vip_users_route import vip_users_bp
from app.api.vip_orders_route import vip_orders_bp
from app.api.reset_data_route import reset_data_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(vip_users_bp, url_prefix="/vip_users")
    app.register_blueprint(vip_orders_bp, url_prefix="/vip_orders")
    app.register_blueprint(reset_data_bp, url_prefix="/reset_data")
    return app