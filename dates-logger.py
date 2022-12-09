# Import necessary modules and libraries
import datetime
import sqlite3
from flask import Flask, request, render_template

# Create a Flask app
app = Flask(__name__)

# Create a database connection
conn = sqlite3.connect('expiration_dates.db')
cursor = conn.cursor()

# Create a table to store expiration dates
cursor.execute('''
    CREATE TABLE expiration_dates (
        id INTEGER PRIMARY KEY,
        product_name TEXT,
        expiry_date DATE
    )
''')

# Function to add a new expiration date
def add_expiry_date(product_name, expiry_date):
    cursor.execute('''
        INSERT INTO expiration_dates (product_name, expiry_date)
        VALUES (?, ?)
    ''', (product_name, expiry_date))
    conn.commit()

# Function to retrieve all expiration dates
def get_expiry_dates():
    cursor.execute('''
        SELECT * FROM expiration_dates
    ''')
    return cursor.fetchall()

# Function to check if a product has expired
def is_expired(product_name):
    cursor.execute('''
        SELECT * FROM expiration_dates
        WHERE product_name = ? AND expiry_date < ?
    ''', (product_name, datetime.date.today()))
    return cursor.fetchone()

# Route to add a new expiration date
@app.route('/add_expiry_date', methods=['POST'])
def add_expiry_date_route():
    product_name = request.form['product_name']
    expiry_date = datetime.datetime.strptime(request.form['expiry_date'], '%Y-%m-%d').date()
    add_expiry_date(product_name, expiry_date)
    return 'Expiration date added successfully'

# Route to retrieve all expiration dates
@app.route('/get_expiry_dates')
def get_expiry_dates_route():
    expiry_dates = get_expiry_dates()
    return render_template('expiry_dates.html', expiry_dates=expiry_dates)

# Route to check if a product has expired
@app.route('/is_expired')
def is_expired_route():
    product_name = request.args.get('product_name')
    expired = is_expired(product_name)
    return 'Product has expired' if expired else 'Product has not expired'

# Run the app
if __name__ == '__main__':
    app.run()
