from app.main import bp
from app import db
from flask import redirect, url_for

@bp.route('/initdb')
def initdb():
    db.create_all()
    return "<h3>✅ Database initialized successfully!</h3>"

@bp.route('/')
def home():
    return redirect(url_for('main.initdb'))
