from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
app.debug = True

# initialize database connection settings
mysql = MySQL()


# local mysql db settings
'''
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'taxicalling'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
'''

# remote cleardb settings
app.config['MYSQL_DATABASE_USER'] = 'b734081a447cd9'
app.config['MYSQL_DATABASE_PASSWORD'] = '8a9cc8b7'
app.config['MYSQL_DATABASE_DB'] = 'heroku_b595805c66ef772'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'

mysql.init_app(app)

conn = mysql.connect()
cur = conn.cursor()
bcrypt = Bcrypt(app)


# Insert fake data into database
# sql = "INSERT INTO driver (id, date, time, location_lat, location_lng, name, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
# fake data 1: '1', '2018-02-04', '08:41:09', '22.2793113', '114.13650370000005', 'anonymous', '1'
#  -> INSERT INTO driver (id, date, time, location_lat, location_lng, name, status) VALUES ('1', '2018-02-04', '08:41:09', '22.2793113', '114.13650370000005', 'anonymous', '1');
# fake data 2: '2', '2018-02-04', '08:41:09', '22.2813071', '114.15267180000001', 'anonymous', '1'
#  -> INSERT INTO driver (id, date, time, location_lat, location_lng, name, status) VALUES ('2', '2018-02-04', '08:41:09', '22.2813071', '114.15267180000001', 'anonymous', '1');
# fake data 3: '3', '2018-02-04', '08:41:09', '22.2900175', '114.14439979999997', 'anonymous', '1'
#  -> INSERT INTO driver (id, date, time, location_lat, location_lng, name, status) VALUES ('3', '2018-02-04', '08:41:09', '22.2900175', '114.14439979999997', 'anonymous', '2');


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if request.method == "POST":
        code = bcrypt.generate_password_hash(request.form['code'])

        if bcrypt.check_password_hash(code, 'driver1'):
            print "Driver 1 requested"
            return redirect(url_for("driver", driverid=1))
        elif bcrypt.check_password_hash(code, 'driver2'):
            print "Driver 2 requested"
            return redirect(url_for("driver", driverid=2))
        elif bcrypt.check_password_hash(code, 'driver3'):
            print "Driver 3 requested"
            return redirect(url_for("driver", driverid=3))
        elif bcrypt.check_password_hash(code, 'customer'):
            print "Customer requested"
            return redirect(url_for("caller"))
        elif bcrypt.check_password_hash(code, 'callcentre'):
            print "Centre requested"
            return redirect(url_for("callcentre"))

        
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route("/caller", methods=['GET', 'POST'])
def caller():
    if request.method == "POST":

        for key, value in request.form.iteritems():
            print key, value, len(value)

        # validate each fields in the request form
        # fields in request: name , to_lat , to_lng, from_lng , from_lat, phone, time, date, destination
        name = "anonymous" if request.form.get('name', None) == None or len(request.form.get('name')) == 0 else request.form['name']
        phone = "1111" if request.form.get('phone', None) == None else request.form['phone']
        to_lat = "22" if request.form.get('to_lat', None) == None else round(float(request.form['to_lat']), 8)
        to_lng = "143" if request.form.get('to_lng', None) == None else round(float(request.form['to_lng']), 9)
        from_lng = "143" if request.form.get('from_lng', None) == None else round(float(request.form['from_lng']), 9)
        from_lat = "22" if request.form.get('from_lat', None) == None else round(float(request.form['from_lat']), 8)
        time = "00:00:00" if request.form.get('time', None) == None else request.form['time']
        date = "2018-02-05" if request.form.get('date', None) == None else request.form['date']
        destination = "1111" if request.form.get('destination', None) == None else request.form['destination']

        print ""
        print from_lat, from_lng, to_lat, to_lng
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
        sql = "INSERT INTO request " \
              "(date, time, from_lat, from_lng, name, phone, destination, to_lat, to_lng) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (date, time, from_lat, from_lng, name, phone, destination, to_lat, to_lng))

        conn.commit()

        return render_template('caller.html')
    else:
        return render_template('caller.html')


@app.route("/driver", methods=['GET', 'POST'])
def driver():
    if request.method == "POST":
        print "post"
    else:
        return render_template('driver.html', driverid=request.args.get('driverid'))


@app.route("/callcentre", methods=['GET', 'POST'])
def callcentre():
    if request.method == "POST":
        print "post"
    else:
        # retrieve all driver data from driver table
        cur.execute("SELECT * FROM driver;")  # Get address details by ID

        driverdata = []
        callerdata = []
        for row in cur:
            formattedRow = {}
            # (1, datetime.date(2018, 2, 4), datetime.timedelta(0, 31269), Decimal( &  # 39;22.27931130&#39;), Decimal(&#39;114.13650370&#39;), u&#39;anonymous&#39;, 1)
            formattedRow['id'] = row[0]
            formattedRow['date'] = str(row[1])
            formattedRow['time'] = str(row[2])
            formattedRow['location_lat'] = float(row[3])
            formattedRow['location_lng'] = float(row[4])
            formattedRow['name'] = row[5]
            formattedRow['status'] = row[6]

            driverdata.append(formattedRow)

        # retrieve most recent caller data from request table
        cur.execute("SELECT * FROM request ORDER BY id DESC;")
        row = cur.fetchone()

        callerdata = []
        if (row != None):
            formattedRow = {}
            # (date, time, from_lat, from_lng, name, phone, destination, to_lat, to_lng)
            formattedRow['id'] = row[0]
            formattedRow['date'] = str(row[1])
            formattedRow['time'] = str(row[2])
            formattedRow['from_lat'] = float(row[3])
            formattedRow['from_lng'] = float(row[4])
            formattedRow['name'] = row[5]
            formattedRow['phone'] = row[6]
            formattedRow['destination'] = row[7]
            formattedRow['to_lat'] = float(row[8])
            formattedRow['to_lng'] = float(row[9])
            callerdata.append(formattedRow)

        return render_template('callcentre.html', driverdata=json.dumps(driverdata), callerdata=json.dumps(callerdata))


if __name__ == "__main__":
    app.run()
