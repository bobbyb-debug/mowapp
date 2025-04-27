# app/jobs/routes.py

from flask import Blueprint, render_template
from app.models import Job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/', methods=['GET'])
def jobs_home():
    jobs = Job.query.order_by(Job.date.desc()).all()
    return render_template('jobs.html', jobs=jobs)
