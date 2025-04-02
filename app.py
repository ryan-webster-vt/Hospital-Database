from flask import Flask, render_template, request, redirect, flash
from mysql_connection import get_connection
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        return render_template("index.html", message="Hospital Database System")
    except Exception as e:
        return render_template("index.html", message=f"Error: {str(e)}")

@app.route("/insert", methods=["POST"])
def insert():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        sql = """INSERT INTO patients 
                (first_name, last_name, date_of_birth, phone_number) 
                VALUES (%s, %s, %s, %s)"""
        data = (
            request.form['first_name'],
            request.form['last_name'],
            request.form['date_of_birth'],
            request.form['phone_number']
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
        # Get the ID of the inserted patient for the success message
        patient_id = cursor.lastrowid
        return render_template("index.html", message=f"Patient added successfully with ID: {patient_id}")
    except Exception as e:
        return render_template("index.html", message=f"Error adding patient: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/delete", methods=["POST"])
def delete():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # First check if patient exists
        check_sql = "SELECT first_name, last_name FROM patients WHERE patient_id = %s"
        cursor.execute(check_sql, (request.form['patient_id'],))
        patient = cursor.fetchone()
        
        if not patient:
            return render_template("index.html", message="No patient found with that ID")
        
        # Delete the patient
        sql = "DELETE FROM patients WHERE patient_id = %s"
        cursor.execute(sql, (request.form['patient_id'],))
        connection.commit()
        
        return render_template("index.html", 
                             message=f"Patient {patient[0]} {patient[1]} (ID: {request.form['patient_id']}) deleted successfully!")
    except Exception as e:
        return render_template("index.html", message=f"Error deleting patient: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/list")
def list_patients():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Select patients with a proper join
        cursor.execute("""
            SELECT p.patient_id, p.first_name, p.last_name, 
                   p.date_of_birth, p.phone_number 
            FROM patients p
            ORDER BY p.patient_id DESC
        """)
        patients = cursor.fetchall()
        
        return render_template("index.html", 
                             message="Hospital Database System",
                             patients=patients)
    except Exception as e:
        return render_template("index.html", message=f"Error listing patients: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
