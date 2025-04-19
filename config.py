import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(basedir, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'receipts')
    PHOTO_FOLDER = os.path.join(basedir, 'app', 'static', 'photos')
    DOCUMENT_FOLDER = os.path.join(basedir, 'app', 'static', 'documents')
    LOG_FOLDER = os.path.join(basedir, 'app', 'logs')
