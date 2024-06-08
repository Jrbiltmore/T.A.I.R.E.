"""
packet_sniffer.py

This module is responsible for sniffing network packets to monitor and analyze network traffic. 
It integrates various techniques to capture and process packets for detailed analysis.

Author: Jacob Thomas, Mr. Redmond
Version: 0.1.0
"""

import json
import os
from datetime import datetime
from scapy.all import sniff, PcapWriter

class PacketSniffer:
    def __init__(self, config_file):
        """
        Initialize the PacketSniffer with a configuration file.
        
        :param config_file: Path to the JSON file containing sniffer configurations.
        """
        self.config_file = config_file
        self.config = self.load_config()
        self.packets = []

    def load_config(self):
        """
        Load sniffer configurations from the provided JSON file.
        
        :return: Sniffer configurations.
        """
        try:
            with open(self.config_file, 'r') as file:
                config = json.load(file)
                return config
        except Exception as e:
            print(f"Error occurred while loading configurations: {e}")
            return {}

    def start_sniffing(self):
        """
        Start sniffing network packets based on the loaded configurations.
        """
        try:
            interface = self.config.get("interface", "eth0")
            filter = self.config.get("filter", "tcp")
            duration = self.config.get("duration", 60)
            print(f"Starting packet sniffing on interface {interface} with filter '{filter}' for {duration} seconds.")
            packets = sniff(iface=interface, filter=filter, timeout=duration)
            self.packets.extend(packets)
            print("Packet sniffing completed successfully.")
        except Exception as e:
            print(f"Error occurred while sniffing packets: {e}")

    def save_packets(self, file_path):
        """
        Save the sniffed packets to a pcap file.
        
        :param file_path: Path to the file where the packets will be saved.
        """
        try:
            writer = PcapWriter(file_path, append=True, sync=True)
            writer.write(self.packets)
            writer.close()
            print(f"Packets successfully saved to {file_path}")
        except Exception as e:
            print(f"Error occurred while saving packets: {e}")

    def load_packets(self, file_path):
        """
        Load packets from a pcap file.
        
        :param file_path: Path to the file from which the packets will be loaded.
        """
        try:
            from scapy.utils import rdpcap
            self.packets = rdpcap(file_path)
            print(f"Packets successfully loaded from {file_path}")
        except Exception as e:
            print(f"Error occurred while loading packets: {e}")

    def print_summary(self):
        """
        Print a summary of the sniffed packets.
        """
        print(f"Total packets sniffed: {len(self.packets)}")
        for i, packet in enumerate(self.packets[:10], start=1):  # Print the first 10 packets
            print(f"Packet {i}: {packet.summary()}")

if __name__ == "__main__":
    config_file_path = 'sniffer_config.json'
    packets_file_path = 'sniffed_packets.pcap'

    # Ensure sniffer_config.json exists
    if not os.path.exists(config_file_path):
        print(f"{config_file_path} not found. Creating default configurations file.")
        default_config = {
            "interface": "eth0",
            "filter": "tcp",
            "duration": 60
        }
        with open(config_file_path, 'w') as file:
            json.dump(default_config, file, indent=4)

    sniffer = PacketSniffer(config_file_path)
    sniffer.start_sniffing()
    sniffer.save_packets(packets_file_path)
    sniffer.print_summary()
