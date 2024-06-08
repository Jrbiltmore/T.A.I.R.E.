"""
data_collector.py

This module is responsible for collecting data from various sources to build comprehensive intelligence profiles. 
It integrates multiple data gathering techniques to ensure accurate and up-to-date information collection.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import requests
import json
import os
from datetime import datetime

class DataCollector:
    def __init__(self, api_file_path, data_file_path):
        """
        Initialize the DataCollector with paths to the API JSON file and data file.
        
        :param api_file_path: Path to the JSON file containing API sources.
        :param data_file_path: Path to the JSON file where collected data will be stored.
        """
        self.api_file_path = api_file_path
        self.data_file_path = data_file_path
        self.data = []
        self.sources = self.load_api_sources()
        self.ensure_files_exist()

    def ensure_files_exist(self):
        """
        Ensure that the necessary JSON files exist, creating them with default values if they do not.
        """
        if not os.path.exists(self.api_file_path):
            print(f"{self.api_file_path} not found. Creating default API file.")
            default_apis = {
                "sources": [
                    {
                        "name": "Example API 1",
                        "url": "https://api.example.com/source1"
                    },
                    {
                        "name": "Example API 2",
                        "url": "https://api.example.com/source2"
                    }
                ]
            }
            with open(self.api_file_path, 'w') as file:
                json.dump(default_apis, file, indent=4)
        
        if not os.path.exists(self.data_file_path):
            print(f"{self.data_file_path} not found. Creating default data file.")
            with open(self.data_file_path, 'w') as file:
                json.dump([], file, indent=4)

    def load_api_sources(self):
        """
        Load API sources from the provided JSON file.
        
        :return: List of API sources.
        """
        try:
            with open(self.api_file_path, 'r') as file:
                apis = json.load(file)
                return apis.get("sources", [])
        except Exception as e:
            print(f"Error occurred while loading API sources: {e}")
            return []

    def collect_data(self):
        """
        Collect data from all specified sources.
        """
        for source in self.sources:
            try:
                response = requests.get(source['url'])
                if response.status_code == 200:
                    self.data.append({"source_name": source['name'], "data": response.json()})
                else:
                    print(f"Failed to retrieve data from {source['name']}")
            except Exception as e:
                print(f"Error occurred while fetching data from {source['name']}: {e}")

    def save_data(self):
        """
        Save the collected data to a JSON file.
        """
        try:
            with open(self.data_file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            print(f"Data successfully saved to {self.data_file_path}")
        except Exception as e:
            print(f"Error occurred while saving data: {e}")

    def load_data(self):
        """
        Load data from a JSON file.
        """
        try:
            with open(self.data_file_path, 'r') as file:
                self.data = json.load(file)
            print(f"Data successfully loaded from {self.data_file_path}")
        except Exception as e:
            print(f"Error occurred while loading data: {e}")

    def print_summary(self):
        """
        Print a summary of the collected data.
        """
        print(f"Data collected from {len(self.sources)} sources.")
        for i, entry in enumerate(self.data):
            print(f"Source {i + 1}: {entry['source_name']} - {len(entry['data'])} entries")

if __name__ == "__main__":
    # Define the paths to the JSON files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_file_path = os.path.join(current_dir, 'APIs.json')
    data_file_path = os.path.join(current_dir, 'collected_data.json')

    collector = DataCollector(api_file_path, data_file_path)
    collector.collect_data()
    collector.save_data()
    collector.print_summary()
