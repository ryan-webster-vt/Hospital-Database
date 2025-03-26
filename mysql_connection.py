import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password2357!',
    'database': 'Hospital'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_patient():
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    phone_number = request.form['phone_number']
    medical_record_id = request.form['medical_record_id']
    insurance_id = request.form['insurance_id']
    
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Patients 
        (first_name, middle_name, last_name, date_of_birth, phone_number, medical_record_id, insurance_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (first_name, middle_name, last_name, date_of_birth, phone_number, medical_record_id, insurance_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)