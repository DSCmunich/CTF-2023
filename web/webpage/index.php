<?php
// Check for the TOKEN cookie
$passwordHash = getenv('ADMIN_PASSWORD_HASH');
$isAdmin = false;
if (hash('sha256', $_COOKIE['PASSWORD']) === $passwordHash) {
	$isAdmin = true;
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

// Fetch all records from the table
$sql = "SELECT * FROM testimonials";
$result = $db->query($sql);
?>

<!DOCTYPE HTML>
<!--
	Read Only by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Willis Corto Personal Webpage</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
	</head>
	<body class="is-preload">

		<!-- Header -->
			<section id="header">
				<header>
					<span class="image avatar"><img src="images/avatar.jpg" alt="" /></span>
					<h1 id="logo"><a href="#">Willis Corto</a></h1>
					<p>I learned from a rogue AI<br />
					and now I'm totally crazy</p>
				</header>
				<nav id="nav">
					<ul>
						<li><a href="#one" class="active">About</a></li>
						<li><a href="#two">Things I Can Do</a></li>
						<li><a href="#three">Testimonials</a></li>
						<li><a href="#four">Submit a Testimonial</a></li>
					</ul>
				</nav>
			</section>

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Main -->
					<div id="main">

						<!-- One -->
							<section id="one">
								<div class="image main" data-position="center">
									<img src="images/banner.jpg" alt="" />
								</div>
								<div class="container">
									<header class="major">
										<h2>Willis Corto Webpage</h2>
										<p>Embracing the intricate dance between technology and imagination. Come join me as we explore the limitless possibilities of the digital world together.</p>
									</header>
									<p>Hello! I'm Willis, a recent coding enthusiast and budding artificial intelligence aficionado. I'm thrilled that you've stumbled upon my little corner of the internet. This website, which I've proudly built from scratch, is the product of my newfound love for programming and an insatiable curiosity for the world of AI.</p>
								</div>
							</section>

						<!-- Two -->
							<section id="two">
								<div class="container">
									<h3>Things I Can Do</h3>
									<ul class="feature-icons">
										<li class="icon solid fa-code">Write all the code</li>
										<li class="icon solid fa-cubes">Stack small boxes</li>
										<li class="icon solid fa-book">Read books and stuff</li>
										<li class="icon solid fa-coffee">Drink much coffee</li>
										<li class="icon solid fa-bolt">Lightning bolt</li>
										<li class="icon solid fa-users">Shadow clone technique</li>
									</ul>
								</div>
							</section>

						<!-- Three -->
							<section id="three">
								<div class="container">
									<h3>Testimonials</h3>
									<p>These are the things people say about me!</p>
									<div class="features">
										<?php
											while ($row = $result->fetch_assoc()) {
												if($row["verified"] !== "1" && $row["verified"] !== "0") {
													continue;
												}
												if($row["verified"] !== "1" && !$isAdmin) {
													continue;
												}

												?>
													<article>
														<a href="#" class="image"><img src="<?= $row["image"] ?>" /></a>
														<div class="inner">
															<h4><?php
																echo $row["name"];
																if(!$row["verified"]) {
																	echo "&nbsp;&nbsp;&nbsp;<span style=\"color: red;\">Unverified!</span>";
																	echo "&nbsp<a href=\"/php/verify-testimonial.php?id=" . $row['id'] . "\">Verify</a>";
																}
															?></h4>
															<p><?= $row["message"] ?></p>
														</div>
													</article>
												<?php
											}
										?>
									</div>
								</div>
							</section>

						<!-- Four -->
							<section id="four">
								<div class="container">
									<h3>Submit a Testimonial</h3>
									<p>Feel free to leave a message, about wether or not you like my new website!</p>
									<form method="post" enctype="multipart/form-data" action="/php/submit-testimonial.php">
										<div class="row gtr-uniform">
											<div class="col-6 col-12"><input type="text" name="name" id="name" placeholder="Your Name" /></div>
											<div class="col-6 col-12">Your Avatar:&nbsp;&nbsp;&nbsp;<input type="file" name="image" id="image" /></div>
											<div class="col-12"><textarea name="message" id="message" placeholder="Your Message" rows="6"></textarea></div>
											<div class="col-12">
												<ul class="actions">
													<li><input type="submit" class="primary" value="Submit" /></li>
													<li><input type="reset" value="Reset Form" /></li>
												</ul>
											</div>
										</div>
									</form>
								</div>
							</section>
					</div>

				<!-- Footer -->
					<section id="footer">
						<div class="container">
							<ul class="copyright">
								<li>&copy; Willis Corto. All rights reserved.</li><li>Design: <a href="http://html5up.net">HTML5 UP</a></li>
							</ul>
						</div>
					</section>

			</div>

		<!-- Scripts from Template -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
	</body>
</html>