# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import os
import socket
import sys

from socket_utils.config import COMMANDS
from socket_utils.receive import recvData
from socket_utils.send import sendData, sendFile

# # Command line checks
# if len(sys.argv) < 2:
#     print("USAGE python " + sys.argv[0] + " <FILE NAME>")

# # The name of the file
# fileName = sys.argv[1]


# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

while True:
    # Get the user input
    cmd = input("ftp> ").lower()

    # Validate user input
    if cmd not in COMMANDS:
        print("Invalid command\n")
        continue

    # Send user input
    sendData(connSock, cmd.encode())
    print("Command sent to server")

    # Receive server response
    resData = recvData(connSock)
    res = resData[0].decode()
    print("Response received:", res)

    # Temporary
    break


# # Send the file
# fileBytesSent = sendFile(connSock, fileName)
# print("File sent", fileBytesSent, "bytes")

# Close the socket
connSock.close()
