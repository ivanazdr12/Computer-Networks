#! /usr/bin/env python3
# HTTP Server

from socket import *
from datetime import datetime, time
from sys import argv
from os import path
from re import match
import codecs
import time

ip = argv[1] 
port = int(argv[2])

# create server TCP socket
server = socket(AF_INET, SOCK_STREAM)

# avoid bind() exception: OSError:
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

try:
    server.bind((ip, port))
    server.listen(1)
    print("Server listening on http://%s:%d" % (ip, port))
except Exception as exc:
    print("Caught exception error : %s" % exc)
    exit(1)

def GetContentData(fileName):
    structureContent = ''
    f = codecs.open("filename.html", 'r', encoding='utf-8')
    data = f.read()
    for line in data.splitlines():
        if '<p class="p1">' in line:
            structureContent += line
    
    structureContent = structureContent.replace('<p class="p1">', '')
    structureContent = structureContent.replace('<span class="s1">', '')
    structureContent = structureContent.replace('</span>', '')
    structureContent = structureContent.replace('</p>','')
    structureContent = structureContent.replace('&lt;','<')
    structureContent = structureContent.replace('&gt;','>')

    return structureContent

while True:
    try:
        # accepting incoming connection requests
        connection, address = server.accept()

        dataLen = 1000000
        headers = str(connection.recv(dataLen).decode()).splitlines()

        fileName = ""
        mod_time = False

        for header in headers:
            # getting filename from request
            if match(r"GET .+ HTTP/1.1", header):
                fileName = match(r"GET (.+) HTTP/1.1", header).groups()[0]
                
            # getting modified time from request
            if match(r"If-Modified-Since: (.+)", header):
                mod_time = match(r"If-Modified-Since: (.+) GMT", header).groups()[0]
                mod_time = datetime.strptime(mod_time, "%a, %d %b %Y %H:%M:%S")

        # https://www.geeksforgeeks.org/python-os-path-realpath-method/
        filePath: str = path.dirname(path.realpath(__file__)) + fileName
        responseMessage = ""
        responseContent = b""

        # current time
        t = time.gmtime(time.time())
        date = (time.strftime("%a, %d %b %Y %H:%M:%S GMT", t))
        
        try:
            responseContent = GetContentData(filePath)
            ContentLength = str(len(responseContent))

            # get time file was last modified
            last_mod_time = path.getmtime(filePath)
            last_mod_time = datetime.utcfromtimestamp(last_mod_time).replace(microsecond=0)

            # HTTP 200 Response
            responseMessage = "HTTP/1.1 200 OK" + "\r\n"
            responseMessage += "Date: " + date + "\r\n" 
            responseMessage += "Last-Modified: " + last_mod_time.strftime(
                "%a, %d %b %Y %H:%M:%S GMT"
            ) + "\r\n"
            responseMessage += "Content-Length: " + ContentLength + "\r\n"
            responseMessage += "Content-Type: text/html; charset=UTF-8\r\n"
            responseMessage += "\r\n"
            responseMessage +=  responseContent
            
            if mod_time:
                if last_mod_time <= mod_time:
                    responseMessage = "HTTP/1.1 304 Not Modified\r\n"
                    responseMessage += "Date: " + date + "\r\n"
                    responseMessage += "\r\n"

        except:
            # file not exist
            responseContent: bytes = b""
            ContentLength = str(len(responseContent))
            responseMessage: str = "HTTP/1.1 404 Not Found\r\n"
            responseMessage += "Date: " + date + "\r\n"
            responseMessage += "Content-Length: " + ContentLength + "\r\n"
            responseMessage += "\r\n"

        connection.send(responseMessage.encode())
        print("Response sent!")
        connection.close()

    except:
        server.close()
        break
