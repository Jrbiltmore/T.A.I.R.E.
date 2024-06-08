"""
cipher_decryptor.py

This module is responsible for decrypting various cipher texts. 
It integrates multiple decryption techniques to handle different types of encrypted data.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class CipherDecryptor:
    def __init__(self, config_file):
        """
        Initialize the CipherDecryptor with a configuration file.
        
        :param config_file: Path to the JSON file containing decryption configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.decrypted_texts = []

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

    def decrypt_texts(self):
        """
        Decrypt texts based on the loaded configurations.
        """
        for encryption in self.config.get("encryptions", []):
            try:
                decrypted_text = self.decrypt(encryption)
                self.decrypted_texts.append(decrypted_text)
                print(f"Decrypted text: {decrypted_text}")
            except Exception as e:
                print(f"Error occurred while decrypting text: {e}")

    def decrypt(self, encryption):
        """
        Decrypt a specific encrypted text.
        
        :param encryption: The encryption configuration.
        :return: Decrypted text.
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
        Decrypt a text encrypted with Fernet.
        
        :param encryption: The encryption configuration.
        :return: Decrypted text.
        """
        key = encryption.get("key")
        cipher_text = encryption.get("cipher_text")
        fernet = Fernet(key)
        return fernet.decrypt(cipher_text.encode()).decode()

    def decrypt_aes(self, encryption):
        """
        Decrypt a text encrypted with AES.
        
        :param encryption: The encryption configuration.
        :return: Decrypted text.
        """
        key = base64.b64decode(encryption.get("key"))
        iv = base64.b64decode(encryption.get("iv"))
        cipher_text = base64.b64decode(encryption.get("cipher_text"))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
        return decrypted_text.decode()

    def save_decrypted_texts(self, file_path):
        """
        Save the decrypted texts to a JSON file.
        
        :param file_path: Path to the file where the decrypted texts will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump({"decrypted_texts": self.decrypted_texts}, file, indent=4)
            print(f"Decrypted texts successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving decrypted texts: {e}")

    def load_decrypted_texts(self, file_path):
        """
        Load decrypted texts from a JSON file.
        
        :param file_path: Path to the file from which the decrypted texts will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.decrypted_texts = json.load(file).get("decrypted_texts", [])
            print(f"Decrypted texts successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading decrypted texts: {e}")

    def print_summary(self):
        """
        Print a summary of the decrypted texts.
        """
        print("Decrypted Texts Summary:")
        for i, text in enumerate(self.decrypted_texts):
            print(f"Text {i + 1}: {text}")

if __name__ == "__main__":
    config_file_path = 'decryption_config.json'
    decrypted_texts_file_path = 'decrypted_texts.json'

    # Ensure decryption_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "encryptions": [
                {
                    "method": "fernet",
                    "key": Fernet.generate_key().decode(),
                    "cipher_text": Fernet(Fernet.generate_key()).encrypt(b"Example text").decode()
                },
                {
                    "method": "aes",
                    "key": base64.b64encode(os.urandom(32)).decode(),
                    "iv": base64.b64encode(os.urandom(16)).decode(),
                    "cipher_text": base64.b64encode(AES.new(base64.b64decode(os.urandom(32)), AES.MODE_CBC, base64.b64decode(os.urandom(16))).encrypt(b"Example text".ljust(32))).decode()
                }
            ]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    decryptor = CipherDecryptor(config_file_path)
    decryptor.decrypt_texts()
    decryptor.save_decrypted_texts(decrypted_texts_file_path)
    decryptor.print_summary()
