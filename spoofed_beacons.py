"""
This script allows you to create fake wifi networks and view them on LINUX.

http://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/scapy_wifi/scapy_tut.html

Must install wireshark in order for winpcap to be installed correctly.
Command: "airmon-ng start wlan0"
"""
from scapy.all import sendp
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap

SSIDS = ["hello", "there", "general", "kenobi"]
IFACE = "mon0"
BROADCAST = "ff:ff:ff:ff:ff:ff"
BSSID = "aa:aa:aa:aa:aa:aa"

# TODO: Works on linux machines but not windows :'(
frames = []
for netSSID in SSIDS:
    print(netSSID)
    dot11 = Dot11(addr1=BROADCAST, addr2=BSSID, addr3=BSSID)
    beacon = Dot11Beacon(cap="ESS")
    essid = Dot11Elt(ID=0, info=netSSID)
    rsn = Dot11Elt(ID=1, info="\x82\x84\x8b\x96\x24\x30\x48\x6c")
    dsp = Dot11Elt(ID=3, info="\x0b")
    tim = Dot11Elt(ID=5, info="\x00\x01\x00\x00")

    frame = RadioTap() / dot11 / beacon / essid / rsn / dsp / tim
    print("SSID=%-20s   %r" % (netSSID, frame))
    frames.append(frame)
sendp(frames, iface=IFACE, inter=0.1, loop=1)
