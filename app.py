from flask import Flask, redirect, render_template, request, jsonify, url_for
import sqlite3
from models import init_db

app =Flask(__name__)
init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect('database.db')
    if request.method == 'POST':
        search_query = request.form['search_query']
        transactions = conn.execute('SELECT * FROM transactions WHERE description LIKE ?', ('%' + search_query + '%',)).fetchall()
    else:
        transactions = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return render_template('view_transactions.html', transactions=transactions)


@app.route('/add', methods=['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        type_val = request.form['type_val']
        date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (description, amount, type_val, date)
            VALUES (?, ?, ?, ?)
    ''', (description, amount, type_val, date))
        conn.commit()
        conn.close()
        return redirect(url_for('view_transactions'))
    return render_template('add_transaction.html')

@app.route('/transactions', methods=['GET'])
def view_transactions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()

    return render_template('view_transactions.html', transactions=transactions)

@app.route('/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()

    if transaction:
        return render_template('view_transactions.html')
    else:
        return jsonify({'message': 'Transaction not found!'}), 404
    
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_transaction(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        type_val = request.form['type_val']
        date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET description = ?, amount = ?, type_val = ?, date = ?
            WHERE id = ?
    ''', (description, amount, type_val, date, id))
        conn.commit()
        conn.close()

        return redirect(url_for('view_transactions'))
    
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()

    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/transactions/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('view_transactions'))


if __name__ == '__main__':
    app.run(debug=True)