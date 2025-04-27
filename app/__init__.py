# app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, migrate, login
from app.main.routes import main_bp
from app.jobs.routes import jobs_bp
from flask_login import LoginManager, AnonymousUserMixin

# Create login manager globally
login_manager = LoginManager()

# Optional dummy anonymous user
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'

login_manager.anonymous_user = Anonymous

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set debug mode ON
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp)

    # Setup dummy user loader
    @login_manager.user_loader
    def load_user(user_id):
        return None  # No users yet

    return app
