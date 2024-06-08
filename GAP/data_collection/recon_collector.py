"""
recon_collector.py

This module is responsible for collecting reconnaissance data from various sources. 
It integrates multiple data collection techniques to gather comprehensive and actionable intelligence.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import requests
import json
import os
from datetime import datetime

class ReconCollector:
    def __init__(self, sources_file):
        """
        Initialize the ReconCollector with a list of sources.
        
        :param sources_file: Path to the JSON file containing data sources.
        """
        self.sources_file = sources_file
        self.sources = self.load_sources()
        self.data = []

    def load_sources(self):
        """
        Load sources from the provided JSON file.
        
        :return: List of data sources.
        """
        try:
            with open(self.sources_file, 'r') as file:
                sources = json.load(file)
                return sources.get("sources", [])
        except Exception as e:
            print(f"Error occurred while loading sources: {e}")
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

    def save_data(self, file_path):
        """
        Save the collected data to a JSON file.
        
        :param file_path: Path to the file where the data will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving data: {e}")

    def load_data(self, file_path):
        """
        Load data from a JSON file.
        
        :param file_path: Path to the file from which the data will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            print(f"Data successfully loaded from {file_path}")
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
    sources_file_path = 'recon_sources.json'
    data_file_path = 'recon_data.json'

    # Ensure recon_sources.json exists
    if not os.path.exists(sources_file_path):
        print(f"{sources_file_path} not found. Creating default sources file.")
        default_sources = {
            "sources": [
                {
                    "name": "Example Source 1",
                    "url": "https://api.example.com/source1"
                },
                {
                    "name": "Example Source 2",
                    "url": "https://api.example.com/source2"
                }
            ]
        }
        with open(sources_file_path, 'w') as file:
            json.dump(default_sources, file, indent=4)

    collector = ReconCollector(sources_file_path)
    collector.collect_data()
    collector.save_data(data_file_path)
    collector.print_summary()
