#! /usr/bin/env python3
# Ping Client

from socket import *
from time import *
from struct import *
from random import *
import sys

def clientUDP(serverIP, serverPort):
    packetsSent = 0
    packetsRcvd = 0
    rtts = []
    clientsocket = socket(AF_INET, SOCK_DGRAM)
    print("Pinging " + serverIP + ":" + str(serverPort) + " --")
    for i in range(10):
        clientsocket.settimeout(None)
        #time elapsed
        sent = perf_counter()
        clientsocket.sendto(pack("II",1,i+1), (serverIP, serverPort))
        packetsSent += 1
        clientsocket.settimeout(1)
        while True:
            try:
                data, address = clientsocket.recvfrom(serverPort)
            except timeout:
                print("Ping message number " + str(i+1) + " timed out")
                break
            if data is not None:
                recvd = perf_counter()
                print("Ping message number " + str(i+1) + " RTT: %.6f secs" % (recvd-sent))
                packetsRcvd += 1
                rtts.append(recvd-sent)
                break
    clientsocket.close()
    print('\n')
    print("Packets transmitted: " + str(packetsSent))
    print("Packets received: " + str(packetsRcvd))
    print("Packets lost: " + str(packetsSent-packetsRcvd))
    print("Packet loss rate: %.6f%%" % ((1-packetsRcvd/packetsSent)*100)) 
    minRtt = rtts[0]
    maxRtt = rtts[0]
    averageRtt = 0
    for trip in rtts:
        if trip < minRtt:
            minRtt = trip
        if trip > maxRtt:
            maxRtt = trip
        averageRtt += trip
    averageRtt = averageRtt/packetsRcvd
    print("Minimum RTT: %.6f secs" % minRtt)
    print("Maximum RTT: %.6f secs" % maxRtt)
    print("Average RTT: %.6f secs" % averageRtt)

host = sys.argv[1]
port = int(sys.argv[2])
clientUDP(host, port)
