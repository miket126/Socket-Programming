import os
import socket

from .receive import FileResponse, Response
from .send import FileBytesSent, sendError, sendFile


# Create a server socket and listen
def createServerSocket(port=0):
    # Create a server socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    sock.bind(("", port))

    # Start listening on the socket
    sock.listen()

    # Get the port number
    generated_port = sock.getsockname()[1]

    return sock, generated_port


# Create a client socket and connect to server socket
def createClientSocket(hostname: str, serverPort: int):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((hostname, serverPort))

    return sock


def handleSendFile(file_dir: str, file_name: str, sock: socket.socket) -> bool:
    try:
        file_path = os.path.join(file_dir, file_name)
        bytes_sent = sendFile(sock, file_path)

        # Print file info
        print(" ", "File transfer completed")
        print(" ", "File bytes sent:")
        print(" ", "  - File name:", file_name)
        print(
            " ", "  - File name header bytes:", bytes_sent.file_name_header_bytes_sent
        )
        print(" ", "  - File name bytes:", bytes_sent.file_name_bytes_sent)
        print(" ", "  - File header bytes:", bytes_sent.file_header_bytes_sent)
        print(" ", "  - File bytes:", bytes_sent.file_bytes_sent)
        print(" ", "  - File bytes total:", bytes_sent.total_bytes_sent)

        return False

    except Exception as e:
        sendError(sock, "Error opening file")
        print(" ", "Error opening file")

        return True


def handleRecvFile(
    res: Response | FileResponse,
    file_dir: str,
) -> bool:
    # Check for error
    if res.error:
        print(" ", "Error:", res.data)
    else:
        # Print file info
        print(" ", "File transfer completed")
        print(" ", "File Data received:")
        print(" ", "  - File name:", res.file_name)
        print(" ", "  - File size:", res.size, " bytes")

        # Receive file and write file
        file_path = os.path.join(file_dir, res.file_name)
        file = open(file_path, "wb")
        file.write(res.data.encode())
        file.close()

    return res.error
