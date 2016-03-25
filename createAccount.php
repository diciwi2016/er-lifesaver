<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "hello";

$us_name = $_GET["name"];
$pw = $_GET["password"];
$email = $_GET["email"];


// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT username FROM userinfo WHERE username =" . "'" . $us_name . "'";

$result = $conn->query($sql);
if ($result->num_rows > 0) {
     echo "that username already exists, please go back and choose another one";
} else {
echo "working" . $us_name;
$sql = "INSERT INTO userinfo (username, password)
VALUES (" . "'" . $us_name . "'" . "," . "'" . $pw . "')";
}
if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}





$conn->close();

















?>


