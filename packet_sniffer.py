from scapy.all import *

capture = sniff(prn=lambda x: x.summary(), filter="tcp")
