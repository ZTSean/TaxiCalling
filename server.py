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

        for key, value in request.form.iteritems():
            print key, len(value)

        # validate each fields in the request form
        # fields in request: name , to_x , to_y, from_y , from_x, phone, time, date, destination
        name = "anonymous" if len(request.form['name']) == 0 else request.form['name']
        phone = "1111" if len(request.form['phone']) == 0 else request.form['phone']
        to_x = "1111" if len(request.form['to_x']) == 0 else request.form['to_x']
        to_y = "1111" if len(request.form['to_y']) == 0 else request.form['to_y']
        from_y = "1111" if len(request.form['from_y']) == 0 else request.form['from_y']
        from_x = "1111" if len(request.form['from_x']) == 0 else request.form['from_x']
        time = "1111" if len(request.form['time']) == 0 else request.form['time']
        date = "1111" if len(request.form['date']) == 0 else request.form['date']
        destination = "1111" if len(request.form['destination']) == 0 else request.form['destination']

        '''
        cur.execute("SELECT id FROM request ORDER BY id DESC");
        row = cur.fetchone()
        id = 0
        if row is not None:
            id = 
        else:
            print "no data inside"
        '''

        # write new request to the database
        sql = "INSERT INTO request (date, time, from_x, from_y, name, phone, destination, to_x, to_y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (date, time, from_x, from_y, name, phone, destination, to_x, to_y))

        conn.commit()

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
