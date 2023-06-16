from . import ProtocolParser
from .database_handling.bases import PacketEntry


from scapy.all import *
import http.client


class HTTPParser(ProtocolParser):
    def parse(cls, packet) -> str:
        payload = packet[Raw].load
        payload_str = payload.decode('utf-8')

        header_end = payload_str.find('\r\n\r\n')
        header = payload_str[:header_end]
        body = payload_str[header_end + 4:]

        headers = http.client.parse_headers(header.split('\r\n')[1:])

        s = ""
        for key, value in headers.items():
            s += f"{key}: {value}\n"
        s += f"\n{body}"

        return s

    def can_parse(cls, packet) -> bool:
        methods = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE',
                   'CONNECT', 'OPTIONS', 'TRACE']
        if packet.haslayer(TCP):
            if packet.haslayer(Raw):  # Checks if packet has payload
                raw = packet[Raw].load
                for method in methods:  # Checks if any of the http methods are present in load
                    if method.encode() in raw:
                        return True

        return False


class IPv4Parser(ProtocolParser):
    def parse(cls, packet) -> str:
        ip_layer = packet[IP]
        return f"IP Header Length: {ip_layer.ihl * 4}\n" \
            f"TOS: {ip_layer.tos}\n" \
            f"Length: {ip_layer.len}\n" \
            f"ID: {ip_layer.id}\n" \
            f"Flags: {ip_layer.flags}\n" \
            f"Fragment Offset: {ip_layer.frag}\n" \
            f"TTL: {ip_layer.ttl}\n" \
            f"Protocol: {ip_layer.proto}\n" \
            f"Source Address: {ip_layer.src}\n" \
            f"Destination Address: {ip_layer.dst}\n"

    def can_parse(cls, packet: PacketEntry) -> bool:
        return IP in packet


class IPv6Parser(ProtocolParser):
    def parse(cls, packet) -> str:
        ip_layer = packet[IPv6]
        return f"Traffic Class: {ip_layer.tc}\n" \
            f"Flow Label: {ip_layer.fl}\n" \
            f"Payload Length: {ip_layer.plen}\n" \
            f"Next Header: {ip_layer.nh}\n" \
            f"Hop Limit: {ip_layer.hlim}\n" \
            f"Source Address: {ip_layer.src}\n" \
            f"Destination Address: {ip_layer.dst}\n"

    def can_parse(cls, packet) -> bool:
        return IPv6 in packet


class TCPParser(ProtocolParser):
    def parse(cls, packet) -> str:
        s = ""
        tcp_layer = packet[TCP]
        for field in tcp_layer.fields_desc:
            field_name = field.name
            field_value = tcp_layer.getfieldval(field_name)
            s += f"{field_name}: {field_value}\n"

        return s

    def can_parse(cls, packet) -> bool:
        return TCP in packet


class UDPParser(ProtocolParser):
    def parse(cls, packet) -> str:
        s = ""
        udp_layer = packet[UDP]
        for field in udp_layer.fields_desc:
            field_name = field.name
            field_value = udp_layer.getfieldval(field_name)
            s += f"{field_name}: {field_value}\n"

        return s

    def can_parse(cls, packet) -> bool:
        return UDP in packet


class EthernetParser(ProtocolParser):
    def parse(cls, packet) -> str:
        s = ""
        for field in packet.fields_desc:
            field_name = field.name
            field_value = packet.getfieldval(field_name)
            s += f"{field_name}: {field_value}\n"

        return s

    def can_parse(cls, packet) -> bool:
        return Ether in packet
