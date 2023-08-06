"""Top-level package for Driver PCAP parser."""

__author__ = """Andres Kepler"""
__email__ = 'andres.kepler@fleetcomplete.com'
__version__ = '0.1.2'

from scapy.all import *
import struct


def packet_summary(pkt):
    ip_src = None
    ip_dst = None
    tcp_sport = None
    tcp_dport = None
    if IP in pkt:
        ip_src = pkt[IP].src
        ip_dst = pkt[IP].dst
    if TCP in pkt:
        tcp_sport = pkt[TCP].sport
        tcp_dport = pkt[TCP].dport
    return ip_src, ip_dst, tcp_sport, tcp_dport, pkt.src, pkt.dst, pkt.time


class DataOut(object):
    def __init__(self, serial,
                 src_ip=None, dst_ip=None,
                 tcp_sport=None, tcp_dport=None,
                 src_mac=None, dst_mac=None,
                 time=None):
        self.serial = serial
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.time = time

    def __dict__(self):
        return dict(serial=self.serial,
                    src_ip=self.src_ip,
                    dst_ip=self.dst_ip,
                    tcp_sport=self.tcp_sport,
                    tcp_dport=self.tcp_dport,
                    src_mac=self.src_mac,
                    dst_mac=self.dst_mac,
                    time=self.time
                    )

    def __repr__(self):
        return str(self.__dict__())


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
            packet_summ = packet_summary(packet)
            serial_lenght = struct.unpack_from('>b', bytes(packet), offset=67)[0]
            if serial_lenght < 15:
                continue
            fmt = ">{}s".format(str(serial_lenght))
            serial = struct.unpack_from(fmt, bytes(packet), offset=68)[0].decode('utf8')
            payload = DataOut(serial,
                              *packet_summ
                              )
            print(payload)
        except struct.error:
            pass
        except UnicodeDecodeError:
            pass
    return 0
