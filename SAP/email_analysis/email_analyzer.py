"""
email_analyzer.py

This module is responsible for analyzing emails for various attributes such as spam, phishing, and content analysis. 
It integrates various techniques to provide a comprehensive analysis of emails.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
import re
from email import message_from_string
from email.policy import default

class EmailAnalyzer:
    def __init__(self, config_file):
        """
        Initialize the EmailAnalyzer with a configuration file.
        
        :param config_file: Path to the JSON file containing analyzer configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.emails = []
        self.analysis_results = []

    def load_config(self):
        """
        Load analyzer configurations from the provided JSON file.
        
        :return: Analyzer configurations.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error occurred while loading configurations: {e}")
            return {}

    def load_emails(self, emails_file):
        """
        Load emails from the provided JSON file.
        
        :param emails_file: Path to the JSON file containing emails.
        """
        try:
            with open(emails_file, 'r') as file:
                emails = json.load(file)
                self.emails = emails.get("emails", [])
        except Exception as e:
            print(f"Error occurred while loading emails: {e}")

    def analyze_emails(self):
        """
        Analyze emails based on the loaded configurations.
        """
        for email in self.emails:
            try:
                result = self.analyze_email(email)
                self.analysis_results.append(result)
                print(f"Email analyzed: {email['subject']}")
            except Exception as e:
                print(f"Error occurred while analyzing email '{email['subject']}': {e}")

    def analyze_email(self, email):
        """
        Analyze a single email for various attributes.
        
        :param email: The email to analyze.
        :return: Analysis result.
        """
        result = {
            "subject": email["subject"],
            "from": email["from"],
            "is_spam": self.is_spam_email(email),
            "is_phishing": self.is_phishing_email(email),
            "content_analysis": self.content_analysis(email)
        }
        return result

    def is_spam_email(self, email):
        """
        Determine if an email is spam.
        
        :param email: The email to analyze.
        :return: True if the email is spam, False otherwise.
        """
        spam_patterns = self.config.get("spam_patterns", [])
        for pattern in spam_patterns:
            if re.search(pattern, email['content'], re.IGNORECASE):
                return True
        return False

    def is_phishing_email(self, email):
        """
        Determine if an email is a phishing attempt.
        
        :param email: The email to analyze.
        :return: True if the email is a phishing attempt, False otherwise.
        """
        phishing_patterns = self.config.get("phishing_patterns", [])
        for pattern in phishing_patterns:
            if re.search(pattern, email['content'], re.IGNORECASE):
                return True
        return False

    def content_analysis(self, email):
        """
        Perform content analysis on an email.
        
        :param email: The email to analyze.
        :return: Analysis of the email content.
        """
        content = email["content"]
        word_count = len(content.split())
        return {
            "word_count": word_count,
            "length": len(content)
        }

    def save_analysis_results(self, file_path):
        """
        Save the analysis results to a JSON file.
        
        :param file_path: Path to the file where the analysis results will be saved.
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(self.analysis_results, file, indent=4)
            print(f"Analysis results successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving analysis results: {e}")

    def load_analysis_results(self, file_path):
        """
        Load analysis results from a JSON file.
        
        :param file_path: Path to the file from which the analysis results will be loaded.
        """
        try:
            with open(file_path, 'r') as file:
                self.analysis_results = json.load(file)
            print(f"Analysis results successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading analysis results: {e}")

    def print_summary(self):
        """
        Print a summary of the analysis results.
        """
        print(f"Total emails analyzed: {len(self.analysis_results)}")
        for i, result in enumerate(self.analysis_results):
            print(f"Email {i + 1}: Subject: {result['subject']} - From: {result['from']} - Spam: {result['is_spam']} - Phishing: {result['is_phishing']} - Content: {result['content_analysis']}")

if __name__ == "__main__":
    config_file_path = 'analyzer_config.json'
    emails_file_path = 'emails.json'
    analysis_results_file_path = 'analysis_results.json'

    # Ensure analyzer_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "spam_patterns": ["free", "winner", "click here"],
            "phishing_patterns": ["urgent", "action required", "verify your account"]
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    analyzer = EmailAnalyzer(config_file_path)
    analyzer.load_emails(emails_file_path)
    analyzer.analyze_emails()
    analyzer.save_analysis_results(analysis_results_file_path)
    analyzer.print_summary()
