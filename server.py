# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import os
import socket

#from socket_utils.receive import recvCmd, recvData, recvFile
#from socket_utils.send import sendData

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





#from socket_utils.config import COMMANDS
END_TOKEN = b"<END>"
COMMANDS = ["get", "put", "ls", "quit"]






#from socket_utils.receive import recvData

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock: socket.socket, numBytes: int) -> bytes:
    # The buffer
    recvBuff = str().encode()

    # The temporary buffer
    tmpBuff = str()

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        # Attempt to receive bytes
        tmpBuff = sock.recv(numBytes)
        # The other side has closed the socket
        if not tmpBuff:
            break
        # Add the received bytes to the buffer
        recvBuff += tmpBuff

    return recvBuff


def recvData(sock: socket.socket) -> tuple[bytes, int]:
    # Receive the size data
    dataSize = recvAll(sock, 10)

    # Client closed connection
    if not dataSize:
        return None

    # Decode data size
    dataSize = int(dataSize.decode())

    # Receive the data
    data = recvAll(sock, dataSize)

    return data, dataSize


def recvCmd(sock: socket.socket) -> tuple[str, str | None]:
    # Receive the command
    cmdData = recvData(sock)
    cmdList = cmdData[0].decode().split(" ")

    # Extract the cmd from cmdStr
    cmd = cmdList[0]

    # Removed the padded 0 from cmd
    while cmd.startswith("0"):
        cmd = cmd[1:]

    # Extract the arg from cmdStr
    arg = None

    if len(cmdList) > 1:
        arg = cmdList[1]

    return cmd, arg


def recvFile(sock: socket.socket) -> tuple[str, bytes, int]:
    # Receive the file name
    fileNameData = recvData(sock)

    filename = fileNameData[0].decode()

    fileSize = 0
    fileData = str()

    # Accept connections forever
    while True:
        # Receive a chunk
        chunkData = recvData(sock)

        # If client closed connection or received end token, exit
        if not chunkData or chunkData[0] == END_TOKEN:
            break

        # Add the file size
        fileSize += chunkData[1]

        # Append the received chunk
        fileData += chunkData[0].decode()

    return filename, fileData, fileSize







#from socket_utils.send import sendCmd, sendFile
def sendData(sock: socket.socket, data: bytes) -> int:
    # Make the size into a string
    sizeStr = str(len(data))

    # Pad the start of sizeStr with 0's
    while len(sizeStr) < 10:
        sizeStr = "0" + sizeStr

    # Prepend the size of the data to the
    # file data.
    dataToSend = sizeStr.encode() + data

    # The number of bytes sent
    numSent = 0

    # Start sending untill all data is sent
    while len(dataToSend) > numSent:
        numSent += sock.send(dataToSend[numSent:])

    return numSent


def sendCmd(sock: socket.socket, cmd: str, arg: str | None):
    # Construct the data
    dataToSend = str(cmd)

    # Pad the start of cmd with 0
    while len(dataToSend) < 4:
        dataToSend = "0" + dataToSend

    # Append arg to the
    if arg:
        dataToSend += " "
        dataToSend += arg

    # Send the data
    sendData(sock, dataToSend.encode())


def sendFile(sock: socket.socket, fileName: str) -> int:
    # Send the file name
    sendData(sock, fileName.encode())
    print("File name sent: ", fileName)

    # The number of bytes sent
    fileBytesSent = 0

    # The file data
    fileData = None

    # Open the file
    file = open(fileName, "rb")

    # Keep sending until all is sent
    while True:
        # Make sure to read 65536 bytes everytime from file
        fileData = file.read(65536)
        # Make sure we did not hit EOF
        if fileData:
            # Send the chunk
            # Add the bytes sent to the total bytes sent
            fileBytesSent += sendData(sock, fileData)

        # The file has been read. We are done
        else:
            break

    # Give token when file is fully transferred
    sendData(sock, END_TOKEN)
    # sock.send(END_TOKEN)

    # Close the file
    file.close()

    return fileBytesSent






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
    #break


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
