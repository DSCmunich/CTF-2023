import requests
import urllib.parse
import re
import base64

# Create random Token
r = requests.post(
    url="http://127.0.0.1:5000/register",
    data={"username": "daniel", "email": "daniel@code-byter.com"},
)
token = base64.b64decode(urllib.parse.unquote(r.url[29:]))
print(f"Token: {base64.b64encode(bytes(token))}")

# Get userid
r = requests.get(
    f"http://127.0.0.1:5000/?token={urllib.parse.quote(base64.b64encode(token))}"
)
user_id = bytearray(
    re.search("(?<=Your user ID is )\d{10}", r.text).group(0).encode("UTF-8")
)

# XOR IV to manipulate the first 16 bit. As the 17th bit is still a random number form the user if,
# we can adda random key to the plaintext to keep a valid json string
# From {"id": 3276795153, "username": "daniel", "email": "daniel@code-byter.com"}
# {"id": 1 , "x": 3, "username": "daniel", "email": "daniel@code-byter.com"}
token = bytearray(token)
token[7] = token[7] ^ user_id[0] ^ ord("1")
token[8] = token[8] ^ user_id[1] ^ ord(" ")
token[9] = token[9] ^ user_id[2] ^ ord(",")
token[10] = token[10] ^ user_id[3] ^ ord(" ")
token[11] = token[11] ^ user_id[4] ^ ord('"')
token[12] = token[12] ^ user_id[5] ^ ord("x")
token[13] = token[13] ^ user_id[6] ^ ord('"')
token[14] = token[14] ^ user_id[7] ^ ord(":")
token[15] = token[15] ^ user_id[8] ^ ord(" ")

print(
    f"Admin URL: http://127.0.0.1:5000/?token={urllib.parse.quote(base64.b64encode(bytes(token)))}"
)
