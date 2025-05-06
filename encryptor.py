import base64
from Crypto.Cipher import AES

class AESEncryptor:
    def __init__(self, data_key):
        self.data_key = data_key

    def encrypt(self, plaintext_bytes):
        cipher = AES.new(self.data_key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)
        return {
            'ciphertext': base64.b64encode(ciphertext).decode(),
            'nonce': base64.b64encode(cipher.nonce).decode(),
            'tag': base64.b64encode(tag).decode()
        }

    def decrypt(self, ciphertext_b64, nonce_b64, tag_b64):
        ciphertext = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        tag = base64.b64decode(tag_b64)
        cipher = AES.new(self.data_key, AES.MODE_GCM, nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)
