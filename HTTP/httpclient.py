#! /usr/bin/env python3
# HTTP Client

from socket import *
from datetime import datetime, time
from sys import argv
from os import path
from re import match

# cache file and write content
def cacheFile(contents):
    cachedFile = open("cache.txt", "w")
    cachedFile.write(contents)
    cachedFile.close()

if len(argv) < 2:
    print("Please enter a URL")
    exit(1)
    
# https://www.guru99.com/python-regular-expressions-complete-tutorial.html
url = match(r"(.+):([0-9]+)(/.+)?", argv[1])

host = url.group(1)
port = int(url.group(2))
fileName = url.group(3)

if not url.group(3):
    print("Invalid filename")
    exit(1)

# create TCP client socket
client = socket(AF_INET, SOCK_STREAM)

# create TCP connection to server
client.connect((host, port))

# check if file is already cached
# https://www.geeksforgeeks.org/python-os-path-realpath-method/
filePath = path.dirname(path.realpath(__file__)) + "/cache.txt"
isCached = path.isfile(filePath)

# get request
requestMessage = "GET " + fileName + " HTTP/1.1\r\n"
requestMessage += "Host: " + host + ":" + str(port) + "\r\n"

# conditional get request
if isCached:
    mod_time = path.getmtime(filePath)
    mod_time = datetime.utcfromtimestamp(mod_time)
    mod_time = mod_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    requestMessage += "If-Modified-Since: " + mod_time + "\r\n"
    requestMessage += "\r\n"
else:
    requestMessage += "\r\n"

print(requestMessage)

# send encoded data through TCP connection
client.send(requestMessage.encode())
#===============================================================
# receive the server response
dataLen = 1000000
response = client.recv(dataLen)
response: str = response.decode()

# start reading content after end of this line
# extract this for caching
startLocation = response.find("Content-Type: text/html; charset=UTF-8\r\n\r\n")
if startLocation == -1:
    content = ""
else:
    content = response[startLocation + 42 : len(response)]

http200 = response.find("HTTP/1.1 200 OK")
http304 = response.find("HTTP/1.1 304 Not Modified")
http404 = response.find("HTTP/1.1 404 Not Found")

# file no exist
if http404 != -1:
    print(response)
    
# modified and not cached
if http200 != -1 and not isCached:
    print(response)
    cacheFile(content)

# modified file and cached
if http200 != -1 and isCached:
    print(response)
    cacheFile(content)
    
# file not modified
if http304 != -1:
    print(response)

client.close()
