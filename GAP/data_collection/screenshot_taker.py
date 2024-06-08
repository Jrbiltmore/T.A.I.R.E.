"""
screenshot_taker.py

This module is responsible for taking screenshots for visual documentation. 
It integrates techniques to capture and save screenshots of target systems or websites.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import os
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class ScreenshotTaker:
    def __init__(self, targets_file):
        """
        Initialize the ScreenshotTaker with a list of targets.
        
        :param targets_file: Path to the JSON file containing targets.
        """
        self.targets_file = targets_file
        self.targets = self.load_targets()
        self.screenshots = []

    def load_targets(self):
        """
        Load targets from the provided JSON file.
        
        :return: List of targets.
        """
        try:
            with open(self.targets_file, 'r') as file:
                targets = json.load(file)
                return targets.get("targets", [])
        except Exception as e:
            print(f"Error occurred while loading targets: {e}")
            return []

    def take_screenshots(self):
        """
        Take screenshots of all specified targets.
        """
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for target in self.targets:
            try:
                driver.get(target['url'])
                time.sleep(2)  # wait for the page to load
                screenshot_path = f"screenshots/{target['name']}_{datetime.now().isoformat()}.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                driver.save_screenshot(screenshot_path)
                self.screenshots.append({"target_name": target['name'], "screenshot_path": screenshot_path})
                print(f"Screenshot taken for {target['name']}")
            except Exception as e:
                print(f"Error occurred while taking screenshot for {target['name']}: {e}")

        driver.quit()

    def save_screenshots_info(self, file_path):
        """
        Save the screenshots information to a JSON file.
        
        :param file_path: Path to the file where the screenshots information will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.screenshots, file, indent=4)
            print(f"Screenshots information successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving screenshots information: {e}")

    def load_screenshots_info(self, file_path):
        """
        Load screenshots information from a JSON file.
        
        :param file_path: Path to the file from which the screenshots information will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.screenshots = json.load(file)
            print(f"Screenshots information successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading screenshots information: {e}")

    def print_summary(self):
        """
        Print a summary of the taken screenshots.
        """
        print("Screenshot Summary:")
        for i, entry in enumerate(self.screenshots):
            print(f"Screenshot {i + 1}: Target '{entry['target_name']}' - Path: {entry['screenshot_path']}")

if __name__ == "__main__":
    targets_file_path = 'screenshot_targets.json'
    screenshots_info_file_path = 'screenshots_info.json'

    # Ensure screenshot_targets.json exists
    if not os.path.exists(targets_file_path):
        print(f"{targets_file_path} not found. Creating default targets file.")
        default_targets = {
            "targets": [
                {
                    "name": "Example Target 1",
                    "url": "https://www.example.com"
                },
                {
                    "name": "Example Target 2",
                    "url": "https://www.example.org"
                }
            ]
        }
        with open(targets_file_path, 'w') as file:
            json.dump(default_targets, file, indent=4)

    taker = ScreenshotTaker(targets_file_path)
    taker.take_screenshots()
    taker.save_screenshots_info(screenshots_info_file_path)
    taker.print_summary()
