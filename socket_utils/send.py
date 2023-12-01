import os
import socket


def sendData(
    sock: socket.socket, data: bytes, isFinished: bool = True, isError: bool = False
) -> int:
    # Make the size into a string
    size_str = str(len(data))

    # Pad the start of sizeStr with 0's
    while len(size_str) < 10:
        size_str = "0" + size_str

    # Calculate finished byte
    finished_byte = ("1" if isFinished else "0").encode()

    # Calculate error byte
    error_byte = ("1" if isError else "0").encode()

    # Prepend the size of the data to the
    # file data.
    data_to_send = finished_byte + error_byte + size_str.encode() + data

    # The number of bytes sent
    num_sent = 0

    # Start sending untill all data is sent
    while len(data_to_send) > num_sent:
        num_sent += sock.send(data_to_send[num_sent:])

    return num_sent


def sendCmd(sock: socket.socket, cmd: str, arg: str | None):
    # Construct the data
    data_to_send = str(cmd)

    # Pad the start of cmd with 0
    while len(data_to_send) < 4:
        data_to_send = "0" + data_to_send

    # Append arg to the
    if arg:
        data_to_send += " "
        data_to_send += arg

    # Send the data
    sendData(sock, data_to_send.encode())


def sendError(sock: socket.socket, msg: str):
    return sendData(sock, msg.encode(), True, True)


def sendFile(sock: socket.socket, file_path: str) -> int:
    # Get the file name from path
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    file_name = file_name + file_extension

    # Try opening the file before sending the file name
    file = open(file_path, "rb")

    # Send the file name
    sendData(sock, file_name.encode())

    # The number of bytes sent
    file_bytes_sent = 0

    # The file data
    file_data = None

    # Keep sending until all is sent
    while True:
        # Make sure to read 65536 bytes everytime from file
        file_data = file.read(65536)
        # Make sure we did not hit EOF
        if file_data:
            # Send the chunk
            # Add the bytes sent to the total bytes sent
            file_bytes_sent += sendData(sock, file_data, False)

        # The file has been read. We are done
        else:
            break

    # Give token when file is fully transferred
    sendData(sock, "".encode())
    # sock.send(END_TOKEN)

    # Close the file
    file.close()

    return file_bytes_sent
