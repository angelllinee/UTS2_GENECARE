import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

class KeyManager:
    def __init__(self):
        self.master_key = get_random_bytes(32)  # Simulasi master key (KMS)

    def generate_data_key(self):
        data_key = get_random_bytes(32)
        cipher = AES.new(self.master_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data_key)
        return {
            'data_key_plain': data_key,
            'data_key_encrypted': base64.b64encode(cipher.nonce + ciphertext).decode()
        }

    def decrypt_data_key(self, encrypted_data_key_b64):
        encrypted = base64.b64decode(encrypted_data_key_b64)
        nonce = encrypted[:16]
        ciphertext = encrypted[16:]
        cipher = AES.new(self.master_key, AES.MODE_EAX, nonce)
        return cipher.decrypt(ciphertext)
