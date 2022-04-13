from flask import Flask, Blueprint
from .categories_routes import bp as categories_bp

bp_api = Blueprint("api", __name__, url_prefix="/api")

def init_app(app: Flask):

    bp_api.register_blueprint(categories_bp)

    app.register_blueprint(bp_api)