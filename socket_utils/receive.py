import socket

from .config import END_TOKEN


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock: socket.socket, numBytes: int):
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


def recvData(sock: socket.socket):
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


def recvFile(sock: socket.socket):
    # Receive the file name
    fileNameData = recvData(sock)

    filename = fileNameData[0].decode()

    print("File name received:", filename)

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

    print("File received")
    print("File is", fileSize, "bytes")

    return filename, fileData
