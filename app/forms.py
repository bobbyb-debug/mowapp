from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, DateField, TimeField,
    DecimalField, IntegerField, SelectField, SelectMultipleField,
    BooleanField, FileField, SubmitField
)
from wtforms.validators import DataRequired, Email, Optional, NumberRange
import enum
class JobStatus(enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class InvoiceStatus(enum.Enum):
    UNPAID = "Unpaid"
    PAID = "Paid"
    OVERDUE = "Overdue"

class PriorityLevel(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# ─── Subcategories ─────────────────────────────────────────────

MATERIAL_SUBCATEGORIES = [
    ('Fertilizer', 'Fertilizer'),
    ('Mulch', 'Mulch'),
    ('Plants', 'Plants'),
    ('Irrigation', 'Irrigation Supplies'),
    ('Other', 'Other Material')
]

LABOR_SUBCATEGORIES = [
    ('Mowing', 'Mowing'),
    ('Trimming', 'Trimming'),
    ('Leaf Cleanup', 'Leaf Cleanup'),
    ('Install', 'Install Work'),
    ('Other', 'Other Labor')
]

# ─── Enum Choice Utilities ─────────────────────────────────────

def get_status_choices():
    return [(status.value, status.value) for status in JobStatus]

def get_invoice_status_choices():
    return [(status.value, status.value) for status in InvoiceStatus]

def get_priority_choices():
    return [(priority.value, priority.value) for priority in PriorityLevel]

# ─── Client Form ───────────────────────────────────────────────

class ClientForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    business_name = StringField('Business Name')
    street_address = StringField('Street Address')
    city = StringField('City')
    state = StringField('State', render_kw={"maxlength": 2})
    zip_code = StringField('ZIP Code', render_kw={"maxlength": 10})
    phone = StringField('Phone', validators=[DataRequired()])
    alt_phone = StringField('Alternate Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    tax_id = StringField('Tax ID')
    billing_notes = TextAreaField('Billing Notes')
    general_notes = TextAreaField('General Notes')
    photo = FileField('Client Photo')
    submit = SubmitField('Save Client')

# ─── Contact Form ──────────────────────────────────────────────

class ContactForm(FlaskForm):
    name = StringField('Contact Name', validators=[DataRequired()])
    title = StringField('Title')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    is_primary = BooleanField('Primary Contact')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Contact')

# ─── Job Form ──────────────────────────────────────────────────

class JobForm(FlaskForm):
    client_id = SelectField('Client', coerce=int, validators=[DataRequired()])
    title = StringField('Job Title', validators=[DataRequired()])
    service_type = StringField('Service Type', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M')
    end_time = TimeField('End Time', format='%H:%M')
    cost = DecimalField('Cost', places=2, validators=[DataRequired(), NumberRange(min=0)])
    estimated_cost = DecimalField('Estimated Cost', places=2, validators=[Optional(), NumberRange(min=0)])
    status = SelectField('Status', choices=get_status_choices(), default=JobStatus.PENDING.value)
    priority = SelectField('Priority', choices=get_priority_choices(), default=PriorityLevel.MEDIUM.value)
    description = TextAreaField('Description')
    internal_notes = TextAreaField('Internal Notes')
    invoice_status = SelectField('Invoice Status', choices=get_invoice_status_choices(), default=InvoiceStatus.UNPAID.value)
    is_recurring = BooleanField('Recurring Job')
    recurrence_pattern = StringField('Recurrence Pattern')
    services = SelectMultipleField('Services', coerce=int)
    submit = SubmitField('Save Job')

# ─── Expense Form ──────────────────────────────────────────────

class ExpenseForm(FlaskForm):
    job_id = SelectField('Associated Job', coerce=int)
    category = SelectField('Category', choices=[
        ('Materials', 'Materials'),
        ('Labor', 'Labor'),
        ('Equipment', 'Equipment'),
        ('Travel', 'Travel'),
        ('Meals', 'Meals'),
        ('Office', 'Office'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    subcategory = SelectField('Subcategory', choices=[], validators=[Optional()])
    description = StringField('Description', validators=[DataRequired()])
    amount = DecimalField('Amount', places=2, validators=[DataRequired(), NumberRange(min=0.01)])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    receipt = FileField('Receipt')
    is_billable = BooleanField('Billable to Client', default=True)
    tax_amount = DecimalField('Tax Amount', places=2, default=0.0, validators=[Optional(), NumberRange(min=0)])
    vendor = StringField('Vendor')
    submit = SubmitField('Save Expense')

# ─── Mileage Form ──────────────────────────────────────────────

class MileageForm(FlaskForm):
    job_id = SelectField('Associated Job', coerce=int)
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_location = StringField('Start Location')
    end_location = StringField('End Location')
    distance = DecimalField('Distance (miles)', places=2, validators=[DataRequired(), NumberRange(min=0.1)])
    vehicle = StringField('Vehicle')
    purpose = StringField('Purpose')
    rate = DecimalField('Rate per mile', places=2, default=0.58, validators=[DataRequired(), NumberRange(min=0)])
    is_billable = BooleanField('Billable to Client', default=True)
    submit = SubmitField('Save Mileage')

# ─── Service Form ──────────────────────────────────────────────

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    base_price = DecimalField('Base Price', places=2, validators=[Optional(), NumberRange(min=0)])
    category = StringField('Category')
    is_active = BooleanField('Active', default=True)
    estimated_duration = DecimalField('Estimated Hours', places=2, validators=[Optional(), NumberRange(min=0.25)])
    skill_level = SelectField('Skill Level', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ])
    required_certifications = TextAreaField('Required Certifications')
    default_crew_size = IntegerField('Default Crew Size', validators=[Optional(), NumberRange(min=1)])
    submit = SubmitField('Save Service')

# ─── Document Form ─────────────────────────────────────────────

class DocumentForm(FlaskForm):
    name = StringField('Document Name', validators=[DataRequired()])
    file = FileField('File', validators=[DataRequired()])
    description = TextAreaField('Description')
    is_contract = BooleanField('Is Contract')
    is_invoice = BooleanField('Is Invoice')
    job_id = SelectField('Associated Job', coerce=int)
    client_id = SelectField('Associated Client', coerce=int)
    submit = SubmitField('Upload Document')
