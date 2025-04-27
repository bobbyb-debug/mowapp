# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional, Email

class ClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    business_name = StringField('Business Name', validators=[Optional()])
    phone = StringField('Phone', validators=[DataRequired()])
    alt_phone = StringField('Alternate Phone', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    street_address = StringField('Street Address', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    zip_code = StringField('Zip Code', validators=[Optional()])
    tax_id = StringField('Tax ID', validators=[Optional()])
    billing_notes = TextAreaField('Billing Notes', validators=[Optional()])
    general_notes = TextAreaField('General Notes', validators=[Optional()])
    photo = FileField('Photo', validators=[Optional()])
