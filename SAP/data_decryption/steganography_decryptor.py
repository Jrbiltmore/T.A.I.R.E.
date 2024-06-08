"""
steganography_decryptor.py

This module is responsible for decrypting data hidden using steganography techniques. 
It integrates various methods to extract hidden data from images or other files.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
from PIL import Image

class SteganographyDecryptor:
    def __init__(self, config_file):
        """
        Initialize the SteganographyDecryptor with a configuration file.
        
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
        Decrypt a specific encrypted data hidden using steganography.
        
        :param encryption: The encryption configuration.
        :return: Decrypted data.
        """
        file_path = encryption.get("file_path")
        method = encryption.get("method")
        if method == "LSB":
            return self.decrypt_lsb(file_path)
        else:
            raise ValueError(f"Unsupported steganography method: {method}")

    def decrypt_lsb(self, file_path):
        """
        Decrypt data hidden using Least Significant Bit (LSB) steganography.
        
        :param file_path: Path to the file containing hidden data.
        :return: Decrypted data.
        """
        image = Image.open(file_path)
        binary_data = ""
        for pixel in image.getdata():
            r, g, b = pixel[:3]
            binary_data += bin(r)[-1]  # Extract LSB of red channel
            binary_data += bin(g)[-1]  # Extract LSB of green channel
            binary_data += bin(b)[-1]  # Extract LSB of blue channel

        # Convert binary data to string
        byte_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        decrypted_data = ''.join([chr(int(byte, 2)) for byte in byte_data if int(byte, 2) != 0])
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
    config_file_path = 'steganography_decryption_config.json'
    decrypted_data_file_path = 'steganography_decrypted_data.json'

    # Ensure steganography_decryption_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "encryptions": [
                {
                    "file_path": "hidden_data_image.png",
                    "method": "LSB"
                }
            ]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    decryptor = SteganographyDecryptor(config_file_path)
    decryptor.decrypt_data()
    decryptor.save_decrypted_data(decrypted_data_file_path)
    decryptor.print_summary()
