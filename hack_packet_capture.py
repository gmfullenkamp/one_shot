from scapy.all import sniff
import time
import pyshark
from multiprocessing import Process
import tensorflow as tf
from pymongo import MongoClient
import networkx
from tqdm import tqdm

"""SET UP"""
# Install wireshark https://www.wireshark.org/download.html
# Install docker https://docs.docker.com/get-docker/
# Install mongosh msi https://www.mongodb.com/try/download/community and run
# Follow https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/ and run

"""CONSTANTS"""
MONGO_URI = "localhost:27017"
# Pyshark packets
PYSHARK_DATABASE = "pyshark"
PYSHARK_COLLECTION = "packet_capture"
# Scapy packets
SCAPY_DATABASE = "scapy"
SCAPY_COLLECTION = "packet_capture"


class PysharkPacketCapture:
    def __init__(self, mongo_uri: str, database: str, collection: str, interface: str = "Wi-Fi"):
        self.mongo_uri = mongo_uri
        self.database = database
        self.collection = collection
        self.interface = interface

    @staticmethod
    def packet_to_dict(pyshark_packet):
        packet_dict = {}
        for layer in pyshark_packet.layers:
            layer_name = layer.layer_name.lower()
            if hasattr(layer, "_all_fields"):
                packet_dict[layer_name] = layer._all_fields
            else:
                packet_dict[layer_name] = {}
        return packet_dict

    def capture_packets(self):
        client = MongoClient(self.mongo_uri)
        database = client[self.database]
        collection = database[self.collection]
        capture = pyshark.LiveCapture(interface=self.interface)
        for packet in capture.sniff_continuously(packet_count=None):
            packet_dict = self.packet_to_dict(packet)
            collection.insert_one(packet_dict)
        client.close()


class ScapyPacketCapture:
    def __init__(self, mongo_uri: str, database: str, collection: str):
        self.mongo_uri = mongo_uri
        self.database = database
        self.collection = collection

    @staticmethod
    def packet_to_dict(scapy_packet):
        packet_dict = {}
        for line in scapy_packet.show2(dump=True).split("\n"):
            if "###" in line:
                layer = line.strip("#[] ")
                packet_dict[layer] = {}
            elif "=" in line:
                key, val = line.split("=", 1)
                packet_dict[layer][key.strip()] = val.strip()
        return packet_dict

    def capture_packets(self):
        client = MongoClient(self.mongo_uri)
        database = client[self.database]
        collection = database[self.collection]
        while True:
            for packet in sniff(count=100):
                packet_dict = self.packet_to_dict(packet)
                collection.insert_one(packet_dict)


class GraphGenerator(tf.keras.utils.Sequence):
    def __init__(self, mongo_uri: str, pyshark_database: str, pyshark_collection: str, scapy_database: str,
                 scapy_collection: str):
        self.mongo_uri = mongo_uri
        self.pyshark_database = pyshark_database
        self.pyshark_collection = pyshark_collection
        self.scapy_database = scapy_database
        self.scapy_collection = scapy_collection

        self.graph = networkx.Graph()
        self.ip_hash = []

    def lookup_or_insert(self, ip_address):
        if ip_address not in self.ip_hash:
            self.ip_hash.append(ip_address)
        return self.ip_hash.index(ip_address)

    def update_graph(self):
        # Load and delete pyshark packet data from mongodb
        client = MongoClient(self.mongo_uri)
        pyshark_database = client[self.pyshark_database]
        pyshark_collection = pyshark_database[self.pyshark_collection]
        pyshark_cursor = pyshark_collection.find({})
        for log in tqdm(pyshark_cursor, desc="Adding Pyshark Packet Capture to Graph"):
            if "ip" in log.keys():
                chosen_keys = ["ip.host", "ip.dst"]
                if all([key in log["ip"].keys() for key in chosen_keys]):
                    host_node = self.lookup_or_insert(str(log["ip"]["ip.host"]))
                    dst_node = self.lookup_or_insert(str(log["ip"]["ip.dst"]))
                    self.graph.add_edge(host_node, dst_node, weight=1)
            elif "ipv6" in log.keys():
                chosen_keys = ["ipv6.host", "ipv6.dst"]
                if all([key in log["ipv6"].keys() for key in chosen_keys]):
                    host_node = self.lookup_or_insert(str(log["ipv6"]["ipv6.host"]))
                    dst_node = self.lookup_or_insert(str(log["ipv6"]["ipv6.dst"]))
                    self.graph.add_edge(host_node, dst_node, weight=1)
        x = pyshark_collection.delete_many({})
        print(x.deleted_count, " Pyshark Packets deleted.")
        # Load and delete scapy packet data from mongodb
        client = MongoClient(self.mongo_uri)
        scapy_database = client[self.scapy_database]
        scapy_collection = scapy_database[self.scapy_collection]
        scapy_cursor = scapy_collection.find({})
        for log in tqdm(scapy_cursor, desc="Adding Scapy Packet Capture to Graph"):
            if "IP" in log.keys():
                chosen_keys = ["src", "dst"]
                if all([key in log["IP"].keys() for key in chosen_keys]):
                    host_node = self.lookup_or_insert(str(log["IP"]["src"]))
                    dst_node = self.lookup_or_insert(str(log["IP"]["dst"]))
                    self.graph.add_edge(host_node, dst_node, weight=1)
            if "IPv6" in log.keys():
                chosen_keys = ["src", "dst"]
                if all([key in log["IPv6"].keys() for key in chosen_keys]):
                    host_node = self.lookup_or_insert(str(log["IPv6"]["src"]))
                    dst_node = self.lookup_or_insert(str(log["IPv6"]["dst"]))
                    self.graph.add_edge(host_node, dst_node, weight=1)
        x = scapy_collection.delete_many({})
        print(x.deleted_count, " Scapy Packets deleted.")
        print(f"Nodes: {self.graph.number_of_nodes()}, Edges: {self.graph.number_of_edges()}")

    def on_epoch_end(self):
        self.update_graph()


def main():
    # Create processes for packet capture
    caps1 = PysharkPacketCapture(mongo_uri=MONGO_URI, database=PYSHARK_DATABASE, collection=PYSHARK_COLLECTION)
    proc1 = Process(target=caps1.capture_packets)
    proc1.start()
    caps2 = ScapyPacketCapture(mongo_uri=MONGO_URI, database=SCAPY_DATABASE, collection=SCAPY_COLLECTION)
    proc2 = Process(target=caps2.capture_packets)
    proc2.start()
    time.sleep(10)

    # Generator boi
    generator = GraphGenerator(mongo_uri=MONGO_URI, pyshark_database=PYSHARK_DATABASE,
                               pyshark_collection=PYSHARK_COLLECTION, scapy_database=SCAPY_DATABASE,
                               scapy_collection=SCAPY_COLLECTION)

    # Fake online training
    while True:
        generator.on_epoch_end()
        time.sleep(10)


if __name__ == "__main__":
    main()
