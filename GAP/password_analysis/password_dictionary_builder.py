"""
password_dictionary_builder.py

This module is responsible for building password dictionaries for password cracking. 
It integrates various techniques to create comprehensive dictionaries for use in password analysis.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import itertools

class PasswordDictionaryBuilder:
    def __init__(self, config_file):
        """
        Initialize the PasswordDictionaryBuilder with a configuration file.
        
        :param config_file: Path to the JSON file containing dictionary configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.dictionary = []

    def load_config(self):
        """
        Load dictionary configurations from the provided JSON file.
        
        :return: Dictionary configurations.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error occurred while loading configurations: {e}")
            return {}

    def build_dictionary(self):
        """
        Build the password dictionary based on the loaded configurations.
        """
        try:
            base_words = self.config.get("base_words", [])
            patterns = self.config.get("patterns", [])
            for pattern in patterns:
                for word in base_words:
                    combinations = self.apply_pattern(word, pattern)
                    self.dictionary.extend(combinations)
            print("Password dictionary built successfully.")
        except Exception as e:
            print(f"Error occurred while building dictionary: {e}")

    def apply_pattern(self, word, pattern):
        """
        Apply a pattern to a base word to generate variations.
        
        :param word: The base word to apply the pattern to.
        :param pattern: The pattern to apply.
        :return: List of word variations.
        """
        return [word + p for p in pattern]

    def save_dictionary(self, file_path):
        """
        Save the password dictionary to a JSON file.
        
        :param file_path: Path to the file where the dictionary will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.dictionary, file, indent=4)
            print(f"Password dictionary successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving dictionary: {e}")

    def load_dictionary(self, file_path):
        """
        Load the password dictionary from a JSON file.
        
        :param file_path: Path to the file from which the dictionary will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.dictionary = json.load(file)
            print(f"Password dictionary successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading dictionary: {e}")

    def print_summary(self):
        """
        Print a summary of the password dictionary.
        """
        print("Password Dictionary Summary:")
        for i, word in enumerate(self.dictionary):
            print(f"Word {i + 1}: {word}")

if __name__ == "__main__":
    config_file_path = 'dictionary_config.json'
    dictionary_file_path = 'password_dictionary.json'

    # Ensure dictionary_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "base_words": ["password", "123456", "qwerty"],
            "patterns": [["!", "@", "#"], ["123", "456", "789"]]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    builder = PasswordDictionaryBuilder(config_file_path)
    builder.build_dictionary()
    builder.save_dictionary(dictionary_file_path)
    builder.print_summary()
