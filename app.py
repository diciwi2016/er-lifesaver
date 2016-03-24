from flask import Flask, render_template, request, session, redirect, url_for
import urllib2
import json
import userdb            # add / update user account methods
from data import hd # hospital data gathered from some site

app = Flask(__name__)
key = "AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA"


@app.route('/')
def root():
    return render_template("index.html", title='Main')

# V link to show nearby hospitals + waiting time if available


@app.route('/current', methods=["GET", "POST"])
def current():
    if request.method == "POST":

        # takes the latitude and longitude of user's current location
        lat = request.form['lat']
        lon = request.form['lon']

        url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + \
            str(lat) + "," + str(lon) + "&sensor=true"  # + "&key=" + key
        retS = hospitalsNearLocation(lat + "," + lon, url)

    return retS

# origin is the formatted POST for the origin in directions api
# url is the url for the gmaps api
# returns the formatted thing the whole thing

# hospital_dict:
# (total time, name, address, travel time, wait time, directions, link)
def hospitalsNearLocation(origin, url):
    hospital_data = []
    url = urllib2.urlopen(url)
    f = url.read()
    f = json.loads(f)

    # finds closest address location based on user lat and long
    res = f['results']
    loc = res[0]["formatted_address"]
    loc = loc.replace(" ", '+')

    # find nearest hospitals
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=emergency+room+hospital" + \
        "+near+" + loc + "&key=AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA"

    url = urllib2.urlopen(url)
    f = url.read()
    f = json.loads(f)

    res = f['results']

    x = 0
    retS = "<table border = '1'>"
    # url for directions api
    direction_api = "https://maps.googleapis.com/maps/api/directions/json?mode=driving&key=" + key
    for i in res:
        dirURL = direction_api + "&origin=" + origin + \
            "&destination=" + i['formatted_address']
        dirURL = dirURL.replace(" ", "%20")
        dirJson = json.loads(urllib2.urlopen(dirURL).read())
        legs = dirJson['routes'][0]['legs'][0]
        travel_time = legs['duration']['text']
        name = i['name']
        address = i['formatted_address']
        maps_link = "https://www.google.com/maps/place/" + \
                i['formatted_address']
                
        steps = legs['steps']
        directions = []
        for step in steps:
            directions.append(step['html_instructions'].replace("</div>", "").replace("<div style=\"font-size:0.9em\">", "<br>"))
            #print step['html_instructions']

        # tmp for waiting time
        wait_time = 0
        waitingTimeAvailable = False #var to determine if waiting time is in data
        
        for a in hd:
            if a[:a.find('hospital') - 1] in i['name'].lower():
                wait_time = int(hd[a])
                break

        # waiting time + travel time
        total_time = int(travel_time[:travel_time.find(" ")]) + wait_time 

        hospital_data.append((total_time, name, address, travel_time, \
                              wait_time, directions, maps_link))
        def sortBy(x): return x[0]
    sorted_data = sorted(hospital_data, key=sortBy)
    return render_template("current.html", hospital_data=sorted_data)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        pas = request.form["password"]
        pas2 = request.form["password2"]
        if pas == pas2:
            userdb.add(user, pas)
        else:
            return "Passwords don't match"
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'logged_in' in session and session['logged_in']:
            return render_template("success.html")
        else:
            return render_template("login.html")
    else:
        assert(request.method == "POST")
        if userdb.verify(request.form['username_in'],
                         request.form['password_in']):
            session['logged_in'] = True
            session['username_hash'] = request.form['username_in']
            session['password_hash'] = request.form['password_in']
            return redirect("success")
        else:
            session['logged_in'] = False
            return render_template("login.html")


@app.route("/logout")
@app.route("/logout/")
def logout():
    session['logged_in'] = False
    return redirect(url_for("login"))


@app.route("/success")
def success():
    return render_template("success.html", title="LoggedIn")


@app.route("/update", methods=["GET", "POST"])
def update():                
    if request.method == "POST":
        fName = request.form["fName"]
        lName = request.form["lName"]
        dob = request.form["dob"]
        state = request.form["state"]
        loc = request.form["loc"]
        newInfo = userdb.update(session['username_hash'], session['password_hash'], fName, lName, dob, state, loc)
        return render_template("success.html", L=newInfo)
    else:
        return render_template("update.html")


@app.route("/send")
def send():
    return render_template("send.html")


if __name__ == '__main__':
    app.secret_key = 'dcb61f28eafb8771213f3e0612422b8d'
    app.run(debug=True)

app.run('0.0.0.0', port=8000)
