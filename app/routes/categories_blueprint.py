from flask import Blueprint
from app.controllers.categories_controller import create_category, update_category, delete_category

bp_categories = Blueprint("bp_categories", __name__, url_prefix="/categories")

bp_categories.post("")(create_category)
bp_categories.patch("/<id>")(update_category)
bp_categories.delete("/<id>")(delete_category)