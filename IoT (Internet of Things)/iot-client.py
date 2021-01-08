#! /usr/bin/env python3
# IOT Client

from socket import *
from time import *
from struct import *
from random import *
import sys
import struct

def clientIOT(serverIP, serverPort, func, color):

    clientsocket = socket(AF_INET, SOCK_DGRAM)
    print("Sending Request to " + serverIP + ", " + str(serverPort) + ":")

    messageType = 1
    functionNum = func
    messageID = randint(1,100)
    colorNum = color
    errorCode = 0

    print("Message Type: " + str(messageType))
    print("Function Number: " + str(functionNum))
    print("Message ID: " + str(messageID))
    print("Color Number: " + str(colorNum))
    print("\n")
    
    clientsocket.settimeout(1)
    att = 0
    while att < 3:
        try:
            
            # Sending data
            msg = struct.pack("!hhih",messageType,functionNum,messageID,colorNum)
            clientsocket.sendto(msg,(serverIP, serverPort))

            # Getting  response
            msg,address = clientsocket.recvfrom(1024)

            # Alg for length
            #length = (len(msg) - (struct.calcsize("!hhihh") + questionLength))

            message = struct.unpack("!hhihhh" , msg)
            #message = struct.unpack("!hhihh" + str(questionLength) + "s" + str(length) + "s" , msg)

            # New values after unpack
            messageType = message[0]
            errorCode = message[1]
            messageID = message[2]
            funcNum = message[3]
            lightStatus = message[4]
            colorNum = message[5]

            # Response
            print("Received response from " + str(serverIP) + ", " + str(serverPort))
        
            print("Message Type: " + str(messageType))
            print("Error Code: " + str(errorCode))
            print("Message Identifier: " + str(messageID))
            print("Function Number: " + str(funcNum))
            print("Light Status: " + str(lightStatus))
            print("Color Number " + str(colorNum))
            
            break
            exit(0)
        
        except:            
            print("Request timed out ....")
            if att == 2:
                print("Exiting Program")
        att+=1
            
    clientsocket.close()
    
# Command Line Arguments
host = sys.argv[1]      #IP
port = int(sys.argv[2]) #Port
func = int(sys.argv[3])   #function number
    
if len(sys.argv) < 5:
    color = 1 #default color
else:
    color = int(sys.argv[4])  #color number
        
clientIOT(host, port, func, color)
