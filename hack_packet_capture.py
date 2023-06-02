import time
import pyshark
from tqdm import tqdm
from multiprocessing import Process
import tensorflow as tf
import networkx
import json
import os


class PacketCapture(tf.keras.utils.Sequence):
    interface = "Wi-Fi"
    packets = {"packets": []}
    update_freq = 3000
    packet_json_file = "packets.json"

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
        capture = pyshark.LiveCapture(interface=self.interface)
        for i, pyshark_packet in tqdm(enumerate(capture.sniff_continuously(packet_count=None)),
                                      desc="Capturing packets"):
            packet_dict = self.packet_to_dict(pyshark_packet)
            self.packets["packets"].append(packet_dict)
            if not i % self.update_freq:
                if os.path.exists(self.packet_json_file):
                    os.remove(self.packet_json_file)
                with open(self.packet_json_file, "w") as outfile:
                    json.dump(self.packets, outfile)
                outfile.close()


class GraphGenerator(tf.keras.utils.Sequence):
    packet_json_file = "packets.json"
    ip_lookup = {}

    def generate_unweighted_graph(self):
        graph = networkx.Graph()
        # TODO: Load in MongoDB dataset instead of an updated packets.json file
        with open(self.packet_json_file, "r") as infile:
            packets = json.load(infile)["packets"]
        infile.close()
        for packet in packets:
            # TODO: Calculate edge probability for weight
            if "ip" in packet.keys() \
                    and "ip.host" in packet["ip"].keys() \
                    and "ip.dst" in packet["ip"].keys():
                graph.add_edge(packet["ip"]["ip.host"], packet["ip"]["ip.dst"], weight=1)
            elif "ipv6" in packet.keys() \
                    and "ipv6.host" in packet["ipv6"].keys() \
                    and "ipv6.dst" in packet["ipv6"].keys():
                graph.add_edge(packet["ipv6"]["ipv6.host"], packet["ipv6"]["ipv6.dst"], weight=1)
        print("Total number of graph nodes:", graph.number_of_nodes())
        print("Total number of graph edges:", graph.number_of_edges())
        return graph


def main():
    # Create process for packet capture
    caps = PacketCapture()
    proc_one = Process(target=caps.capture_packets)
    proc_one.start()
    time.sleep(30)

    # Generator boi
    generator = GraphGenerator()
    graph = generator.generate_unweighted_graph()


if __name__ == "__main__":
    main()
