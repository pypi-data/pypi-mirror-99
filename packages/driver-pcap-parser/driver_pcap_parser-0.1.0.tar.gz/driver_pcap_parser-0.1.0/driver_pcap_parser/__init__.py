"""Top-level package for Driver PCAP parser."""

__author__ = """Andres Kepler"""
__email__ = 'andres.kepler@fleetcomplete.com'
__version__ = '0.1.0'

from scapy.all import *
import struct


def parse_file(args):
    packets = rdpcap(args.filename)
    myip = args.filter_dst_ip
    if myip:
        packets = packets.filter(lambda x: x.payload.dst == myip)
    # Let's iterate through every filtered packet
    for packet in packets:
        if len(packet) > 100:
            continue
        try:
            serial = struct.unpack_from('>15s', bytes(packet), offset=68)[0].decode('utf8')
            print(f'Found serial {serial}')
        except struct.error:
            pass
    return 0
