"""
Must install wireshark in order for winpcap to be installed correctly.
"""
from scapy.all import sniff

COUNT = 999999

queries = []


# Gets query specific packets
def get_queries(p: str):
    try:
        qry = p.payload.payload.payload.raw_packet_cache_fields["qd"].fields["qname"]
        if qry not in queries:
            queries.append(qry)
            print("\t", qry)
    except:
        pass


# TODO: Get this query packet sniffing working outside the running machine
#  youtube iPhone and Android WiFi Man-in-the-middle attack // PYTHON Scapy scripts for attacking networks
print("Sniffed queries:")
capture = sniff(prn=lambda x: get_queries(x), count=COUNT)
