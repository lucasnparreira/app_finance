from flask import Flask, request, jsonify
import sqlite3
from models import init_db

app =Flask(__name__)
init_db()

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    description = data['description']
    amount = data['amount']
    type_val = data['type_val']
    date = data['date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (description, amount, type_val, date)
        VALUES (?, ?, ?, ?)
''', (description, amount, type_val, date))
    conn.commit()
    conn.close()
    return jsonify({'message':'Transaction added successfully!'}), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()

    return jsonify(transactions)

@app.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()

    if transaction:
        return jsonify(transaction)
    else:
        return jsonify({'message': 'Transaction not found!'}), 404
    
@app.route('/transactions/<int:id>', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    description = data['description']
    amount = data['amount']
    type_val = data['type_val']
    date = data['date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET description = ?, amount = ?, type_val = ?, date = ?
        WHERE id = ?
''', (description, amount, type_val, date, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Transaction updated successfully!'})

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Transaction deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True)