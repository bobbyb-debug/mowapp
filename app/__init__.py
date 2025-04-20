from flask import Flask
from config import Config
from app.extensions import db, migrate, login
from app.routes.jobs import jobs_bp
from app.routes.main import bp as main_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Set the UPLOAD_FOLDER configuration
    app.config['UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER', 'static/uploads')

    # Register blueprints
    app.register_blueprint(jobs_bp)
    app.register_blueprint(main_bp)

    return app
