import socket

from .config import END_TOKEN


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
