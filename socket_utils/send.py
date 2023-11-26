import socket

from .config import END_TOKEN


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
