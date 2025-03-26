var mysql = require('mysql');

var con = mysql.createConnection({
host: "localhost",
user: "root",
password: "password2357!",
database: "Hospital"
});

con.connect(function(err) {
    if (err) throw err;
    con.query("SELECT * FROM Patients", function (err, result, fields) {
if (err) throw err;
console.log(result);
});
});