# DNS Server

import struct
import socket

#Set server IP address and port number
addressIP = "127.0.0.1"
port = 12000

# Create a UDP server socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign IP address and port to socket
serverSocket.bind((addressIP, port))

print("The server is ready to receive on port:  " + str(port) + "\n")

while True:
    message, address = serverSocket.recvfrom(1024)
    msg = struct.unpack('>hhihh{}s'.format(len(message) - 12), message)
    msgID = int(msg[2])
    qLen = int(msg[3])
    question = msg[5].decode()
    rCode = 1
    answer = ""
    records = []
    ansFound = False

    file = open("dns-master.txt", "r")
    for line in file:
        if 'A IN' in line:
            records.append(line.rstrip())
#            print(records[0])

    for record in records:
        if question in record:
            answer = record
            ansFound = True

    if (ansFound == True):
        rCode = 0

    response = struct.pack('>hhihh{}s{}s'.format(len(question.encode()), len(answer.encode())), 2, rCode, msgID, len(question), len(answer), question.encode(), answer.encode())
    serverSocket.sendto(response, address)
