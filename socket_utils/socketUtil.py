import os
import socket

from .receive import FileResponse, Response
from .send import sendError, sendFile


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


def handleSendFile(file_dir: str, file_name: str, sock: socket.socket):
    try:
        file_path = os.path.join(file_dir, file_name)
        sendFile(sock, file_path)
        print("File transfer completed")
    except Exception:
        sendError(sock, "Error opening file")
        print("Error opening file")


def handleRecvFile(
    res: Response | FileResponse,
    file_dir: str,
):
    # Check for error
    if res.error:
        print("Error:", res.data)
    else:
        # Receive file and write file
        print("File transfer completed")

        file_path = os.path.join(file_dir, res.file_name)
        file = open(file_path, "wb")
        file.write(res.data.encode())
        file.close()
