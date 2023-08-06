"""Top-level package for Driver PCAP parser."""

__author__ = """Andres Kepler"""
__email__ = 'andres.kepler@fleetcomplete.com'
__version__ = '0.1.4'

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
                 terminal_type=None,
                 src_ip=None, dst_ip=None,
                 tcp_sport=None, tcp_dport=None,
                 src_mac=None, dst_mac=None,
                 time=None):
        self.serial = serial
        self.terminal_type = terminal_type
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.time = time

    def __dict__(self):
        return dict(serial=self.serial,
                    terminal_type=self.terminal_type,
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


def get_vt10_serial(packet):
    try:
        serial = struct.unpack_from(">16s", bytes(packet), offset=54)[0].decode('utf8')
    except Exception:
        return None
    if "," in serial:
        serial = serial.split(",")[0]
    else:
        return None
    return str(serial)


def get_ruptela_serial(packet):
    try:
        data = b''.join(struct.unpack_from('>8c', bytes(packet), offset=68))
        serial = str(int.from_bytes(data, byteorder='big'))
    except Exception:
        return None
    if len(serial) > 15:
        return None
    return serial


def get_teltonika_serial(packet):
    try:
        serial_length = struct.unpack_from('>b', bytes(packet), offset=67)[0]
        if len(packet) > 100:
            return None
        if serial_length < 15:
            return None
        fmt = ">{}s".format(str(serial_length))
        serial = struct.unpack_from(fmt, bytes(packet), offset=68)[0].decode('utf8')
    except Exception as e:
        return None
    return serial


def parse_file(args):
    serial_collector = []
    packets = rdpcap(args.filename)
    myip = args.filter_dst_ip
    if myip:
        packets = packets.filter(lambda x: x.payload.dst == myip)
    # Let's iterate through every filtered packet
    for packet in packets:
        packet_summ = packet_summary(packet)
        t_serial = get_teltonika_serial(packet)
        r_serial = get_ruptela_serial(packet)
        v_serial = get_vt10_serial(packet)

        if t_serial:
            terminal_type = "Teltonika"
            serial = t_serial
        elif r_serial:
            terminal_type = "Ruptela"
            serial = r_serial
        elif v_serial:
            terminal_type = "VT10"
            serial = v_serial
        else:
            terminal_type = "Unknown"
            serial = "Unknown"

        if serial == "Unknown" or (len(serial) < 15 or len(serial) > 15):
            continue

        payload = DataOut(serial,
                          terminal_type,
                          *packet_summ
                          )
        if serial not in serial_collector:
            serial_collector.append(serial)
            print(payload)

    return 0
