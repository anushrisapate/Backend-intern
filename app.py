from flask import request, jsonify
from app import app, db

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    required = ['amount', 'description', 'paid_by']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400

    expense = {
        'amount': float(data['amount']),
        'description': data['description'],
        'paid_by': data['paid_by'],
        'split_type': data.get('split_type', 'equal'),
        'splits': data.get('splits', []),
    }
    db.expenses.insert_one(expense)
    return jsonify({'success': True, 'message': 'Expense added successfully'}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = list(db.expenses.find({}, {'_id': 0}))
    return jsonify(expenses)

@app.route('/expenses/<string:description>', methods=['PUT'])
def update_expense(description):
    update_data = request.get_json()
    result = db.expenses.update_one({'description': description}, {'$set': update_data})
    if result.modified_count == 0:
        return jsonify({'message': 'No expense updated'}), 404
    return jsonify({'message': 'Expense updated successfully'})

@app.route('/expenses/<string:description>', methods=['DELETE'])
def delete_expense(description):
    result = db.expenses.delete_one({'description': description})
    if result.deleted_count == 0:
        return jsonify({'message': 'Expense not found'}), 404
    return jsonify({'message': 'Expense deleted successfully'})
