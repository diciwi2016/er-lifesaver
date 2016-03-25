
<?php
session_start();
$servername = "localhost";
$username = "root";
$dbname = "hello";
$password = "";

$us_name = $_GET["name"];
$pw = $_GET["password"];

echo $us_name . " ";
echo $pw . " ";
$doesexist = "yes";
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT password FROM userinfo WHERE username =" . "'" . $us_name . "'";

$result = $conn->query($sql);
if ($result->num_rows > 0) {
     // output data of each row
     while($row = $result->fetch_assoc()) {
		 if ($row["password"] === $pw) {
			 echo "login successful";
			 $_SESSION["username"] = $us_name; 
			 echo $_SESSION["username"];
		 }
		 else {
         echo "login failed";
		 }
     }
} else {
     echo "login failed";
	 $doesexist = "no";
}



$conn->close();

?>