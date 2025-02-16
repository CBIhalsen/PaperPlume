from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import yaml
import base64

class AESCipher:
    def __init__(self):
        self.key = self._load_key()

    def _load_key(self):
        file_path = 'config/config.yaml'
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.load(file, Loader=yaml.SafeLoader)
            value = yaml_data['key']
        return bytes(value.encode('utf-8'))

    def encrypt(self, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encrypted_data_base64 = base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        return encrypted_data_base64

    def decrypt(self, encrypted_data):
        cipher = Cipher(algorithms.AES(self.key), modes.ECB(), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(base64.urlsafe_b64decode(encrypted_data)) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return decrypted_data.decode('utf-8')
