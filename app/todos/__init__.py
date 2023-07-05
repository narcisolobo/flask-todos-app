from flask import Blueprint
bp = Blueprint("todos", __name__, url_prefix="/todos")

from app.todos import routes
