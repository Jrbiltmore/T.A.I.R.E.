"""
password_rules_collector.py

This module is responsible for collecting and analyzing password rules from various sources. 
It integrates various techniques to gather comprehensive rules for use in password analysis and cracking.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import requests

class PasswordRulesCollector:
    def __init__(self, sources_file):
        """
        Initialize the PasswordRulesCollector with a list of sources.
        
        :param sources_file: Path to the JSON file containing data sources.
        """
        self.sources_file = sources_file
        self.sources = self.load_sources()
        self.rules = []

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

    def collect_rules(self):
        """
        Collect password rules from all specified sources.
        """
        for source in self.sources:
            try:
                response = requests.get(source['url'])
                if response.status_code == 200:
                    self.rules.append({"source_name": source['name'], "rules": response.json()})
                else:
                    print(f"Failed to retrieve rules from {source['name']}")
            except Exception as e:
                print(f"Error occurred while fetching rules from {source['name']}: {e}")

    def save_rules(self, file_path):
        """
        Save the collected rules to a JSON file.
        
        :param file_path: Path to the file where the rules will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.rules, file, indent=4)
            print(f"Rules successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving rules: {e}")

    def load_rules(self, file_path):
        """
        Load rules from a JSON file.
        
        :param file_path: Path to the file from which the rules will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.rules = json.load(file)
            print(f"Rules successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading rules: {e}")

    def print_summary(self):
        """
        Print a summary of the collected rules.
        """
        print(f"Rules collected from {len(self.sources)} sources.")
        for i, entry in enumerate(self.rules):
            print(f"Source {i + 1}: {entry['source_name']} - {len(entry['rules'])} rules")

if __name__ == "__main__":
    sources_file_path = 'password_rules_sources.json'
    rules_file_path = 'password_rules.json'

    # Ensure password_rules_sources.json exists
    if not os.path.exists(sources_file_path):
        print(f"{sources_file_path} not found. Creating default sources file.")
        default_sources = {
            "sources": [
                {
                    "name": "Example Source 1",
                    "url": "https://api.example.com/rules1"
                },
                {
                    "name": "Example Source 2",
                    "url": "https://api.example.com/rules2"
                }
            ]
        }
        with open(sources_file_path, 'w') as file:
            json.dump(default_sources, file, indent=4)

    collector = PasswordRulesCollector(sources_file_path)
    collector.collect_rules()
    collector.save_rules(rules_file_path)
    collector.print_summary()
