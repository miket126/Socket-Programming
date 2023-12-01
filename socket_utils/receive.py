import socket


class Response:
    def __init__(self, data: bytes, data_size: int, finished: bool, error: bool):
        self.data = data.decode()
        self.size = data_size
        self.finished = finished
        self.error = error


class FileResponse(Response):
    def __init__(
        self, data: bytes, data_size: int, finished: bool, error: bool, file_name: str
    ):
        super().__init__(data, data_size, finished, error)
        self.file_name = file_name


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


def recvData(sock: socket.socket) -> Response:
    # Receive the finished byte
    finished_byte = recvAll(sock, 1)

    # Receive the error byte
    error_byte = recvAll(sock, 1)

    # Receive the size data
    data_size = recvAll(sock, 10)

    # Client closed connection
    if not data_size:
        return None

    # Decode header fields
    data_size = int(data_size.decode())
    finished = True if finished_byte.decode() == "1" else False
    error = True if error_byte.decode() == "1" else False

    # Receive the data
    data = recvAll(sock, data_size)

    # return data, data_size, finished, error
    return Response(data, data_size, finished, error)


def recvCmd(sock: socket.socket) -> tuple[str, str | None]:
    # Receive the command
    res = recvData(sock)

    cmd_str = res.data.split(" ")

    # Extract the cmd from cmdStr
    cmd = cmd_str[0]

    # Removed the padded 0 from cmd
    while cmd.startswith("0"):
        cmd = cmd[1:]

    # Extract the arg from cmdStr
    arg = None

    if len(cmd_str) > 1:
        arg = cmd_str[1]

    return cmd, arg


def recvFile(sock: socket.socket) -> Response | FileResponse:
    # Receive the file name
    file_name_res = recvData(sock)

    # If error, return message and error flag
    if file_name_res.error:
        return file_name_res

    # Get the file name
    filename = file_name_res.data

    file_size = 0
    file_data = str()

    # Accept connections forever
    while True:
        # Receive a chunk
        chunk_res = recvData(sock)

        # If client closed connection or received end token, exit
        if not chunk_res.data or chunk_res.finished:
            break

        # Add the file size
        file_size += chunk_res.size

        # Append the received chunk
        file_data += chunk_res.data

    return FileResponse(file_data.encode(), file_size, True, False, filename)
