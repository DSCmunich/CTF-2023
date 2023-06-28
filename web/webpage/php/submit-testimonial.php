<?php
// Database configuration
$dbHost     = getenv('DB_HOST');
$dbUsername = getenv('DB_USERNAME');
$dbPassword = getenv('DB_PASSWORD');
$dbName     = getenv('DB_NAME');

// Create database connection
$db = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);
if ($db->connect_error) {
    die("Connection failed: " . $db->connect_error);
}

// Get data from POST request
$name = $_REQUEST['name'];
$image = $_FILES['image']['tmp_name'];
$message = $_REQUEST['message'];

// Save image to disk
$img_path = "/uploads/" . basename($_FILES['image']['name']);
if (!move_uploaded_file($image, ".." . $img_path)) {
    die("Sorry, there was an error uploading your image.");
}

// Insert name and message into the database
$sql = "INSERT INTO testimonials (name, message, image, verified) VALUES ('$name', '$message', '$img_path', 0)";
if ($db->query($sql) !== TRUE) {
    die("Error: " . $sql . "<br>" . $db->error);
}

// Close the database connection
$db->close();
?>

Your testimonial has been submitted for review!
