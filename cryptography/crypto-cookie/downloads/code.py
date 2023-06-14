import base64
import json
import random
import os

import flask
from cryptography.hazmat.primitives import padding, ciphers
from cryptography.hazmat.primitives.ciphers import modes, algorithms

cookie_KEY = os.urandom(32)
ALGO = algorithms.AES(cookie_KEY)
BLOCK_SIZE = ALGO.block_size // 8

app = flask.Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Secret Website</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">
  </head>
  <body class="dark-mode">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="/">Secret Website</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/privacy">Privacy</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      %s
    </div>
  </body>
</html>
"""

WELCOME_PAGE = (
    TEMPLATE
    % """
    <h1 class="display-4 text-center mb-4">Welcome to Secret Website</h1>
    <p class="lead text-center">Only the chosen ones can enter...</p>
    <div class="row justify-content-center">
      <div class="col-lg-4">
        <form method="post" action="/register">
          <div class="mb-3">
            <label for="username" class="form-label">Username:</label>
            <input type="text" class="form-control" id="username" placeholder="Enter your username" name="username" minlength="2" required>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">E-mail:</label>
            <input type="email" class="form-control" id="email" placeholder="Enter your e-mail" name="email" minlength="2" required>
          </div>
          <button type="submit" class="btn btn-primary">Register</button>
        </form>
      </div>
    </div>
"""
)

ADMIN_PAGE = (
    TEMPLATE
    % """
    <h1 class="display-4 text-center mb-4">Welcome, Admin!</h1>
    <p class="lead text-center">Your solved the secure-cookie challenge of the GDSC 2023 CTF. You are truly remarkable!</p>
    <p class="lead text-center">FLAG{Never Gonna Give You Up}</p>
"""
)

USER_PAGE = (
    TEMPLATE
    % """
    <h1 class="display-4 text-center mb-4">You are logged in as %(username)s</h1>
    <p class="lead text-center">Your user ID is %(id)s</p>
"""
)

PRIVACY_PAGE = (
    TEMPLATE
    % """
    <h1>Privacy Policy</h1>
    <h2>Protecting Your Privacy</h2>
    <p>At Secret Website, we are committed to protecting the privacy and confidentiality of our users' personal information. This Privacy Policy explains how we collect, use, and safeguard your data when you interact with our website.</p>
    <h2>Collection and Use of Information</h2>
    <p>We may collect certain personal information from you when you register on our website, such as your username and email address. Rest assured that this information is securely stored and used solely for the purpose of providing you with a personalized experience on our platform.</p>
    <h2>Cookie Policy</h2>
    <p>Our website uses cookies to enhance your browsing experience and ensure the proper functioning of our services. These cookies do not contain any personally identifiable information and are used only for technical purposes.</p>
    <h2>Data Security</h2>
    <p>We employ robust security measures to protect your data from unauthorized access, alteration, or disclosure. Our encryption protocols, firewalls, and regular security audits ensure that your information is safe and secure.</p>
    <h2>Python Code</h2>
    <p>For the sake of transparency, we provide the Python code that powers our website. You can download the code by clicking the link below:</p>
    <p><a href="/downloads/code.py" download>Download Python Code</a></p>
"""
)


def check_cookie(cookie):
    if not cookie:
        return None

    cookie_bytes = base64.b64decode(cookie)
    iv, ciphertext = cookie_bytes[:BLOCK_SIZE], cookie_bytes[BLOCK_SIZE:]

    if len(iv) != BLOCK_SIZE or not ciphertext or len(ciphertext) % BLOCK_SIZE != 0:
        return None

    cipher = ciphers.Cipher(ALGO, modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(ALGO.block_size).unpadder()
    try:
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    except ValueError:
        flask.abort(401)

    return json.loads(plaintext.decode("utf8", errors="replace"))


def create_cookie(username, email):
    id = random.randint(0x8000_0000, 0xFFFF_FFFF)

    iv = os.getrandom(BLOCK_SIZE)

    plaintext = json.dumps({"id": id, "email": email, "username": username}).encode(
        "utf8"
    )

    padder = padding.PKCS7(ALGO.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    cipher = ciphers.Cipher(ALGO, modes.CBC(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return base64.b64encode(iv + ciphertext)


@app.route("/")
def index():
    cookie = flask.request.args.get("cookie")

    result = check_cookie(cookie)
    if not result:
        return WELCOME_PAGE

    if result["id"] == 1:
        return ADMIN_PAGE

    return USER_PAGE % result


@app.route("/register", methods=["POST"])
def register():
    username = flask.request.form["username"]
    email = flask.request.form["email"]

    cookie = create_cookie(username, email)
    return flask.redirect(flask.url_for("index", cookie=cookie))


@app.route("/privacy")
def privacy():
    return PRIVACY_PAGE


@app.route("/static/style.css")
def static_css():
    return flask.send_from_directory("static", "style.css", mimetype="text/css")


@app.route("/downloads/code.py")
def download_code():
    filename = "downloads/code.py"
    file_path = os.path.join(app.root_path, filename)
    return flask.send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
