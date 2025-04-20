from flask import redirect, url_for
from app.main import bp
from app import db

@bp.route('/')
def home():
    return redirect(url_for('main.initdb'))

@bp.route('/initdb')
def initdb():
    db.create_all()
    return "<h3>✅ Database initialized successfully!</h3>"
