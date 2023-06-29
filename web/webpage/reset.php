<?php

$f = fopen("php://stdin", "r");
$line = fgets($f);
fclose($f);
if(!$line) {
    die("Failed reading config from stdin");
}

$config = json_decode($line, true);
if(!$config) {
    die("Failed parsing config");
}

// Create database connection
$db = new mysqli($config["DB_HOST"], $config["DB_USERNAME"], $config["DB_PASSWORD"]);
if ($db->connect_error) {
    die("Connection failed: " . $db->connect_error);
}

$queries = [
    "DROP DATABASE " . $db->real_escape_string($config["DB_NAME"]),
    "CREATE DATABASE IF NOT EXISTS " . $db->real_escape_string($config["DB_NAME"]),

    "__USE_DB__",

    "CREATE TABLE IF NOT EXISTS testimonials (
        id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(30) NOT NULL,
        message VARCHAR(255) NOT NULL,
        image VARCHAR(255) NOT NULL,
        verified BOOLEAN
    )",
    "INSERT INTO testimonials (name, message, image, verified) VALUES
        ('Anonymous', '" . $db->real_escape_string($config["FLAG_DB"]) . "', '', NULL),
        ('Susan Corto', 'Very nice webpage you created. I am very proud of you! with love - your mom', 'uploads/d3702d122441.jpg', 1),
        ('Jane', 'Hi, there!', 'uploads/af6575913b70.jpg', 1),
        ('Doe', 'Good day!', 'uploads/b35ffc9d6a08.jpg', 1)
    ",
];

foreach($queries as $query) {
    if($query === "__USE_DB__") {
        $db->select_db($config["DB_NAME"]);
    }
    else if ($db->query($query) !== TRUE) {
        die("Error running statement $query: " . $db->error);
    }
}

// Close the database connection
$db->close();


// Create & fill flag.txt
$f = fopen("/flag.txt", "w+");
fwrite($f, $config["FLAG_FILE"] . "\n");
fclose($f);


// Reset images
exec("rm -rf /var/www/html/uploads/*");
exec("cp /root/uploads-original/* /var/www/html/uploads/");
?>
