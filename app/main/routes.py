# app/main/routes.py

from datetime import datetime, timedelta
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, send_from_directory
)
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os

from app import db
from app.forms import ClientForm, JobForm, ExpenseForm, MileageForm, ServiceForm
from app.forms import MATERIAL_SUBCATEGORIES, LABOR_SUBCATEGORIES
from app.models import Client, Job, Expense, Mileage, Service
from app.main import bp

UPLOAD_FOLDER = os.path.join('app', 'static', 'receipts')
PHOTO_FOLDER = os.path.join('app', 'static', 'photos')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_monthly_timeframe():
    return datetime.now() - timedelta(days=30)

# ─── One-time route to init database ─────────────
@bp.route('/initdb')
def initdb():
    db.create_all()
    return "<h3>✅ Database initialized successfully!</h3>"

# ─── Home ─────────────────────────────────────────
@bp.route('/')
def home():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard')
def dashboard():
    last_month = get_monthly_timeframe()
    stats = {
        'client_count': Client.query.count(),
        'active_job_count': Job.query.filter(Job.status.in_(['Pending', 'In Progress'])).count(),
        'total_revenue': db.session.query(func.sum(Job.cost)).filter(Job.status == 'Completed').scalar() or 0,
        'total_expenses': db.session.query(func.sum(Expense.amount)).scalar() or 0,
        'recent_jobs': Job.query.join(Client).order_by(Job.date.desc()).limit(5).all(),
        'monthly_revenue': db.session.query(func.sum(Job.cost)).filter(Job.status == 'Completed', Job.date >= last_month).scalar() or 0,
        'monthly_expenses': db.session.query(func.sum(Expense.amount)).filter(Expense.date >= last_month).scalar() or 0,
        'top_services': db.session.query(Job.service_type, func.count(Job.id), func.sum(Job.cost)).group_by(Job.service_type).order_by(func.sum(Job.cost).desc()).limit(5).all()
    }
    return render_template('dashboard.html', **stats)

# (Rest of your client/job/expense routes stay here — you can paste them back in below)

# ─── Home ─────────────────────────────────────────────
@bp.route('/')
def home():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard')
def dashboard():
    last_month = get_monthly_timeframe()
    stats = {
        'client_count': Client.query.count(),
        'active_job_count': Job.query.filter(Job.status.in_(['Pending', 'In Progress'])).count(),
        'total_revenue': db.session.query(func.sum(Job.cost)).filter(Job.status == 'Completed').scalar() or 0,
        'total_expenses': db.session.query(func.sum(Expense.amount)).scalar() or 0,
        'recent_jobs': Job.query.join(Client).order_by(Job.date.desc()).limit(5).all(),
        'monthly_revenue': db.session.query(func.sum(Job.cost)).filter(Job.status == 'Completed', Job.date >= last_month).scalar() or 0,
        'monthly_expenses': db.session.query(func.sum(Expense.amount)).filter(Expense.date >= last_month).scalar() or 0,
        'top_services': db.session.query(Job.service_type, func.count(Job.id), func.sum(Job.cost)).group_by(Job.service_type).order_by(func.sum(Job.cost).desc()).limit(5).all()
    }
    return render_template('dashboard.html', **stats)

# ─── Clients ───────────────────────────────────────────
@bp.route('/clients')
def clients():
    page = request.args.get('page', 1, type=int)
    clients = Client.query.order_by(Client.name.asc()).paginate(page=page, per_page=10)
    return render_template('clients/view_clients.html', clients=clients)

@bp.route('/clients/add', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        filename = None
        if form.photo.data and allowed_file(form.photo.data.filename):
            filename = secure_filename(form.photo.data.filename)
            os.makedirs(PHOTO_FOLDER, exist_ok=True)
            form.photo.data.save(os.path.join(PHOTO_FOLDER, filename))
        client = Client(
            name=form.name.data,
            business_name=form.business_name.data,
            street_address=form.street_address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            phone=form.phone.data,
            alt_phone=form.alt_phone.data,
            email=form.email.data,
            tax_id=form.tax_id.data,
            billing_notes=form.billing_notes.data,
            general_notes=form.general_notes.data,
            photo_filename=filename
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added!', 'success')
        return redirect(url_for('main.clients'))
    return render_template('clients/client_form.html', form=form)

# ─── Jobs ─────────────────────────────────────────────
@bp.route('/jobs')
def jobs():
    jobs = Job.query.order_by(Job.date.desc()).all()
    return render_template('jobs/view_jobs.html', jobs=jobs)

@bp.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    form.client_id.choices = [(c.id, c.name) for c in Client.query.order_by(Client.name)]
    form.services.choices = [(s.id, s.name) for s in Service.query.order_by(Service.name)]
    if form.validate_on_submit():
        job = Job(
            client_id=form.client_id.data,
            title=form.title.data,
            service_type=form.service_type.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            cost=form.cost.data,
            estimated_cost=form.estimated_cost.data,
            status=form.status.data,
            priority=form.priority.data,
            description=form.description.data,
            internal_notes=form.internal_notes.data,
            invoice_status=form.invoice_status.data,
            is_recurring=form.is_recurring.data,
            recurrence_pattern=form.recurrence_pattern.data
        )
        for sid in form.services.data:
            service = Service.query.get(sid)
            if service:
                job.services.append(service)
        db.session.add(job)
        db.session.commit()
        flash('Job added successfully!', 'success')
        return redirect(url_for('main.jobs'))
    return render_template('jobs/add_job.html', form=form)

# ─── Expenses ──────────────────────────────────────────
@bp.route('/expenses', methods=['GET', 'POST'])
def expenses():
    form = ExpenseForm()
    form.job_id.choices = [(j.id, f"{j.client.name} - {j.service_type}") for j in Job.query.order_by(Job.date.desc())]
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    monthly_total = db.session.query(func.sum(Expense.amount)).filter(Expense.date >= datetime.now().replace(day=1)).scalar() or 0

    if form.validate_on_submit():
        expense = Expense(
            job_id=form.job_id.data or None,
            category=form.category.data,
            subcategory=form.subcategory.data,
            description=form.description.data,
            amount=form.amount.data,
            tax_amount=form.tax_amount.data or 0.0,
            date=form.date.data,
            vendor=form.vendor.data,
            is_billable=form.is_billable.data
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense saved!', 'success')
        return redirect(url_for('main.expenses'))

    return render_template('expenses/expense_form.html', form=form, expense=None, expenses=expenses, monthly_total=monthly_total, MATERIAL_SUBCATEGORIES=[label for _, label in MATERIAL_SUBCATEGORIES], LABOR_SUBCATEGORIES=[label for _, label in LABOR_SUBCATEGORIES])

# ─── Static Files ─────────────────────────────────────
@bp.route('/receipts/<filename>')
def view_receipt(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/client_photos/<filename>')
def view_client_photo(filename):
    return send_from_directory(PHOTO_FOLDER, filename)
