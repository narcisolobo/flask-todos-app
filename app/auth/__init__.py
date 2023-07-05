from flask_bcrypt import Bcrypt
from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")
bcrypt = Bcrypt()
from app.auth import routes