from flask import Blueprint
from app.controllers import tasks_categories_controller

bp = Blueprint("tasks_categories", __name__, url_prefix="/")

bp.get("")(tasks_categories_controller.tasks_categories_get)