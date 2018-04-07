from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
from flask_sslify import SSLify
import json
import math
import requests
from wtforms import Form, StringField, validators

class CallTaxiForm(Form):
    name = StringField('name')
    phone = StringField('phone')
    date = StringField('date', [validators.DataRequired()])
    time = StringField('time', [validators.DataRequired()])
    from_lat = StringField('from_lat', [validators.DataRequired()])
    from_lng = StringField('from_lng', [validators.DataRequired()])
    to_lat = StringField('to_lat', [validators.DataRequired()])
    to_lng = StringField('to_lng', [validators.DataRequired()])
    destination = StringField('destination', [validators.DataRequired()])

class DriverLocationForm(Form):
    driverid = StringField('driverid', [validators.DataRequired()])
    date = StringField('date', [validators.DataRequired()])
    time = StringField('time', [validators.DataRequired()])
    location_lat = StringField('location_lat', [validators.DataRequired()])
    location_lng = StringField('location_lng', [validators.DataRequired()])
    name = StringField('name')
    status = StringField('status') # updated by the server

app = Flask(__name__)
sslify = SSLify(app)
app.debug = False

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

assignedDriver = -1
driver1status = 1
driver2status = 1
driver3status = 1

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
        print "POST to main page"
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
        elif bcrypt.check_password_hash(code, 'caller'):
            print "Customer requested"
            return redirect(url_for("caller", requesttype=1))
        elif bcrypt.check_password_hash(code, 'callcentre'):
            print "Centre requested"
            return redirect(url_for("callcentre"))

        return render_template('index.html')
    else:
        print "GET to main page"
        return render_template('index.html')


@app.route("/caller", methods=['GET', 'POST'])
def caller():
    if request.method == "POST":



        return render_template('caller.html')
    else:
        return render_template('index.html')


@app.route("/calltaxi", methods=['POST'])
def calltaxi():
    global assignedDriver
    ## call a taxi
    print "========================================================"
    print "================ Process taxi request =================="
    print "--------------------------------------------------------"
    print "---------------- Request params ------------------------"
    for key, value in request.form.iteritems():
        print key, value, len(value)
    print "--------------------------------------------------------"

    form = CallTaxiForm(request.form)
    if form.validate():
                # validate each fields in the request form
        # fields in request: name , to_lat , to_lng, from_lng , from_lat, phone, time, date, destination
        name = "anonymous" if request.form.get('name', None) == None or len(request.form.get('name')) == 0 else \
            request.form['name']
        phone = "1111" if request.form.get('phone', None) == None else request.form['phone']
        to_lat = "22.0" if request.form.get('to_lat', None) == None or len(request.form.get('to_lat')) == 0 else str(
            round(float(request.form['to_lat']), 8))
        to_lng = "143.0" if request.form.get('to_lng', None) == None or len(request.form.get('to_lng')) == 0 else str(
            round(float(request.form['to_lng']), 9))
        from_lat = "22.0" if request.form.get('from_lat', None) == None or len(
            request.form.get('from_lat')) == 0 else str(
            round(float(request.form['from_lat']), 8))
        from_lng = "143.0" if request.form.get('from_lng', None) == None or len(
            request.form.get('from_lng')) == 0 else str(
            round(float(request.form['from_lng']), 9))
        time = "00:00:00" if request.form.get('time', None) == None else request.form['time']
        date = "2018-02-05" if request.form.get('date', None) == None else request.form['date']
        destination = "1111" if request.form.get('destination', None) == None else request.form['destination']

        print ""
        print "Start: %s, %s" % (from_lat, from_lng)
        print "Destination: %s, %s" % (to_lat, to_lng)
        '''
        cur.execute("SELECT id FROM request ORDER BY id DESC");
        row = cur.fetchone()
        id = 0
        if row is not None:
            id = 
        else:
            print "no data inside"
        '''

        ### test use from_lat, from_lng
        from_lat = 33.8179361
        from_lng = -84.45219920000001

        # pull all driver information from database ========================================
        conn = mysql.connect()
        cur = conn.cursor()
        # availableDriverSQL = 'SELECT * FROM driver WHERE status = 1 SELECT * FROM'
        availableDriverSQL = """(SELECT * FROM driver
                    WHERE status = 1 AND driverid = 1
                    ORDER BY date DESC, time DESC
                    LIMIT 1)

                    UNION

                    (SELECT * FROM driver
                    WHERE status = 1 AND driverid = 2
                    ORDER BY date DESC, time DESC
                    LIMIT 1)

                    UNION 
                    (SELECT * FROM driver
                    WHERE status = 1 AND driverid = 3
                    ORDER BY date DESC, time DESC
                    LIMIT 1)"""
        cur.execute(availableDriverSQL)  # Get address details by ID

        driver_location_row = ""
        availableDrivers = []
        for row in cur:
            # (1, datetime.date(2018, 2, 4), datetime.timedelta(0, 31269), Decimal( &  # 39;22.27931130&#39;), Decimal(&#39;114.13650370&#39;), u&#39;anonymous&#39;, 1)
            driver_location_row += ("%s,%s|" % (row[4], row[5]))
            availableDrivers.append(int(row[1]))

        driver_location_row = driver_location_row.rstrip('|')
        print "All current available driver location:" + driver_location_row

        # send request to google map server to get the time cost to the customer
        maps_key = 'AIzaSyDZ2cAeiEseW9hyqSjuJnsgbKS5DLVPvOs'
        distance_matrix_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'

        params = {
            'origins': driver_location_row,
            'destinations': "%s,%s" % (from_lat, from_lng),
            'key': maps_key
        }

        req = requests.get(distance_matrix_url, params=params);
        res = req.json()

        # print response
        for key, value in res.iteritems():
            print key, value

        # ----------- Process result & find closest driver -----------
        minTime = 10000000
        for i in range(len(res['rows'])):
            availableDriver = res['rows'][i]
            tmp = int(availableDriver['elements'][0]['duration']['value'])
            if tmp < minTime:
                minTime = tmp
                assignedDriver = availableDrivers[i]

        print "Assigned Driver: " + str(assignedDriver)

        '''
        # write new request to the database =================================================
        sql = "INSERT INTO request " \
              "(date, time, from_lat, from_lng, name, phone, destination, to_lat, to_lng) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"'''
        # cur.execute(sql, (date, time, from_lat, from_lng, name, phone, destination, to_lat, to_lng))

        # conn.commit()
        cur.close()
        conn.close()
        print "========================================================"

        return json.dumps(res)

    else:
        res = form.errors
        res['status'] = "INVALID_REQUEST"
        return json.dumps(res)


@app.route("/driver", methods=['GET', 'POST'])
def driver():
    if request.method == "POST":
        print "--------------"

        id = request.args.get('driverid')
        conn = mysql.connect()
        cur = conn.cursor()

        if id == None:
            # id not shown: invalid request

            return render_template('index.html')
        else:
            # check if there are previous info could be used
            '''
            conn = mysql.connect()
            cur = conn.cursor()
            driver_info_sql = "SELECT * FROM driver WHERE id = %s;"
            print driver_info_sql
            cur.execute(driver_info_sql, (id,))

            row = cur.fetchone()
            cur.close()
            conn.close()
            '''

            print "[Initial Request]: no need to update"


        return render_template('driver.html', driverid=id)

    else:
        return render_template('index.html')

@app.route("/update_driver_location", methods=['POST'])
def update_driver_location():
    global assignedDriver, driver1status, driver2status, driver3status
    form = DriverLocationForm(request.form)
    if form.validate():
        id = int(request.form.get('driverid'))
        print "================ Update Request from driver " + str(id) + " ================"
        # update driver location & change status
        # fields in request: name , to_lat , to_lng, from_lng , from_lat, phone, time, date, destination
        name = "anonymous" if request.form.get('name', None) == None or len(request.form.get('name')) == 0 else \
        request.form['name']
        location_lat = "22.0" if request.form.get('location_lat', None) == None or len(
            request.form.get('location_lat')) == 0 else str(round(float(request.form['location_lat']), 8))
        location_lng = "143.0" if request.form.get('location_lng', None) == None or len(
            request.form.get('location_lng')) == 0 else str(round(float(request.form['location_lng']), 9))
        time = "00:00:00" if request.form.get('time', None) == None else request.form['time']
        date = "2018-02-05" if request.form.get('date', None) == None else request.form['date']

        print "Current Assigned driver: " + str(assignedDriver)

        if assignedDriver != -1 and id == assignedDriver:
            print "Driver " + str(id) + " has been assigned customer..."
            conn = mysql.connect()
            cur = conn.cursor()
            # driver has been assigned to a customer

            if id == 1:
                driver1status = 2
            elif id == 2:
                driver2status = 2
            elif id == 3:
                driver3status = 2

            status = 2  # on-call
            sql = "INSERT INTO driver (driverid, date, time, location_lat, location_lng, name, status) VALUES (%s, %s, %s, %s, %s, %s, %s) "


            assignedDriver = -1

            cur.execute(sql, (id, date, time, location_lat, location_lng, name, status))
            conn.commit()

            cur.close()
            conn.close()

            print "Success assigned driver " + str(id) + " for on-call..."

            # return status for update
            # update == 2, need update in UI
            return json.dumps({"status": "OK", "update": 2, "driver_status": 2})
        else:
            print "Driver " + str(id) + " not being assigned..."
            # driver not being assigned a new customer
            conn = mysql.connect()
            cur = conn.cursor()
            # driver has been assigned to a customer

            status = 1 if request.form.get('status', None) == None else request.form['status']
            sql = "INSERT INTO driver (driverid, date, time, location_lat, location_lng, name, status) VALUES (%s, %s, %s, %s, %s, %s, %s) "

            cur.execute(sql, (id, date, time, location_lat, location_lng, name, status))
            conn.commit()

            cur.close()
            conn.close()

            # update == 1: no need to update in UI
            return json.dumps({"status": "OK", "update": 1})
    else:
        # the input form is not valid
        res = form.errors
        res['status'] = "INVALID_REQUEST"
        return json.dumps(res)

@app.route("/pickup", methods=["POST"])
def pickup ():
    global driver1status, driver2status, driver3status
    print "========================================================"
    print "=============== Process pick up request ================"
    print "--------------------------------------------------------"
    print "---------------- Request params ------------------------"
    # check whether the driver is on call
    id = int(request.get('driverid'))

    if id == 1 and driver1status == 2:
        print "Success assigned driver 1 for hired..."
        driver1status = 3 # set driver to available
        return json.dumps({"status": "OK"})
    elif id == 2 and driver2status == 2:
        print "Success assigned driver 2 for hired..."
        driver2status = 3
        return json.dumps({"status": "OK"})
    elif id == 3 and driver3status == 2:
        print "Success assigned driver 3 for hired..."
        driver3status = 3

        return json.dumps({ "status" : "OK" })
    # else return error
    else:
        return json.dumps({"status": "INVALID_REQUEST", "error": "You are not on-call..."})
    print "========================================================"


@app.route("/endtrip", methods=["POST"])
def end_trip ():
    global driver1status, driver2status, driver3status
    print "========================================================"
    print "=============== Process end trip request ================"
    print "--------------------------------------------------------"
    print "---------------- Request params ------------------------"

    # check whether the driver is hired
    id = int(request.get('driverid'))
    if id == 1 and driver1status == 3:
        driver1status = 1 # set driver to available
        print "Success assigned driver 1 for end trip..."
        return json.dumps({"status": "OK"})
    elif id == 2 and driver2status == 3:
        print "Success assigned driver 2 for end trip..."
        driver2status = 1
        return json.dumps({"status": "OK"})
    elif id == 3 and driver3status == 3:
        print "Success assigned driver 3 for end trip..."
        driver3status = 1

        return json.dumps({ "status" : "OK" })
    # else return error
    else:
        return json.dumps({"status": "INVALID_REQUEST", "error": "You are not hired..."})
    print "========================================================"


@app.route("/callcentre", methods=['GET', 'POST'])
def callcentre():
    if request.method == "POST":
        print "post"
    else:
        # retrieve all driver data from driver table
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM driver;")  # Get address details by ID

        driverdata = []
        callerdata = []
        for row in cur:
            formattedRow = {}
            # (1, datetime.date(2018, 2, 4), datetime.timedelta(0, 31269), Decimal( &  # 39;22.27931130&#39;), Decimal(&#39;114.13650370&#39;), u&#39;anonymous&#39;, 1)
            formattedRow['driverid'] = row[1]
            formattedRow['date'] = str(row[2])
            formattedRow['time'] = str(row[3])
            formattedRow['location_lat'] = float(row[4])
            formattedRow['location_lng'] = float(row[5])
            formattedRow['name'] = row[6]
            formattedRow['status'] = row[7]

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

        cur.close()
        conn.close()
        return render_template('callcentre.html', driverdata=json.dumps(driverdata), callerdata=json.dumps(callerdata))


if __name__ == "__main__":
    app.run()
