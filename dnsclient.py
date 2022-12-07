# DNS Client

import sys
import struct
import socket
import random


# Get server IP address and port from command line args
address = sys.argv[1]
port = int(sys.argv[2])
host = sys.argv[3]

# Create UDP client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

noResponse = True
numTries = 0
question = host + " A IN"

while(numTries < 3 and noResponse):
    # Generate a random number from 0 to 100 to act as message id
    msgID = random.randint(1, 100)

    print("Sending Request to " + address + ", " + str(port) + ":")
    if (numTries == 0):
        print("Message ID: " + str(msgID))
        print("Question Length: " + str(len(question.encode())) + " bytes")
        print("Answer Length: 0 bytes")
        print("Question: " + question + "\n")

    # Send DNS request to server
    request = struct.pack('>hhihh%ds' % (len(question.encode())), 1, 0, msgID, len(question), 0, question.encode())
    clientSocket.settimeout(1)
    clientSocket.sendto(request, (address, port))
    numTries += 1
    
    # Attempt to receive DNS response
    try:
        dResponse, dAddress = clientSocket.recvfrom(1024)
        response = struct.unpack('>hhihh%ds%ds' % (len(question.encode()), (len(dResponse) - len(question.encode()) - 12)), dResponse)
        rCode = int(response[1])
        msgID = int(response[2])
        qLen = int(response[3])
        aLen = int(response[4])
        question2 = response[5].decode()
        answer = response[6].decode()

        print("Received Response from " + address + ", " + str(port) + ":")
        if (rCode == 0):
            print("Return Code: " + str(rCode) + " (No errors)")
        else:
            print("Return Code: " + str(rCode) + " (Name does not exist)")
        print("Message ID: " + str(msgID))
        print("Question Length: " + str(len(question2.encode())) + " bytes")
        print("Answer Length: " + str(len(answer.encode())) + " bytes")
        print("Question: " + question2)
        if(len(answer.encode()) != 0):
            print("Answer: " + answer)

        noResponse = False
    except:
        print("Request timed out ... " )
        if (numTries == 3):
            print("Exiting Program.")


clientSocket.close()
