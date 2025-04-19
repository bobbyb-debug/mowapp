# app/models.py
from datetime import datetime
from app import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    business_name = db.Column(db.String(120))
    street_address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone = db.Column(db.String(20), nullable=False)
    alt_phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    tax_id = db.Column(db.String(20))
    billing_notes = db.Column(db.Text)
    general_notes = db.Column(db.Text)
    photo_filename = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship('Job', backref='client', lazy=True)
    documents = db.relationship('Document', backref='client', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    service_type = db.Column(db.String(100))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    estimated_cost = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))
    priority = db.Column(db.String(50))
    description = db.Column(db.Text)
    internal_notes = db.Column(db.Text)
    invoice_status = db.Column(db.String(50))
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship('Service', secondary='job_services', backref='jobs')
    expenses = db.relationship('Expense', backref='job', lazy=True)
    mileage_logs = db.relationship('Mileage', backref='job', lazy=True)
    documents = db.relationship('Document', backref='job', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50))
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0.0)
    date = db.Column(db.Date, nullable=False)
    vendor = db.Column(db.String(100))
    receipt_filename = db.Column(db.String(200))
    is_billable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Mileage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    date = db.Column(db.Date, nullable=False)
    start_location = db.Column(db.String(200))
    end_location = db.Column(db.String(200))
    distance = db.Column(db.Numeric(10, 2), nullable=False)
    vehicle = db.Column(db.String(100))
    purpose = db.Column(db.String(200))
    rate = db.Column(db.Numeric(5, 2), default=0.58)
    is_billable = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    base_price = db.Column(db.Numeric(10, 2))
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    estimated_duration = db.Column(db.Numeric(5, 2))
    skill_level = db.Column(db.String(50))
    required_certifications = db.Column(db.Text)
    default_crew_size = db.Column(db.Integer)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    file = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_contract = db.Column(db.Boolean, default=False)
    is_invoice = db.Column(db.Boolean, default=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ─── Association Table ────────────────────────────────
job_services = db.Table('job_services',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
)
