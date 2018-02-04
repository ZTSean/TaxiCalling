from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.debug = True

## initialize database connection settings
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'taxicalling'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cur = conn.cursor()


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if request.method == "POST":
        print request.form['page']
        return redirect(url_for(request.form['page']))
    else:
        return render_template('index.html')


@app.route("/caller", methods=['GET', 'POST'])
def caller():
    if request.method == "POST":
        # write new request to the database
        name = request.form['name']
        phone = request.form['phone']

        for key, value in request.form.iteritems():
            print key, value

        '''
        cur.execute("INSERT INTO request (date, time, from_x, from_y, name, phone, destination, to_x, to_y) VALUES (" + "'")
        '''

        return render_template('caller.html')
    else:
        return render_template('caller.html')


@app.route("/driver", methods=['GET', 'POST'])
def driver():
    if request.method == "POST":
        print "post"
    else:
        return render_template('driver.html')


@app.route("/callCentre", methods=['GET', 'POST'])
def callcentre():
    if request.method == "POST":
        print "post"
    else:
        return render_template('callcentre.html')


if __name__ == "__main__":
    app.run()
