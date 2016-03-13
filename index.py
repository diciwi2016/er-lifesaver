#! /usr/bin/python
print "Content-type: text/html\n\n"
import requests
import json
print """

<html>
<center>
    <img src="http://www.naturallyeclectik.com/wp-content/uploads/2016/01/emergency-255x300.jpg"
</center>

<script>

    
var x=document.getElementById("demo");
window.onload = function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.watchPosition(showPosition);
    navigator.geolocation.watchPosition(showPosition2);
    }
  else{x.innerHTML="Geolocation is not supported by this browser.";}
  }
function showPosition(position)
  {
  document.getElementById("lat").value=position.coords.latitude
  }
  function showPosition2(position)
  {
  document.getElementById("long").value=position.coords.longitude
  }

</script>


<form action="current.py" method="POST">
<input  id="lat" type="text" name="lat" value="">
<input  id="long" type="text" name = "long" value="">
<input type="submit" value = "Current Location">
</form>


<BR><BR>

Or enter your location manually:
    <form action = "mapresults.py" method="get">
    Location: <input type="text" name="loc"><br>
      <input type="submit" value="Submit">
    </form>

</html>
"""
#+ "<br />Longitude: " + position.coords.longitude;  
