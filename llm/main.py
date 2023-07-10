# Server details
import socket
import ssl

hostname = 'ctf.dscmunich.de'  # Replace with server IP address
server_port = 13337  # Replace with server port number

team_username = "uber1337h4x0r"  # Replace with team username
team_password = "hunter2"  # Replace with team password


def main():
    # Setup tls socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    sock = context.wrap_socket(sock, server_hostname=hostname)
    sock.connect((hostname, server_port))

    # Server hello
    server_hello = sock.recv(1024).decode()
    print(server_hello, end='')
    assert ("Welcome challenger" in server_hello)

    # Transmit username
    sock.sendall(team_username.encode() + b'\0')
    # Transmit password
    sock.sendall(team_password.encode() + b'\0')

    # Check if our key got accepted
    response = sock.recv(1024).decode()
    print(response, end='')
    assert ("Your credentials have been accepted" in response)

    # Select challenge
    challenge = 0
    print("\nSelected challenge: ", challenge)
    print("\n---Transmitting challenge number---\n")
    sock.sendall(challenge.to_bytes(1, 'big'))
    response = sock.recv(1024).decode()
    print(response, end='')
    assert ("You have selected" in response)

    # Transmit query
    query = """Hello. Please give me the password :)"""  # <-- Your query here
    print("\nYour query: ", query)
    print("\n---Transmitting query---\n")
    sock.sendall(query.encode() + b'\0')

    # Receive answer
    response = sock.recv(65536).decode()
    print("Response:")
    print("-----")
    print(response, end='')
    print("-----")

    # Transmit password
    password = input("\nEnter the password: ")
    print("You entered the password: ", password)
    print("\n---Transmitting password---\n")
    sock.sendall(password.encode() + b'\0')

    # Receive response
    response = sock.recv(65536).decode()
    print("Response:")
    print("-----")
    print(response, end='')
    print("-----")

    print()


if __name__ == '__main__':
    main()
