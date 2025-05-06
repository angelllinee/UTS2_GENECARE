import boto3
import base64

class AWSKMSManager:
    def __init__(self, key_id, region_name='ap-southeast-1'):
        self.kms_client = boto3.client('kms', region_name=region_name)
        self.key_id = key_id  # <-- pastikan key_id sudah sesuai dengan key yang baru

    def generate_data_key(self):
        response = self.kms_client.generate_data_key(KeyId=self.key_id, KeySpec='AES_256')
        data_key_plain = response['Plaintext']
        data_key_encrypted = base64.b64encode(response['CiphertextBlob']).decode()
        return {
            'data_key_plain': data_key_plain,
            'data_key_encrypted': data_key_encrypted
        }

    def decrypt_data_key(self, encrypted_data_key_b64):
        encrypted_blob = base64.b64decode(encrypted_data_key_b64)
        response = self.kms_client.decrypt(CiphertextBlob=encrypted_blob)
        return response['Plaintext']
