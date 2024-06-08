"""
xor_decryptor.py

This module is responsible for decrypting data encrypted with XOR encryption. 
It integrates techniques to handle XOR-encrypted data.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json

class XORDecryptor:
    def __init__(self, config_file):
        """
        Initialize the XORDecryptor with a configuration file.
        
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
        Decrypt a specific XOR-encrypted data.
        
        :param encryption: The encryption configuration.
        :return: Decrypted data.
        """
        key = encryption.get("key")
        cipher_text = encryption.get("cipher_text")
        decrypted_data = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(cipher_text))
        return decrypted_data

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
    config_file_path = 'xor_decryption_config.json'
    decrypted_data_file_path = 'xor_decrypted_data.json'

    # Ensure xor_decryption_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "encryptions": [
                {
                    "key": "secret",
                    "cipher_text": ''.join(chr(ord(c) ^ ord("secret"[i % len("secret")])) for i, c in enumerate("Example data"))
                }
            ]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    decryptor = XORDecryptor(config_file_path)
    decryptor.decrypt_data()
    decryptor.save_decrypted_data(decrypted_data_file_path)
    decryptor.print_summary()
