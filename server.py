# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import os
import socket

from socket_utils.receive import recvCmd, recvData, recvFile
from socket_utils.send import sendData

# The port on which to listen
listenPort = 1234

# Create a welcome socket.
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(("localhost", listenPort))

# Start listening on the socket
welcomeSock.listen()


print("Waiting for connections...")

# Accept connections
clientSock, addr = welcomeSock.accept()

print("Accepted connection from client: ", addr)
print("\n")

# Control Channel
while True:
    # Receive the command and argument
    cmd, arg = recvCmd(clientSock)
    print("Command received:", cmd, arg)

    # If command is quit, exit
    if cmd == "quit":
        break

    # Handle commands
    # Temporary
    sendData(
        clientSock, "".join([cmd, " " if arg else "", arg if arg else ""]).encode()
    )
    print("Sent command back to client")

    # Temporary
    break


# # Receive file and write file
# filename, fileData, fileSize = recvFile(clientSock)
# print("File received")
# print("File is", fileSize, "bytes")


# file_path = os.path.join("server_files", filename)
# file = open(file_path, "wb")
# file.write(fileData.encode())
# file.close()

# Close our side
clientSock.close()
welcomeSock.close()
