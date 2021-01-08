#! /usr/bin/env python3
# IOT Server

from socket import *
from struct import *
from random import *
import sys
import struct

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign server IP address and port number to the socket
serverSocket.bind((serverIP, serverPort))

# Define msg type
messageType = 2

# MessageID list for tracking duplicates
# Func and colors list for appending to return status 
messageIDS = []
funcNumList = []
colorsNumList = []

def checkIfDuplicates(lst):
    if len(lst) == len(set(lst)):
        return False
    else:
        lst = lst.pop()
        return True
    
print("The server is ready to receive on port:  " + str(serverPort) + "\n")
    
# loop forever listening for incoming UDP messages
while True:
    colorsDict = {
        1: "Blue",
        2: "Green",
        3: "Cyan",
        4: "Red",
        5: "Magenta",
        6: "Yellow",
        7: "White",  
    }
    
    # Receive and print the client data from the "data" socket
    data, address = serverSocket.recvfrom(1024)   
    message = struct.unpack("!hhih", data)

    funcNum = message[1]
    messageID = message[2]
    colorNum = message[3]
    
    funcList = [1,2,3,4]
    
    messageIDS.append(str(messageID))
    funcNumList.append(str(funcNum))
    if colorNum in colorsDict:
        colorsNumList.append(str(colorNum))
    
# handle error cases
# return light status

    #when error occurs, light turns off
    dup = checkIfDuplicates(messageIDS)     #when duplicate messageID (bulb not functioning error) 
    if dup:
        errorCode = 1
        lightStatus = 0
        if colorsNumsList:
            del colorsNumList[-1]
    elif colorNum not in colorsDict:        #if color not supported (color error)
        errorCode = 2
        lightStatus = 0
        if colorsNumList:
            del colorsNumList[-1]
    elif funcNum not in funcList:       #if funcNum not supported (format error)
        errorCode = 3
        lightStatus = 0
        if colorsNumList:
            del colorsNumList[-1]
    else:
        
        if funcNum == 1 or funcNum == 2:    #to set color or change color
            lightStatus = 1
            errorCode = 0
        elif funcNum == 3:      #to get status

            #if last element in list is to set color or change color, status is ON
            for x in range(len(funcNumList)-1,-1,-1):
                if funcNumList[x] == str(1) or funcNumList[x] == str(2):
                    lightStatus = 1
                    errorCode = 0
                    break

                #if last element in list is set to turn off, status is OFF
                elif funcNumList[x] == str(4):
                    lightStatus = 0
                    errorCode = 0
                    break

                else:
                    errorCode = 3
                    
            #if list is empty and a get status is requested (bulb not functioning error)
            del colorsNumList[-1]
            if not colorsNumList:
                errorCode = 1
                lightStatus = 0

            #get the color from last element 
            else:
                colorNum = int(colorsNumList[-1])
                errorCode = 0

        #if light request to turn off, status is OFF    
        elif funcNum == 4:
            lightStatus = 0
            errorCode = 0
            if colorsNumList:
                del colorsNumList[-1]

    data = struct.pack("!hhihhh", messageType, errorCode, messageID, funcNum, lightStatus, colorNum)
    
    serverSocket.sendto(data,address)
