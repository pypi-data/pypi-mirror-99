==================
Driver PCAP parser
==================


.. image:: https://img.shields.io/pypi/v/driver_pcap_parser.svg
        :target: https://pypi.python.org/pypi/driver_pcap_parser

.. image:: https://img.shields.io/travis/andrke/driver_pcap_parser.svg
        :target: https://travis-ci.com/andrke/driver_pcap_parser

.. image:: https://readthedocs.org/projects/driver-pcap-parser/badge/?version=latest
        :target: https://driver-pcap-parser.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Python PCAP file parser for Teltonika drivers


* Free software: MIT license
* Documentation: https://driver-pcap-parser.readthedocs.io.


Features
--------

* Parses PCAP file and detects TELTONIKA serial number
* Add Ruptela serial number parser
* Add VT10 serial number parser

Usage
--------

.. code-block::

   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip install driver_pcap_parser
   $ sudo timeout 60s tcpdump -i eth0 -G 60 'dst port 123 and dst host 1.2.3.4' -w '/tmp/log.pcap'
   $ driver_pcap_parser -f /tmp/log.pcap

   {'serial': '123', 'src_ip': '1.1.1.1', 'dst_ip': '1.1.1.2', 'tcp_sport': 37767, 'tcp_dport': 21300, 'src_mac': 'a1:b2:c3:d4:e5:f6', 'dst_mac': 'a1:b2:c3:d4:e5:f7', 'time': Decimal('1616154926.586344')}
   {'serial': '112', 'src_ip': '1.1.1.1', 'dst_ip': '1.1.1.2', 'tcp_sport': 32287, 'tcp_dport': 21300, 'src_mac': 'a1:b2:c3:d4:e5:f6', 'dst_mac': 'a1:b2:c3:d4:e5:f7', 'time': Decimal('1616154926.612047')}
   {'serial': '111', 'src_ip': '1.1.1.1', 'dst_ip': '1.1.1.2', 'tcp_sport': 18308, 'tcp_dport': 21300, 'src_mac': 'a1:b2:c3:d4:e5:f6', 'dst_mac': 'a1:b2:c3:d4:e5:f7', 'time': Decimal('1616154926.660903')}

Credits
-------

This packge was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
