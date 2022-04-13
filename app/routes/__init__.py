from flask import Flask, Blueprint
from .categories_routes import bp as categories_bp
from .tasks_routes import bp as tasks_bp
from.tasks_categories import bp as tasks_categories_bp

bp_api = Blueprint("api", __name__, url_prefix="/api")

def init_app(app: Flask):

    bp_api.register_blueprint(categories_bp)
    bp_api.register_blueprint(tasks_bp)
    bp_api.register_blueprint(tasks_categories_bp)

    app.register_blueprint(bp_api)