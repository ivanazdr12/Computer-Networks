#! /usr/bin/env python3
# Ping Server

from socket import *
from struct import *
from random import *
import sys

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(serverPort)
    if randint(1,9) < 4:
            print("Message with sequence number " + str(unpack("II", data)[1]) + " dropped")
            continue
    else:
        print("Responding to ping request with sequence number " + str(unpack("II", data)[1]))
        serverSocket.sendto(pack("II", 2, unpack("II", data)[1]), address)

