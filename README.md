# Hospital Management System Database
## Instructions
### Clone the Repository
```bash
git clone https://github.com/ryan-webster-vt/Hospital-Database.git
cd Hospital-Database
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
Login
```bash
mysql -u root -p
```
You will be prompted to insert your MySQL password.
Then create a database:
```sql
CREATE DATABASE hospital;
exit;
```
### Load .sql Onto Database
If you're using a different MySQL username, replace root
```bash
mysql -u root -p hospital < hospital.sql
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
source venv/bin/activate # On Windows: venv\Scripts\activate
flask run
```
Click on link once launched: http://127.0.0.1:5000

