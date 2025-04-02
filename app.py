from flask import Flask, render_template, request, redirect, flash
from mysql_connection import get_connection
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Redirect to the list route to always show patients
    return redirect("/list")

@app.route("/insert", methods=["POST"])
def insert():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        sql = """INSERT INTO patients 
                (first_name, middle_name, last_name, date_of_birth, phone_number, insurance_id) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        
        # Handle middle name (could be empty)
        middle_name = request.form['middle_name']
        if not middle_name:
            middle_name = None
                        
        insurance_id = request.form.get('insurance_id')
        if insurance_id == "":
            insurance_id = None
        
        data = (
            request.form['first_name'],
            middle_name,
            request.form['last_name'],
            request.form['date_of_birth'],
            request.form['phone_number'],
            insurance_id
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
        # Get the ID of the inserted patient for the success message
        patient_id = cursor.lastrowid
        
        # Get medical records and insurance options for the form
        cursor.execute("SELECT medical_record_id, sex, height FROM medical_record")
        medical_records = cursor.fetchall()
        
        cursor.execute("SELECT insurance_id, name FROM insurances")
        insurances = cursor.fetchall()
        
        return redirect("/list?message=Patient added successfully with ID: " + str(patient_id))
    except Exception as e:
        return redirect(f"/list?message=Error adding patient: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/update_medical_record", methods=["POST"])
def update_medical_record():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        patient_id = request.form['patient_id']
        medical_record_id = request.form.get('medical_record_id')
        
        # Check if the patient already has a medical record
        cursor.execute("SELECT medical_record_id FROM patients WHERE patient_id = %s", (patient_id,))
        patient_data = cursor.fetchone()
        
        if patient_data and patient_data[0]:
            # Patient already has a medical record - update it
            update_sql = """
                UPDATE medical_record 
                SET sex = %s, height = %s, vaccination_count = %s 
                WHERE medical_record_id = %s
            """
            update_data = (
                request.form['sex'],
                request.form['height'],
                request.form['vaccination_count'],
                patient_data[0]
            )
            cursor.execute(update_sql, update_data)
            connection.commit()
        else:
            # Patient doesn't have a medical record - create a new one and assign it
            create_sql = "INSERT INTO medical_record (sex, height, vaccination_count) VALUES (%s, %s, %s)"
            create_data = (
                request.form['sex'],
                request.form['height'],
                request.form['vaccination_count']
            )
            cursor.execute(create_sql, create_data)
            connection.commit()
            
            # Get the ID of the new medical record
            new_medical_record_id = cursor.lastrowid
            
            # Assign the new medical record to the patient
            assign_sql = "UPDATE patients SET medical_record_id = %s WHERE patient_id = %s"
            assign_data = (new_medical_record_id, patient_id)
            cursor.execute(assign_sql, assign_data)
            connection.commit()
        
        # Get patient details for success message
        patient_sql = "SELECT first_name, last_name FROM patients WHERE patient_id = %s"
        cursor.execute(patient_sql, (patient_id,))
        patient = cursor.fetchone()
        
        return redirect(f"/list?message=Medical record updated for {patient[0]} {patient[1]}")
    except Exception as e:
        return redirect(f"/list?message=Error updating medical record: {str(e)}")
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
            return redirect("/list?message=No patient found with that ID")
        
        # Delete the patient
        sql = "DELETE FROM patients WHERE patient_id = %s"
        cursor.execute(sql, (request.form['patient_id'],))
        connection.commit()
        
        return redirect(f"/list?message=Patient {patient[0]} {patient[1]} (ID: {request.form['patient_id']}) deleted successfully!")
    except Exception as e:
        return redirect(f"/list?message=Error deleting patient: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/list")
def list_patients():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Select patients with join to get medical record and insurance info
        cursor.execute("""
            SELECT p.patient_id, p.first_name, p.middle_name, p.last_name, 
                   p.date_of_birth, p.phone_number, 
                   m.sex, m.height, i.name as insurance_name, m.vaccination_count, m.medical_record_id
            FROM patients p
            LEFT JOIN medical_record m ON p.medical_record_id = m.medical_record_id
            LEFT JOIN insurances i ON p.insurance_id = i.insurance_id
            ORDER BY p.patient_id DESC
        """)
        patients = cursor.fetchall()
        
        # Get medical records and insurance options for the form
        cursor.execute("SELECT medical_record_id, sex, height FROM medical_record")
        medical_records = cursor.fetchall()
        
        cursor.execute("SELECT insurance_id, name FROM insurances")
        insurances = cursor.fetchall()
        
        # Check if there's a message in the URL parameters
        message = request.args.get('message', "Hospital Database System")
        
        return render_template("index.html", 
                             message=message,
                             patients=patients,
                             medical_records=medical_records,
                             insurances=insurances)
    except Exception as e:
        return render_template("index.html", message=f"Error listing patients: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
