"""
data_decryptor.py

This module is responsible for decrypting data from various sources. 
It integrates multiple decryption techniques to handle different types of encrypted data.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import base64
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class DataDecryptor:
    def __init__(self, config_file):
        """
        Initialize the DataDecryptor with a configuration file.
        
        :param config_file: Path to the JSON file containing decryption configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.decrypted_data = []

    def load_config(self):
        """
        Load decryption configurations from the provided JSON file.
        
        :return: Decryption configurations.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error occurred while loading configurations: {e}")
            return {}

    def decrypt_data(self):
        """
        Decrypt data based on the loaded configurations.
        """
        for encryption in self.config.get("encryptions", []):
            try:
                decrypted_data = self.decrypt(encryption)
                self.decrypted_data.append(decrypted_data)
                print(f"Decrypted data: {decrypted_data}")
            except Exception as e:
                print(f"Error occurred while decrypting data: {e}")

    def decrypt(self, encryption):
        """
        Decrypt a specific encrypted data.
        
        :param encryption: The encryption configuration.
        :return: Decrypted data.
        """
        method = encryption.get("method")
        if method == "fernet":
            return self.decrypt_fernet(encryption)
        elif method == "aes":
            return self.decrypt_aes(encryption)
        else:
            raise ValueError(f"Unsupported decryption method: {method}")

    def decrypt_fernet(self, encryption):
        """
        Decrypt data encrypted with Fernet.
        
        :param encryption: The encryption configuration.
        :return: Decrypted data.
        """
        key = encryption.get("key")
        cipher_text = encryption.get("cipher_text")
        fernet = Fernet(key)
        return fernet.decrypt(cipher_text.encode()).decode()

    def decrypt_aes(self, encryption):
        """
        Decrypt data encrypted with AES.
        
        :param encryption: The encryption configuration.
        :return: Decrypted data.
        """
        key = base64.b64decode(encryption.get("key"))
        iv = base64.b64decode(encryption.get("iv"))
        cipher_text = base64.b64decode(encryption.get("cipher_text"))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
        return decrypted_data.decode()

    def save_decrypted_data(self, file_path):
        """
        Save the decrypted data to a JSON file.
        
        :param file_path: Path to the file where the decrypted data will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump({"decrypted_data": self.decrypted_data}, file, indent=4)
            print(f"Decrypted data successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving decrypted data: {e}")

    def load_decrypted_data(self, file_path):
        """
        Load decrypted data from a JSON file.
        
        :param file_path: Path to the file from which the decrypted data will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.decrypted_data = json.load(file).get("decrypted_data", [])
            print(f"Decrypted data successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading decrypted data: {e}")

    def print_summary(self):
        """
        Print a summary of the decrypted data.
        """
        print("Decrypted Data Summary:")
        for i, data in enumerate(self.decrypted_data):
            print(f"Data {i + 1}: {data}")

if __name__ == "__main__":
    config_file_path = 'data_decryption_config.json'
    decrypted_data_file_path = 'decrypted_data.json'

    # Ensure data_decryption_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "encryptions": [
                {
                    "method": "fernet",
                    "key": Fernet.generate_key().decode(),
                    "cipher_text": Fernet(Fernet.generate_key()).encrypt(b"Example data").decode()
                },
                {
                    "method": "aes",
                    "key": base64.b64encode(os.urandom(32)).decode(),
                    "iv": base64.b64encode(os.urandom(16)).decode(),
                    "cipher_text": base64.b64encode(AES.new(base64.b64decode(os.urandom(32)), AES.MODE_CBC, base64.b64decode(os.urandom(16))).encrypt(b"Example data".ljust(32))).decode()
                }
            ]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    decryptor = DataDecryptor(config_file_path)
    decryptor.decrypt_data()
    decryptor.save_decrypted_data(decrypted_data_file_path)
    decryptor.print_summary()
