import base64
import random

def encrypt_pdf(file_path, output_path):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Generate a random 4-byte key
    key = bytearray(random.getrandbits(8) for _ in range(4))

    # Perform encryption with a vulnerable block cipher
    ciphertext = encrypt_vulnerable(plaintext, key)

    with open(output_path, 'wb') as file:
        file.write(ciphertext)

    print('Encryption completed successfully.')
    print(f'Key: {base64.b64encode(key).decode()}')

def encrypt_vulnerable(plaintext, key):
    block_size = 4
    ciphertext = bytearray()

    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i+block_size]
        encrypted_block = bytearray(block[i] ^ key[i % 4] for i in range(len(block)))
        ciphertext.extend(encrypted_block)

    return ciphertext

# Usage example
input_file = 'plaintext.pdf'
encrypted_file = 'encrypted.pdf'

# Encrypt the PDF file
encrypt_pdf(input_file, encrypted_file)