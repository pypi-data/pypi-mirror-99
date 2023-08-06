"""Console script for driver_pcap_parser."""
import argparse
import sys
from driver_pcap_parser import parse_file


def parse_args():
    """Console script for driver_pcap_parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', required=True)
    parser.add_argument('-m', '--filter_dst_ip')
    parser.add_argument('-L', '--logstash')
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    return parser.parse_args()


def main():
    return parse_file(parse_args())


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
