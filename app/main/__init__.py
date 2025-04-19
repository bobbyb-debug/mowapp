from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes  # ensure this is below the bp line
