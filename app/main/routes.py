from flask import render_template, redirect, url_for
from app.main import bp
from app import db

@bp.route('/initdb')
def initdb():
    db.create_all()
    return "<h3>✅ Database initialized successfully!</h3>"

@bp.route('/')
def home():
    return redirect(url_for('main.initdb'))  # redirect to /initdb just for testing
