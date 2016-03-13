#! /usr/bin/python
print "Content-type: text/html\n\n"
import urllib2
import cgi
import cgitb
import json
from data import hd
cgitb.enable()
form=cgi.FieldStorage()
keys=form.keys()

loc=""

if "loc" in keys:
    loc = form['loc'].value
    loc=loc.replace(" ", '+')

key="AIzaSyDm8rcyz9i4d8p2QvmCAumvNTM1V9CfmDA"
url="https://maps.googleapis.com/maps/api/place/textsearch/json?query=emergency+room" + "+near+" + loc + "&key=" + key

url=urllib2.urlopen(url)
f=url.read()
f = json.loads(f)

res= f['results']
x=0
for i in res:
     print i['name'], "<br>", i['formatted_address']
     for a in hd:
         if a[:a.find('hospital')-1] in i['name'].lower():
             print "<BR>Waiting Time: ", hd[a], " minutes"
     print "<BR><BR><BR>"#, '<img src="', i['icon'], '>"<br><br><br>'
     x+=1
     if x== 10:
        break
