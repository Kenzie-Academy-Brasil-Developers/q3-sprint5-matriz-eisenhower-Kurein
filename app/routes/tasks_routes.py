from flask import Blueprint
from app.controllers import tasks_controller

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

bp.post("")(tasks_controller.post_task)
bp.patch("/<int:task_id>")(tasks_controller.patch_task)
bp.delete("/<int:task_id>")(tasks_controller.delete_task)