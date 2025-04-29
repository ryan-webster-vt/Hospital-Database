from flask import Flask, render_template, request, redirect, flash, session, url_for
from mysql_connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    # Redirect to the list route to always show patients
    username = session.get('user')
    return redirect("/list")

@app.route("/insert", methods=["POST"])
def insert():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # First create medical record
        med_sql = """INSERT INTO medical_record 
                    (sex, height, vaccination_count) 
                    VALUES (%s, %s, %s)"""
        
        med_data = (
            request.form['sex'],
            request.form['height'],
            request.form.get('vaccination_count', 0)
        )
        
        cursor.execute(med_sql, med_data)
        connection.commit()
        
        # Get the new medical record ID
        medical_record_id = cursor.lastrowid
        
        # Now insert patient with the medical record ID
        sql = """INSERT INTO patients 
                (first_name, middle_name, last_name, date_of_birth, phone_number, insurance_id, medical_record_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        
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
            insurance_id,
            medical_record_id  # Include medical record ID
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
        # Get the ID of the inserted patient for the success message
        patient_id = cursor.lastrowid
        
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
#@login_required(role="patient")
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

# Adds user to user table
def create_user(username, password, role, patient_id=None):
    connection = get_connection()
    cursor = connection.cursor()
    hashed_pw = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash, role, patient_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (username, hashed_pw, role, patient_id))
    connection.commit()
    connection.close()

def validate_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, password_hash, role, patient_id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    connection.close()
    if result and check_password_hash(result[1], password):
        return {"user_id": result[0], "username": username, "role": result[2], "patient_id": result[3]}
    return None

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        # Only try to get patient_id if the role is 'patient'
        patient_id = None
        if role == 'patient' and 'patient_id' in request.form and request.form['patient_id']:
            patient_id = request.form['patient_id']
        
        try:
            create_user(username, password, role, patient_id)
            flash(f"Account created successfully! Please log in.")
            return redirect("/login")
        except Exception as e:
            flash(f"Error creating account: {str(e)}")
    
    # Get list of patients for the dropdown - only needed for the patient role
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT patient_id, first_name, last_name FROM patients ORDER BY last_name, first_name")
    patients = cursor.fetchall()
    connection.close()
    
    return render_template("signup.html", patients=patients)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        user = validate_user(request.form["username"], request.form["password"])
        if user:
            session["user"] = user
            flash(f"Welcome, {user['username']}!")
            return redirect("/list")
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("You have been logged out successfully.")
    return redirect("/login")

@app.route("/change_password", methods = ["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect("/login")
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = generate_password_hash(new_password)
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (hashed_password, session["user"]["user_id"]))
        connection.commit()
        connection.close()
        flash("Password changed successfully.")
        return redirect("/list")
    return render_template("change_password.html")

def login_required(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                return redirect("/login")
            if role and session["user"]["role"] != role:
                return "Access Denied", 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route("/admin/create_user", methods=["GET", "POST"])
@login_required(role="admin")
def admin_create_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        # Only try to get patient_id if the role is 'patient'
        patient_id = None
        if role == 'patient' and 'patient_id' in request.form and request.form['patient_id']:
            patient_id = request.form['patient_id']
        
        try:
            create_user(username, password, role, patient_id)
            flash(f"User '{username}' created successfully as {role}.")
            return redirect("/admin/create_user")
        except Exception as e:
            flash(f"Error creating user: {str(e)}")
    
    # Get list of patients for the dropdown
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT patient_id, first_name, last_name FROM patients ORDER BY last_name, first_name")
    patients = cursor.fetchall()
    connection.close()
    
    return render_template("admin_create_user.html", patients=patients)

# --------------------------
# New Statistical Reports Routes
# --------------------------

# ADMIN STATISTICS
@app.route("/stats/admin")
@login_required(role="admin")
def admin_stats():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # 1. Total number of patients
        cursor.execute("SELECT COUNT(*) FROM patients")
        total_patients = cursor.fetchone()[0]

        # 2. Average age of patients (calculate age using TIMESTAMPDIFF in years)
        cursor.execute("SELECT AVG(TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE())) FROM patients")
        avg_age = cursor.fetchone()[0]

        # 3. Total gross bill amounts (SUM)
        cursor.execute("SELECT SUM(gross_cost) FROM bills")
        total_bills = cursor.fetchone()[0]

        # 4. Minimum and Maximum bill amounts (MIN and MAX)
        cursor.execute("SELECT MIN(gross_cost), MAX(gross_cost) FROM bills")
        min_bill, max_bill = cursor.fetchone()

        # 5. Average vaccination count across all medical records (AVG)
        cursor.execute("SELECT AVG(vaccination_count) FROM medical_record")
        avg_vaccinations = cursor.fetchone()[0]

        return render_template("admin_stats.html", 
                               total_patients=total_patients, 
                               avg_age=avg_age,
                               total_bills=total_bills, 
                               min_bill=min_bill, 
                               max_bill=max_bill, 
                               avg_vaccinations=avg_vaccinations)
    except Exception as e:
        return f"Error generating admin statistics: {str(e)}"
    finally:
        if 'connection' in locals():
            connection.close()

# DOCTOR STATISTICS
@app.route("/stats/doctor")
@login_required(role="doctor")
def doctor_stats():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # 1. Total number of doctors in the hospital
        cursor.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = cursor.fetchone()[0]

        # 2. Average number of patients treated per doctor (from treats table)
        cursor.execute("""
            SELECT AVG(patient_count) 
            FROM (SELECT COUNT(*) AS patient_count FROM treats GROUP BY doctor_id) AS sub
        """)
        avg_patients = cursor.fetchone()[0]

        # 3. Average gross bill amount per doctor (by aggregating bills grouped by doctor)
        cursor.execute("""
            SELECT AVG(bill_sum) 
            FROM (SELECT SUM(gross_cost) AS bill_sum FROM bills GROUP BY doctor_id) AS sub
        """)
        avg_bill_per_doctor = cursor.fetchone()[0]

        # 4. Prescription dosage statistics (MIN, MAX, AVG) for prescriptions by doctors
        cursor.execute("SELECT MIN(dosage), MAX(dosage), AVG(dosage) FROM prescriptions")
        min_dosage, max_dosage, avg_dosage = cursor.fetchone()

        # 5. Average number of prescriptions issued per doctor
        cursor.execute("""
            SELECT AVG(prescription_count) 
            FROM (SELECT COUNT(*) AS prescription_count FROM prescriptions GROUP BY doctor_id) AS sub
        """)
        avg_prescriptions_per_doctor = cursor.fetchone()[0]

        return render_template("doctor_stats.html", 
                               total_doctors=total_doctors, 
                               avg_patients=avg_patients,
                               avg_bill_per_doctor=avg_bill_per_doctor, 
                               min_dosage=min_dosage, 
                               max_dosage=max_dosage, 
                               avg_dosage=avg_dosage,
                               avg_prescriptions_per_doctor=avg_prescriptions_per_doctor)
    except Exception as e:
        return f"Error generating doctor statistics: {str(e)}"
    finally:
        if 'connection' in locals():
            connection.close()

# NURSE STATISTICS
@app.route("/stats/nurse")
@login_required(role="nurse")
def nurse_stats():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        # 1. Total number of nurses in the hospital
        cursor.execute("SELECT COUNT(*) FROM nurses")
        total_nurses = cursor.fetchone()[0]

        # 2. Average number of patients cared for per nurse (via the cares table)
        cursor.execute("""
            SELECT AVG(patient_count) 
            FROM (SELECT COUNT(*) AS patient_count FROM cares GROUP BY nurse_id) AS sub
        """)
        avg_patients_per_nurse = cursor.fetchone()[0]

        # 3. Overall patient height statistics (MIN, MAX, AVG) for patients cared for by nurses
        cursor.execute("""
            SELECT MIN(m.height), MAX(m.height), AVG(m.height)
            FROM medical_record m
            JOIN patients p ON m.medical_record_id = p.medical_record_id
            JOIN cares c ON p.patient_id = c.patient_id
        """)
        min_height, max_height, avg_height = cursor.fetchone()

        # 4. Total sum of vaccination counts among patients under nurse care
        cursor.execute("""
            SELECT SUM(m.vaccination_count)
            FROM medical_record m
            JOIN patients p ON m.medical_record_id = p.medical_record_id
            JOIN cares c ON p.patient_id = c.patient_id
        """)
        total_vaccinations = cursor.fetchone()[0]

        # 5. Average vaccination count per nurse (using a subquery grouped by nurse_id)
        cursor.execute("""
            SELECT AVG(avg_vacc) 
            FROM (
                SELECT AVG(m.vaccination_count) AS avg_vacc 
                FROM medical_record m
                JOIN patients p ON m.medical_record_id = p.medical_record_id
                JOIN cares c ON p.patient_id = c.patient_id
                GROUP BY c.nurse_id
            ) AS sub
        """)
        avg_vaccination_per_nurse = cursor.fetchone()[0]

        return render_template("nurse_stats.html", 
                               total_nurses=total_nurses, 
                               avg_patients_per_nurse=avg_patients_per_nurse,
                               min_height=min_height, 
                               max_height=max_height, 
                               avg_height=avg_height,
                               total_vaccinations=total_vaccinations, 
                               avg_vaccination_per_nurse=avg_vaccination_per_nurse)
    except Exception as e:
        return f"Error generating nurse statistics: {str(e)}"
    finally:
        if 'connection' in locals():
            connection.close()

# PATIENT STATISTICS
@app.route("/stats/patient")
@login_required(role="patient")
def patient_stats():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Get the patient_id of the logged in user
        # Check if user has a patient_id associated with their account
        if 'user' in session and session['user'].get('patient_id'):
            patient_id = session['user']['patient_id']
            print(patient_id)
        else:
            return "Your user account is not linked to any patient record. Please contact the administrator."
        
        # Get patient name for displaying in the template
        cursor.execute("SELECT first_name, last_name FROM patients WHERE patient_id = %s", (patient_id,))
        patient_name = cursor.fetchone()
        
        if not patient_name:
            return "Patient record not found. Please contact the administrator."
            
        patient_fullname = f"{patient_name[0]} {patient_name[1]}"
        
        # 1. Number of appointments for this patient
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = %s", (patient_id,))
        appointments_count = cursor.fetchone()[0]

        # 2. Number of prescriptions received
        cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE patient_id = %s", (patient_id,))
        prescriptions_count = cursor.fetchone()[0]

        # 3. Total dosage amount from prescriptions (SUM)
        cursor.execute("SELECT SUM(dosage) FROM prescriptions WHERE patient_id = %s", (patient_id,))
        total_dosage = cursor.fetchone()[0]
        total_dosage = total_dosage if total_dosage else 0  # Handle None result

        # 4. Average prescription dosage (AVG)
        cursor.execute("SELECT AVG(dosage) FROM prescriptions WHERE patient_id = %s", (patient_id,))
        avg_dosage = cursor.fetchone()[0]
        avg_dosage = avg_dosage if avg_dosage else 0  # Handle None result

        # 5. Number of treatments received (from the treats table)
        cursor.execute("SELECT COUNT(*) FROM treats WHERE patient_id = %s", (patient_id,))
        treatments_count = cursor.fetchone()[0]

        # 6. Get medical record information for this patient
        cursor.execute("""
            SELECT m.sex, m.height, m.vaccination_count 
            FROM medical_record m
            JOIN patients p ON m.medical_record_id = p.medical_record_id
            WHERE p.patient_id = %s
        """, (patient_id,))
        medical_record = cursor.fetchone()
        
        # Set default values if no medical record exists
        sex = height = vaccination_count = "No data"
        if medical_record:
            sex = medical_record[0] if medical_record[0] else "Not specified"
            height = medical_record[1] if medical_record[1] else "Not specified"
            vaccination_count = medical_record[2] if medical_record[2] else 0

        return render_template("patient_stats.html",
                               patient_id=patient_id,
                               patient_name=patient_fullname,
                               appointments_count=appointments_count,
                               prescriptions_count=prescriptions_count,
                               total_dosage=total_dosage,
                               avg_dosage=avg_dosage,
                               treatments_count=treatments_count,
                               sex=sex,
                               height=height,
                               vaccination_count=vaccination_count)
    except Exception as e:
        return f"Error generating patient statistics: {str(e)}"
    finally:
        if 'connection' in locals():
            connection.close()

# --------------------------
# Appointment Management Routes
# --------------------------

@app.route("/appointments")
def list_appointments():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Get appointments with patient names
        cursor.execute("""
            SELECT a.appointment_id, a.date, a.time, a.patient_id, 
                   p.first_name, p.last_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            ORDER BY a.date ASC, a.time ASC
        """)
        appointments = cursor.fetchall()
        
        # Get patients for the dropdown
        cursor.execute("""
            SELECT patient_id, first_name, middle_name, last_name
            FROM patients
            ORDER BY last_name, first_name
        """)
        patients = cursor.fetchall()
        
        # Check if there's a message in the URL parameters
        message = request.args.get('message')
        
        return render_template("appointments.html", 
                             appointments=appointments,
                             patients=patients,
                             message=message)
    except Exception as e:
        return render_template("appointments.html", message=f"Error listing appointments: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/appointments/add", methods=["POST"])
def add_appointment():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        patient_id = request.form['patient_id']
        appointment_date = request.form['date']
        appointment_time = request.form['time']
        
        # First check if patient exists
        cursor.execute("SELECT first_name, last_name FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            return redirect("/appointments?message=No patient found with that ID")
        
        # Insert the appointment
        sql = """INSERT INTO appointments 
                (date, time, patient_id) 
                VALUES (%s, %s, %s)"""
        
        data = (
            appointment_date,
            appointment_time,
            patient_id
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
        appointment_id = cursor.lastrowid
        
        return redirect(f"/appointments?message=Appointment added successfully for {patient[0]} {patient[1]} at {appointment_time} on {appointment_date}")
    except Exception as e:
        return redirect(f"/appointments?message=Error adding appointment: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/appointments/update", methods=["POST"])
def update_appointment():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        appointment_id = request.form['appointment_id']
        patient_id = request.form['patient_id']
        appointment_date = request.form['date']
        appointment_time = request.form['time']
        
        # First check if patient exists
        cursor.execute("SELECT first_name, last_name FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            return redirect("/appointments?message=No patient found with that ID")
        
        # Update the appointment
        sql = """UPDATE appointments
                SET date = %s, time = %s, patient_id = %s
                WHERE appointment_id = %s"""
        
        data = (
            appointment_date,
            appointment_time,
            patient_id,
            appointment_id
        )
        
        cursor.execute(sql, data)
        connection.commit()
        
        return redirect(f"/appointments?message=Appointment updated successfully for {patient[0]} {patient[1]}")
    except Exception as e:
        return redirect(f"/appointments?message=Error updating appointment: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/appointments/delete", methods=["POST"])
def delete_appointment():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        appointment_id = request.form['appointment_id']
        
        # First get appointment details for confirmation message
        cursor.execute("""
            SELECT a.date, a.time, p.first_name, p.last_name 
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.appointment_id = %s
        """, (appointment_id,))
        
        appointment = cursor.fetchone()
        
        if not appointment:
            return redirect("/appointments?message=No appointment found with that ID")
        
        # Delete the appointment
        sql = "DELETE FROM appointments WHERE appointment_id = %s"
        cursor.execute(sql, (appointment_id,))
        connection.commit()
        
        return redirect(f"/appointments?message=Appointment for {appointment[2]} {appointment[3]} on {appointment[0]} at {appointment[1]} deleted successfully")
    except Exception as e:
        return redirect(f"/appointments?message=Error deleting appointment: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
