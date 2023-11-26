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
from socket_utils.send import sendCmd, sendFile

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
    _input = input("ftp> ").lower().split(" ")

    # Initialize command and arg
    cmd = ""
    arg = None

    # Validate input
    if len(_input) < 1 or len(_input) > 2:
        print("Invalid input\n")
        continue

    # Assign the command
    cmd = _input[0]

    # If argument is provided, assign it to a variable
    if len(_input) > 1:
        arg = _input[1]

    # Validate cmd
    if cmd not in COMMANDS:
        print("Invalid command")
        print("Valid commands:")
        print("\tls")
        print("\tget <file name>")
        print("\tput <file name>")
        print("\tquit")
        continue

    # Send the command
    sendCmd(connSock, cmd, arg)
    print("Command sent to server:", cmd, arg)

    # If command is quit, exit
    if cmd == "quit":
        break

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
