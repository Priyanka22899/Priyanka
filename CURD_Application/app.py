from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'employee_db'
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employee")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employee=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        address = request.form["address"]
        date = request.form["date"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee(Name,Gender,Address,JoinDate) VALUES(%s,%s,%s,%s)",
                    (name, gender, address, date))
        mysql.connection.commit()
        return redirect(url_for("index"))


@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        address = request.form['address']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE employee SET Name=%s,Gender=%s,Address=%s,JOINT Date=%s WHERE id=%s""",
                    (name, gender, address, date))
        mysql.connection.commit()
        return redirect(url_for("index"))


@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", (id_data))
    mysql.connection.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug="true")
