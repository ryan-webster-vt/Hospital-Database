from flask import Flask, render_template, request, redirect
from mysql_connection import connect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", message="Hospital Database System")

@app.route("/insert", methods=["POST"])
def insert():
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO Patients (name, age, gender, diagnosis) VALUES (%s, %s, %s, %s)"
    data = (
        request.form['name'],
        request.form['age'],
        request.form['gender'],
        request.form['diagnosis']
    )
    cursor.execute(sql, data)
    db.commit()
    return render_template("index.html", message="Patient added successfully!")

@app.route("/delete", methods=["POST"])
def delete():
    db = connect()
    cursor = db.cursor()
    sql = "DELETE FROM Patients WHERE patient_id = %s"
    cursor.execute(sql, (request.form['patient_id'],))
    db.commit()
    return render_template("index.html", message="Patient deleted successfully!")

if __name__ == "__main__":
    app.run(debug=True)
