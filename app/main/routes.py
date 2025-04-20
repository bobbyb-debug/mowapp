from flask import Blueprint, request, flash, send_from_directory, render_template, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func
import os
from app import db
from app.models import Expense, Job
from app.forms import ExpenseForm
# app/routes/jobs.py
from flask import Blueprint, render_template

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/', methods=['GET'])
def jobs_home():
    return render_template('jobs.html')

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    # Monthly revenue (example calculation)
    monthly_revenue = db.session.query(func.sum(Job.cost)).filter(
        Job.date >= datetime.now() - timedelta(days=30)
    ).scalar() or 0

    # Monthly expenses
    monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= datetime.now() - timedelta(days=30)
    ).scalar() or 0

    # Active jobs
    active_job_count = Job.query.filter(Job.status == 'In Progress').count()

    # Total clients
    client_count = db.session.query(func.count(Job.client_id.distinct())).scalar() or 0

    # Top services this month
    top_services = db.session.query(
        Job.service_type,
        func.count(Job.id).label('job_count'),
        func.sum(Job.cost).label('total_revenue')
    ).filter(
        Job.date >= datetime.now() - timedelta(days=30)
    ).group_by(Job.service_type).order_by(func.sum(Job.cost).desc()).limit(5).all()

    # Recent jobs
    recent_jobs = Job.query.order_by(Job.date.desc()).limit(10).all()

    return render_template(
        'dashboard.html',
        monthly_revenue=monthly_revenue,
        monthly_expenses=monthly_expenses,
        active_job_count=active_job_count,
        client_count=client_count,
        top_services=top_services,
        recent_jobs=recent_jobs
    )

@bp.route('/expenses', methods=['GET', 'POST'])
def expenses():
    form = ExpenseForm()
    form.job_id.choices = [(j.id, f"{j.client.name} - {j.service_type}")
                           for j in Job.query.order_by(Job.date.desc())]

    if form.validate_on_submit():
        expense = Expense(
            job_id=form.job_id.data,
            category=form.category.data,
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data
        )
        if form.receipt.data:
            filename = secure_filename(form.receipt.data.filename)
            form.receipt.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            expense.receipt_filename = filename

        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('main.expenses'))

    expenses = Expense.query.order_by(Expense.date.desc()).limit(50).all()
    monthly_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= datetime.now() - timedelta(days=30)
    ).scalar() or 0

    return render_template('expense_form.html',
                           form=form,
                           expenses=expenses,
                           monthly_total=monthly_total)

@bp.route('/receipts/<filename>')
def view_receipt(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
