from flask import Flask, render_template, request, redirect, flash
from mysql_connection import get_connection

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
        
        sql = "INSERT INTO Patients (name, age, gender, diagnosis) VALUES (%s, %s, %s, %s)"
        data = (
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['diagnosis']
        )
        
        cursor.execute(sql, data)
        connection.commit()
        return render_template("index.html", message="Patient added successfully!")
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
        
        sql = "DELETE FROM Patients WHERE patient_id = %s"
        cursor.execute(sql, (request.form['patient_id'],))
        connection.commit()
        
        if cursor.rowcount == 0:
            return render_template("index.html", message="No patient found with that ID")
        return render_template("index.html", message="Patient deleted successfully!")
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
        
        cursor.execute("SELECT * FROM Patients ORDER BY created_at DESC")
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
