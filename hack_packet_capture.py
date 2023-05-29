import pyshark

capture = pyshark.LiveCapture()
for packet in capture.sniff_continuously(packet_count=None):
    [print(layer) for layer in packet.layers]
