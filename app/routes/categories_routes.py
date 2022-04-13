from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint("categories", __name__, url_prefix="/categories")

bp.post("")(categories_controller.post_category)
bp.patch("/<int:category_id>")(categories_controller.patch_category)
bp.delete("/<int:category_id>")(categories_controller.delete_category)