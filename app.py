from flask import Flask, render_template, request, session, redirect, url_for
import urllib2, json, userdb
from data import hd

app = Flask(__name__)
key="AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA"

@app.route('/')
def root():
    return render_template("index.html", title = 'Main')

##V link to show nearby hospitals + waiting time if available

@app.route('/current', methods = ["GET", "POST"])
def current():
    if request.method == "POST":
        
        #takes the latitude and longitude of user's current location
        lat = request.form['lat']
        lon = request.form['lon']
        url="http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat)+"," + str(lon) + "&sensor=true"# + "&key=" + key
        url=urllib2.urlopen(url)
        f=url.read();
        f = json.loads(f)
        
        #finds closest address location based on user lat and long 
        res= f['results']
        loc= res[0]["formatted_address"]
        loc=loc.replace(" ", '+')
        
        #find nearest hospitals
        url="https://maps.googleapis.com/maps/api/place/textsearch/json?query=emergency+room+hospital" + "+near+" + loc + "&key=AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA" 

        url=urllib2.urlopen(url)
        f=url.read()
        f = json.loads(f)

        res= f['results']

        x=0
        retS="<table border = '1'>"
        for i in res:
             retS+= "<tr><td><b>" + i['name'] + "</b><br>"+ i['formatted_address'] 
             
             for a in hd:
                 if a[:a.find('hospital')-1] in i['name'].lower():
                     retS+= "</td><td>Waiting Time: "+ hd[a] + " minutes" 
             retS+= "<BR><BR></td></tr>"#, '<img src="', i['icon'], '>"<br><br><br>'
             x+=1
             if x== 10:
                break
        
    return render_template("current.html",  s=retS)

@app.route("/signup", methods = ["GET", "POST"])
def signup():
           if request.method=="POST":
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
            return "Logged in!!"
        else:
            return render_template("login.html")
    else:
        assert(request.method == "POST")
        if userdb.verify(request.form['username_in'], request.form['password_in']):
            session['logged_in'] = True
            session['username_hash'] = request.form['username_in']
            session['password_hash'] = request.form['password_in']
            return redirect("Success")
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

if __name__=='__main__':
    app.secret_key = 'dcb61f28eafb8771213f3e0612422b8d'
    app.run(debug=True)

app.run('0.0.0.0', port = 8000)
