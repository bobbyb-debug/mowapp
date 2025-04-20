from flask import Blueprint

bp = Blueprint('clients', __name__)

@bp.route('/')
def index():
    return "Clients Blueprint"