# app/clients/routes.py
from flask import Blueprint, render_template, redirect, url_for
from app.forms import ClientForm
from app.models import Client
from app import db

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/')
def view_clients():
    clients = Client.query.order_by(Client.name).all()
    return render_template('clients/view_clients.html', clients=clients)

@clients_bp.route('/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients.view_clients'))
    return render_template('clients/client_form.html', form=form)
