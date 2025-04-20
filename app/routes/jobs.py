from flask import Blueprint, render_template, request, redirect, url_for
from app import db

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/', methods=['GET'])
def jobs_home():
    return render_template('jobs.html')

@jobs_bp.route('/list')
def job_list():
    from app.models import Job
    jobs = Job.query.all()
    return render_template('jobs/jobs_list.html', jobs=jobs)

@jobs_bp.route('/new', methods=['GET', 'POST'])
def new_job():
    from app.models import Job, Service
    if request.method == 'POST':
        job_name = request.form.get('job_name')
        service_ids = request.form.getlist('services')  # Get selected services
        if job_name:
            job = Job(name=job_name)
            if service_ids:
                services = Service.query.filter(Service.id.in_(service_ids)).all()
                job.services.extend(services)
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('jobs.job_list'))
    services = Service.query.all()  # Query all services
    return render_template('jobs/add_job.html', services=services)
