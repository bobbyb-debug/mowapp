# app/models.py

from datetime import datetime
from app import db

# Association table for many-to-many relationship between Job and Service
job_services = db.Table(
    'job_services',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    business_name = db.Column(db.String(128))
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    phone = db.Column(db.String(20), nullable=False)
    alt_phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    tax_id = db.Column(db.String(20))
    billing_notes = db.Column(db.Text)
    general_notes = db.Column(db.Text)
    photo = db.Column(db.String(255))

    jobs = db.relationship('Job', backref='client', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'business_name': self.business_name,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'phone': self.phone,
            'alt_phone': self.alt_phone,
            'email': self.email,
            'tax_id': self.tax_id,
            'billing_notes': self.billing_notes,
            'general_notes': self.general_notes,
            'photo': self.photo
        }

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    rate = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rate': self.rate
        }

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)

    services = db.relationship('Service', secondary=job_services, backref=db.backref('jobs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'date': self.date.isoformat(),
            'total_amount': self.total_amount,
            'notes': self.notes,
            'services': [service.to_dict() for service in self.services]
        }

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(255))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    receipt_filename = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'amount': self.amount,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'notes': self.notes
        }
