from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from app.models import Job

class ExpenseForm(FlaskForm):
    job_id = SelectField('Job', coerce=int, validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    receipt = StringField('Receipt')
    submit = SubmitField('Submit')

    def populate_job_choices(self):
        self.job_id.choices = [(job.id, job.name) for job in Job.query.all()]
