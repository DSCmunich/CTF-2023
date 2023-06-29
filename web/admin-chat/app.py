import os
import time
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

EASY_CHALLENGE_URL = os.getenv("EASY_CHALLENGE_URL") or "localhost:8081"
HARD_CHALLENGE_URL = os.getenv("HARD_CHALLENGE_URL") or "localhost:8082"
EASY_CHALLENGE_FLAG = os.getenv("EASY_CHALLENGE_FLAG")
HARD_CHALLENGE_FLAG = os.getenv("HARD_CHALLENGE_FLAG")
try:
    PORT = int(os.getenv("PORT"))
except:
    PORT = 8080

MESSAGES_SUCCESS = [
    "Fun Link!",
    "Hmm, looks interesting.",
    "LOL!",
    "LMFAO",
    "Ohh, cool"
]
MESSAGES_FAILURE = [
    "That looks broken.",
    "Why would you send me this broken thing?",
    "I dont think that worked.",
    "Please send a working link next time",
]

def open_url_as_admin(url):
    if not url.startswith(EASY_CHALLENGE_URL) and not url.startswith(HARD_CHALLENGE_URL):
        return False

    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox") # TODO?!
    driver = webdriver.Chrome("chromedriver", chrome_options=chrome_options)

    success = False
    try:
        # https://stackoverflow.com/a/28331099
        if url.startswith(EASY_CHALLENGE_URL):
            driver.get(EASY_CHALLENGE_URL + "/404")
            driver.add_cookie({'name': 'PASSWORD', 'value': EASY_CHALLENGE_FLAG, 'domain': EASY_CHALLENGE_URL})
        elif url.startswith(HARD_CHALLENGE_URL):
            driver.get(HARD_CHALLENGE_URL + "/404")
            driver.add_cookie({'name': 'PASSWORD', 'value': HARD_CHALLENGE_FLAG, 'domain': HARD_CHALLENGE_URL})

        driver.get(url)
        time.sleep(3)
        success = True
    except:
        pass
    finally:
        driver.quit()

    return success

class RequestHandler(BaseHTTPRequestHandler):
    def send(self, status, msg):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(msg.encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.lower()
        params = parse_qs(parsed.query)

        if path == "/":
            with open("frontend/index.html", "r") as fd:
                self.send(200, fd.read())
        elif path in ["/styles.css", "/client.js", ""]:
            with open("frontend" + path, "r") as fd:
                self.send(200, fd.read())
        elif self.path.startswith("/send") and "url" in params:
            success = open_url_as_admin(params["url"][0])
            self.send(200, random.choice(MESSAGES_SUCCESS if success else MESSAGES_FAILURE))
        else:
            self.send(404, "not found")

class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == "__main__":
    print(f"Starting on port {PORT} with challenge URLs {EASY_CHALLENGE_URL} and {MEDIUM_CHALLENGE_URL}")
    httpd = ThreadingHttpServer(("0.0.0.0", PORT), RequestHandler)
    httpd.serve_forever()
