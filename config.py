import os
from datetime import timedelta

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/receipts')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max upload

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)