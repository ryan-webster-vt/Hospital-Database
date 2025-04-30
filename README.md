# Hospital Management System Database
## Instructions
### Clone the Repository
```bash
git clone https://github.com/ryan-webster-vt/Hospital-Database.git
cd \path\
```
### Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
### Install Python Dependencies
```bash
pip install -r requirements.txt
```
### Configure MySQL 
Make sure you have a running MySQL server.
Then create a database:
```sql
CREATE DATABASE hospital;
exit;
```
### Load .sql Onto Database
```bash
mysql -u [username] -p hospital < hospital.sql
```
### Create and Edit .env file
```bash
nano .env
```
Edit your .env file as shown below, replace DB_USER and DB_PASSWORD with your respective MySQL username and password.
```bash
DB_USER=username
DB_PASSWORD=password
DB_NAME=hospital
```
Click Ctrl-O then Enter to save and Ctrl-X to exit.
### Launch Website
```bash
venv\Scripts\activate
flask run
```
Click on link once launched: http://127.0.0.1:5000

