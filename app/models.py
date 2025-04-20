# filepath: app/models.py
from app.extensions import db
from datetime import datetime

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    receipt_filename = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    job = db.relationship('Job', backref='expenses')

    def __repr__(self):
        return f'<Expense {self.description} ${self.amount}>'

job_services = db.Table('job_services',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    services = db.relationship('Service', secondary=job_services, backref='jobs')

    def __repr__(self):
        return f'<Job {self.name}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
