from flask import render_template, redirect, url_for
from app.main import bp
from app import db

@bp.route('/')
def home():
    return redirect(url_for('main.initdb'))  # temporary: auto-redirect for testing

@bp.route('/initdb')
def initdb():
    db.create_all()
    return "<h3>✅ Database initialized successfully!</h3>"
