import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask / SQLAlchemy
    SECRET_KEY                    = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI       = os.environ.get("DATABASE_URL") or "sqlite:///mowapp.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth (dev only; remove/invert for prod!)
    OAUTHLIB_INSECURE_TRANSPORT   = os.environ.get("OAUTHLIB_INSECURE_TRANSPORT", "1")
    GOOGLE_CLIENT_ID              = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET          = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL          = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # Uploads
    UPLOAD_FOLDER                 = os.path.join(basedir, "app", "static", "uploads")
    ALLOWED_EXTENSIONS            = {"jpg", "jpeg", "png", "pdf"}
    MAX_CONTENT_LENGTH            = 5 * 1024 * 1024  # 5 MB max upload

    # Sessions
    PERMANENT_SESSION_LIFETIME    = timedelta(days=7)
