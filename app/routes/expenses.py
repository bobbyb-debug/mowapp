from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Expense
from app import db

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/')
def expense_list():
    expenses = Expense.query.all()
    return render_template('expenses/expenses_list.html', expenses=expenses)

@expenses_bp.route('/new', methods=['GET', 'POST'])
def new_expense():
    if request.method == 'POST':
        description = request.form.get('description')
        amount = request.form.get('amount')
        if description and amount:
            expense = Expense(description=description, amount=float(amount))
            db.session.add(expense)
            db.session.commit()
            return redirect(url_for('expenses.expense_list'))
    return render_template('expenses/new_expense.html')
