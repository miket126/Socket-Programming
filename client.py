# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import os
import socket
import sys

# Command line checks
if len(sys.argv) < 2:
     print("USAGE python " + sys.argv[0] + "<SERVER_NAME>" + "<PORT NUMBER>")

# The name of the file
#fileName = sys.argv[1]


# Server address
#serverAddr = "localhost"
serverAddr = sys.argv[1]

# Server port
#serverPort = 1234
serverPort = int(sys.argv[2])

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))






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
    if arg:
        print("Command sent to server:", cmd, arg)
    else:
        print("Command sent to server:", cmd)
        










    
    # ls command
    
        
    
    
    
     
     
        
    
    
    # If command is quit, exit
    if cmd == "quit":
        print("Connection closed successfully\n")
        break

    # Receive server response
    resData = recvData(connSock)
    res = resData[0].decode()
    print("Response received:", res)

    # Temporary
    #break


# # Send the file
# fileBytesSent = sendFile(connSock, fileName)
# print("File sent", fileBytesSent, "bytes")

# Close the socket
connSock.close()