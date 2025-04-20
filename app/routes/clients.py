from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Client
from app import db

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def client_list():
    clients = Client.query.all()
    return render_template('clients/clients_list.html', clients=clients)

@clients_bp.route('/new', methods=['GET', 'POST'])
def new_client():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        if client_name:
            client = Client(name=client_name)
            db.session.add(client)
            db.session.commit()
            return redirect(url_for('clients.client_list'))
    return render_template('clients/new_client.html')
