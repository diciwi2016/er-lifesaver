from flask import Flask, render_template, request, session, redirect, url_for
from random import randint, choice
import urllib2, json, requests, userdb
from data import hd

app = Flask(__name__)
key="AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA"

@app.route('/')
def root():
    return render_template("index.html", title = 'Main')

@app.route('/current', methods = ["GET", "POST"])
def current():
    if request.method == "POST":
        lat = request.form['lat']
        lon = request.form['lon']
        url="http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat)+"," + str(lon) + "&sensor=true"# + "&key=" + key
        url=urllib2.urlopen(url)
        f=url.read();
        f = json.loads(f)

        res= f['results']
        loc= res[0]["formatted_address"]
        loc=loc.replace(" ", '+')

        url="https://maps.googleapis.com/maps/api/place/textsearch/json?query=emergency+room+hospital" + "+near+" + loc + "&key=AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA" 

        url=urllib2.urlopen(url)
        f=url.read()
        f = json.loads(f)

        res= f['results']

        x=0
        retS=""
        for i in res:
             retS+= i['name'] + "<br>"+ i['formatted_address']
             for a in hd:
                 if a[:a.find('hospital')-1] in i['name'].lower():
                     retS+= "<BR>Waiting Time: "+ hd[a] + " minutes"
             retS+= "<BR><BR><BR>"#, '<img src="', i['icon'], '>"<br><br><br>'
             x+=1
             if x== 10:
                break
        
    return render_template("current.html",  s=retS)

@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    else:
        assert(request.method == "POST")
        if userdb.verify(request.form['username_in'], request.form['password_in']):
            session['logged_in'] = True
            session['username_hash'] = userdb.username_hash(request.form['username_in'])
            session['password_hash'] = userdb.password_hash( request.form['password_in'])
            return redirect(url_for("home"))
        else:
            session['logged_in'] = False
            return render_template("login.html", ERROR="User not recognized.")


@app.route("/logout")
@app.route("/logout/")
def logout():
    session['logged_in'] = False
    return redirect(url_for("login"))

if __name__=='__main__':
    app.run(debug=True)

app.run('0.0.0.0', port = 8000)
