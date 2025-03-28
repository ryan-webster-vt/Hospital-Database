from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Database configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password2357!',
    'database': 'Hospital'
}

@app.route('/')
def home():
    try:
        # Try to connect to the database
        connection = pymysql.connect(**config)

        # If connection is successful, display the message
        connection.close()
        return render_template('index.html', message="Connected to the Database!")

    except pymysql.MySQLError as err:
        # If there's an error, display the error message
        return render_template('index.html', message=f"Error: {err}")

if __name__ == '__main__':
    app.run(debug=True)
