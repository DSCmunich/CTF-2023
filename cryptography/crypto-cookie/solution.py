import requests
import urllib.parse
import re
import base64

# Create random cookie
r = requests.post(
    url="http://127.0.0.1:5000/register",
    data={"username": "daniel", "email": "daniel@code-byter.com"},
)
cookie = base64.b64decode(urllib.parse.unquote(r.url[29:]))
print(f"cookie: {base64.b64encode(bytes(cookie))}")

# Get userid
r = requests.get(
    f"http://127.0.0.1:5000/?cookie={urllib.parse.quote(base64.b64encode(cookie))}"
)
user_id = bytearray(
    re.search("(?<=Your user ID is )\d{10}", r.text).group(0).encode("UTF-8")
)

# XOR IV to manipulate the first 16 bit. As the 17th bit is still a random number form the user if,
# we can add a random key to the plaintext to keep a valid json string
# From {"id": 3276795153, "username": "daniel", "email": "daniel@code-byter.com"}
# {"id": 1 , "x": 3, "username": "daniel", "email": "daniel@code-byter.com"}
cookie = bytearray(cookie)
cookie[7] = cookie[7] ^ user_id[0] ^ ord("1")
cookie[8] = cookie[8] ^ user_id[1] ^ ord(" ")
cookie[9] = cookie[9] ^ user_id[2] ^ ord(",")
cookie[10] = cookie[10] ^ user_id[3] ^ ord(" ")
cookie[11] = cookie[11] ^ user_id[4] ^ ord('"')
cookie[12] = cookie[12] ^ user_id[5] ^ ord("x")
cookie[13] = cookie[13] ^ user_id[6] ^ ord('"')
cookie[14] = cookie[14] ^ user_id[7] ^ ord(":")
cookie[15] = cookie[15] ^ user_id[8] ^ ord(" ")

print(
    f"Admin URL: http://127.0.0.1:5000/?cookie={urllib.parse.quote(base64.b64encode(bytes(cookie)))}"
)
