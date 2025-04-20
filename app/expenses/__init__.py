from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, Response, make_response, session
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.extensions import db
from app.models import Job, Expense
from app.forms import ExpenseForm

bp = Blueprint('expenses', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../static/receipts')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.route('/expenses', methods=['GET', 'POST'])
def record_expense():
    form = ExpenseForm()
    form.job_id.choices = [(j.id, f"{j.name}") for j in Job.query.order_by(Job.name.asc())]

    if form.validate_on_submit():
        expense = Expense(
            job_id=form.job_id.data,
            category=form.category.data,
            description=form.description.data,
            amount=form.amount.data,
            date=form.date.data
        )
        if form.receipt.data:
            filename = secure_filename(form.receipt.data.filename)
            receipt_path = os.path.join(UPLOAD_FOLDER, filename)
            form.receipt.data.save(receipt_path)
            expense.receipt_filename = filename

        db.session.add(expense)
        db.session.commit()
        flash("Expense added!", "success")
        return redirect(url_for("expenses.record_expense"))

    expenses = Expense.query.order_by(Expense.date.desc()).limit(50).all()
    monthly_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.date >= datetime.now() - timedelta(days=30)
    ).scalar() or 0

    return render_template("expense_form.html", form=form, expenses=expenses, monthly_total=monthly_total)

# + PDF, CSV, delete_expense and view_receipt routes exactly as before
