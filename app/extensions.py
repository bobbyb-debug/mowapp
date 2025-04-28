from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate      import Migrate
from flask_login        import LoginManager
from authlib.integrations.flask_client import OAuth   # ← new

db      = SQLAlchemy()
migrate = Migrate()
login   = LoginManager()
oauth   = OAuth()                                      # ← new

# Core Flask extensions

# Handles ORM database access
db = SQLAlchemy()

# Handles DB migrations
migrate = Migrate()

# Handles user session management
login = LoginManager()
login.login_view = 'main.login'
