"""
performance_monitor.py

This module is responsible for monitoring system performance metrics. 
It integrates various monitoring techniques to collect and analyze performance data.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import psutil
import json
import os
from datetime import datetime

class PerformanceMonitor:
    def __init__(self, metrics_file):
        """
        Initialize the PerformanceMonitor with a file to save metrics.
        
        :param metrics_file: Path to the JSON file to save performance metrics.
        """
        self.metrics_file = metrics_file
        self.metrics = []

    def collect_metrics(self):
        """
        Collect system performance metrics.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            network_info = psutil.net_io_counters()

            metric = {
                "timestamp": datetime.now().isoformat(),
                "cpu_usage": cpu_usage,
                "memory_usage": memory_info.percent,
                "disk_usage": disk_usage.percent,
                "network_sent": network_info.bytes_sent,
                "network_received": network_info.bytes_recv
            }
            self.metrics.append(metric)
            print(f"Metrics collected at {metric['timestamp']}")
        except Exception as e:
            print(f"Error occurred while collecting metrics: {e}")

    def save_metrics(self):
        """
        Save the collected metrics to a JSON file.
        """
        try:
            with open(self.metrics_file, 'w') as file:
                json.dump(self.metrics, file, indent=4)
            print(f"Metrics successfully saved to {self.metrics_file}")
        except Exception as e:
            print(f"Error occurred while saving metrics: {e}")

    def load_metrics(self):
        """
        Load metrics from a JSON file.
        
        :param file_path: Path to the file from which the metrics will be loaded.
        """
        try:
            with open(self.metrics_file, 'r') as file:
                self.metrics = json.load(file)
            print(f"Metrics successfully loaded from {self.metrics_file}")
        except Exception as e:
            print(f"Error occurred while loading metrics: {e}")

    def print_summary(self):
        """
        Print a summary of the collected metrics.
        """
        print("Performance Metrics Summary:")
        for i, metric in enumerate(self.metrics):
            print(f"Metric {i + 1}: {metric['timestamp']} - CPU: {metric['cpu_usage']}%, Memory: {metric['memory_usage']}%, Disk: {metric['disk_usage']}%, Network Sent: {metric['network_sent']} bytes, Network Received: {metric['network_received']} bytes")

if __name__ == "__main__":
    metrics_file_path = 'performance_metrics.json'

    monitor = PerformanceMonitor(metrics_file_path)
    monitor.collect_metrics()
    monitor.save_metrics()
    monitor.print_summary()
