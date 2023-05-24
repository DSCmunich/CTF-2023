import base64

def decrypt_pdf(file_path, output_path):
    with open(file_path, 'rb') as file:
        ciphertext = file.read()

    # Recover the key using the first known bytes
    key = recover_key(ciphertext)

    # Perform decryption using the recovered key
    plaintext = decrypt_with_key(ciphertext, key)

    with open(output_path, 'wb') as file:
        file.write(plaintext)

    print('Decryption completed successfully.')

def recover_key(ciphertext):
    known_plaintext = b'%PDF'

    # XOR the known plaintext with the ciphertext to recover the key
    key = bytearray(ciphertext[i] ^ known_plaintext[i] for i in range(len(known_plaintext)))
    print(f'Key: {base64.b64encode(key).decode()}')
    return key

def decrypt_with_key(ciphertext, key):
    # XOR the ciphertext with the key to obtain the plaintext
    plaintext = bytearray(ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext)))

    return plaintext

# Usage example
encrypted_file = 'encrypted.pdf'
decrypted_file = 'decrypted.pdf'

# Decrypt the encrypted PDF file
decrypt_pdf(encrypted_file, decrypted_file)
