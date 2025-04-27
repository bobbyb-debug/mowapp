from app.extensions import db

# Association table for many-to-many between Job and Service
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

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    rate = db.Column(db.Float, nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)

    services = db.relationship('Service', secondary=job_services, backref=db.backref('jobs', lazy=True))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(64))
    subcategory = db.Column(db.String(64))
    notes = db.Column(db.Text)
