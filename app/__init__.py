from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
# Import routes for jobs, clients, and expenses
from app.routes.jobs import jobs_bp
from app.routes.clients import clients_bp
from app.routes.expenses import expenses_bp

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    register_error_handlers(app)

    return app

def register_error_handlers(app):
    app.register_blueprint(jobs_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(expenses_bp)

    register_error_handlers(app)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
