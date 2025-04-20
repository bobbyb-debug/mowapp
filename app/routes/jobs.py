from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Job
from app import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
def job_list():
    jobs = Job.query.all()
    return render_template('jobs/jobs_list.html', jobs=jobs)

@jobs_bp.route('/new', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        job_name = request.form.get('job_name')
        if job_name:
            job = Job(name=job_name)
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('jobs.job_list'))
    return render_template('jobs/new_job.html')
