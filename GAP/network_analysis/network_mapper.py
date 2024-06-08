"""
network_mapper.py

This module is responsible for mapping network topology and identifying active devices. 
It integrates various techniques to create a comprehensive map of the network.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import subprocess

class NetworkMapper:
    def __init__(self, config_file):
        """
        Initialize the NetworkMapper with a configuration file.
        
        :param config_file: Path to the JSON file containing network mapping configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.network_map = []

    def load_config(self):
        """
        Load network mapping configurations from the provided JSON file.
        
        :return: Network mapping configurations.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error occurred while loading configurations: {e}")
            return {}

    def map_network(self):
        """
        Map the network based on the loaded configurations.
        """
        try:
            ip_range = self.config.get("ip_range", "192.168.1.0/24")
            command = f"nmap -sn {ip_range}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.network_map.append({"command": command, "result": result.stdout})
            print("Network mapping completed successfully.")
        except Exception as e:
            print(f"Error occurred while mapping network: {e}")

    def save_network_map(self, file_path):
        """
        Save the network map to a JSON file.
        
        :param file_path: Path to the file where the network map will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.network_map, file, indent=4)
            print(f"Network map successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving network map: {e}")

    def load_network_map(self, file_path):
        """
        Load the network map from a JSON file.
        
        :param file_path: Path to the file from which the network map will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.network_map = json.load(file)
            print(f"Network map successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading network map: {e}")

    def print_summary(self):
        """
        Print a summary of the network map.
        """
        print("Network Map Summary:")
        for i, entry in enumerate(self.network_map):
            print(f"Map {i + 1}: Command '{entry['command']}' - Result: {entry['result']}")

if __name__ == "__main__":
    config_file_path = 'network_config.json'
    map_file_path = 'network_map.json'

    # Ensure network_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "ip_range": "192.168.1.0/24"
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    mapper = NetworkMapper(config_file_path)
    mapper.map_network()
    mapper.save_network_map(map_file_path)
    mapper.print_summary()
