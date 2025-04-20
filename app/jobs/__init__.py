from flask import Blueprint

bp = Blueprint('jobs', __name__)

@bp.route('/')
def index():
    return "Jobs Blueprint"