from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Core Flask extensions

# Handles ORM database access
db = SQLAlchemy()

# Handles DB migrations
migrate = Migrate()

# Handles user session management
login = LoginManager()
login.login_view = 'main.login'
