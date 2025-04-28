# app/routes/auth.py

from flask import Blueprint, redirect, url_for, session
from app.extensions import oauth

auth_bp = Blueprint('auth', __name__)

# Setup Google OAuth client
google = oauth.create_client('google')

@auth_bp.route('/login')
def login():
    # Redirect user to Google for login
    redirect_uri = url_for('auth.auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth')
def auth():
    # Handle callback from Google and get the user info
    token = google.authorize_access_token()
    user = google.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('main.index'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))
