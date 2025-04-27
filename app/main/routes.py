from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.extensions import db
from app.models import Client, Job, Expense
from app.forms import ClientForm
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    monthly_revenue = db.session.query(func.coalesce(func.sum(Job.total_amount), 0.0)).scalar()
    monthly_expenses = db.session.query(func.coalesce(func.sum(Expense.amount), 0.0)).scalar()
    recent_jobs = Job.query.order_by(Job.date.desc()).limit(5).all()
    return render_template(
        'dashboard.html',
        monthly_revenue=monthly_revenue,
        monthly_expenses=monthly_expenses,
        recent_jobs=recent_jobs
    )

@main_bp.route('/clients')
def clients():
    clients = Client.query.order_by(Client.name).all()
    return render_template('clients/view_clients.html', clients=clients)

@main_bp.route('/expenses')
def expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('expenses/view_expenses.html', expenses=expenses)

@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
