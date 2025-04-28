# app/routes/api.py (or wherever your API routes are)

from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Expense
from datetime import datetime
# app/routes/api.py

from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)

# In-memory for now:
services_storage = [
    {"id": 1, "name": "Basic Mowing", "price": 35},
    {"id": 2, "name": "Premium Maintenance", "price": 75},
    {"id": 3, "name": "Complete Landscaping", "price": 150},
]

@api_bp.route('/api/services', methods=['GET', 'POST'])
def services():
    global services_storage
    if request.method == 'GET':
        return jsonify(services_storage)

    if request.method == 'POST':
        services_storage = request.json
        return jsonify({"message": "Services saved successfully."}), 200

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'GET':
        expenses = Expense.query.all()
        return jsonify([
            {
                "id": e.id,
                "date": e.date.isoformat(),  # Convert date to string for JSON
                "category": e.category,
                "subcategory": e.subcategory,
                "amount": e.amount,
                "description": e.description,
                "notes": e.notes
            }
            for e in expenses
        ])
    
    if request.method == 'POST':
        data = request.get_json()

        expense = Expense(
            date=datetime.fromisoformat(data['date']).date(),  # safely parse ISO date
            category=data['category'],
            subcategory=data['subcategory'],
            amount=data['amount'],
            description=data['description'],
            notes=data.get('notes', "")
        )
        db.session.add(expense)
        db.session.commit()

        return jsonify({"message": "Expense added successfully"}), 201
# app/routes/api.py

@api_bp.route('/api/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    data = request.get_json()
    expense = Expense.query.get_or_404(id)

    expense.date = datetime.fromisoformat(data['date']).date()
    expense.category = data['category']
    expense.subcategory = data['subcategory']
    expense.amount = data['amount']
    expense.description = data['description']
    expense.notes = data['notes']

    db.session.commit()

    return jsonify({"message": "Expense updated successfully"}), 200

@api_bp.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200
