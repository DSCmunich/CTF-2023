<?php
$passwordHash = getenv('ADMIN_PASSWORD_HASH');
if (hash('sha256', $_COOKIE['PASSWORD']) !== $passwordHash) {
    die("Unauthorized access. Since login is not yet implemented please set the PASSWORD cookie manually!");
}

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

// Get ID parameter
if (!isset($_GET['id'])) {
    die("Invalid id!");
}
$id = (int)$_GET['id'];

// Set verified to true if it was false
$stmt = $db->prepare("UPDATE testimonials SET verified = 1 WHERE id = ? AND verified = 0");
if(!$stmt) {
    die("SQL Error: " . $db->error);
}
$stmt->bind_param("i", $id);
$stmt->execute();

// Close the database connection
$db->close();
?>

OK
