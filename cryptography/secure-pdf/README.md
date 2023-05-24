# Secure PDF

Author: @code_byter \
Points: tbd... (easy)

## Description

Your friend, a talented developer, has come up with a custom encryption algorithm to securely transmit sensitive PDF files. They believe their encryption scheme is robust and can protect the data from any potential Man-in-the-Middle (MitM) attackers. However, they want to put their algorithm to the test and have asked for your assistance.

    def encrypt_secure(plaintext, key):
        block_size = 4
        ciphertext = bytearray()

        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i+block_size]
            encrypted_block = bytearray(block[i] ^ key[i % 4] for i in range(len(block)))
            ciphertext.extend(encrypted_block)

        return ciphertext

Your friend has encrypted a PDF file using their custom encryption algorithm and sent it to you. They are confident that the encrypted file is secure and challenge you to decrypt it without knowing the secret key. They assure you that the encryption algorithm relies on strong principles and should be resistant to attacks.

The file contains the secret flag. Can you reveal it, given the file decrypted.pdf?

## Solution

The file is encrypted with a 4 byte long key. This is vulnerable to plaintext attacks.
For pdf files, the first 4 bytes are known.

    def recover_key(ciphertext):
        known_plaintext = b'%PDF'

        # XOR the known plaintext with the ciphertext to recover the key
        key = bytearray(ciphertext[i] ^ known_plaintext[i] for i in range(len(known_plaintext)))
        print(f'Key: {base64.b64encode(key).decode()}')
        return key
