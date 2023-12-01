import os
import sys

from socket_utils.receive import recvCmd, recvData, recvFile
from socket_utils.send import sendData
from socket_utils.socketUtil import (
    createClientSocket,
    createServerSocket,
    handleRecvFile,
    handleSendFile,
)
from socket_utils.utils import filesInDir, validateDir

# Command line checks
if len(sys.argv) < 2:
    print("USAGE python " + sys.argv[0] + " <PORT NUMBER>\n")
    exit()

# The port of the server
port = int(sys.argv[1])


# Create the server socket.
server_sock, _ = createServerSocket(port)
print("Waiting for connections on port " + str(port) + "...")


# Accept connections
client_sock, addr = server_sock.accept()
print("Accepted connection from client: ", addr, "\n")
print("Waiting for next command...\n")

# Define directory for files
file_dir = "server_files"

# If file directory doesn't exist, create one
validateDir(file_dir)


# Control Channel
while True:
    # Command status
    status = "SUCCESS"

    # Receive the command and argument
    cmd, arg = recvCmd(client_sock)
    print(f"{addr} - ", cmd, arg, "\n")

    # Handle QUIT command
    if cmd == "quit":
        sendData(client_sock, "\n  Closing connection\n".encode())
        print(" ", f"[{cmd.upper()}]", status, "\n")
        break

    # Handle LS command
    if cmd == "ls":
        # Get the files in the files directory
        file_str = filesInDir(file_dir)

        # Send the data back
        sendData(client_sock, file_str.encode())

    # Handle GET or PUT command
    if cmd == "get" or cmd == "put":
        # Send acknowledgement
        sendData(client_sock, "".encode())

        # Receive the port number from client
        port_res = recvData(client_sock)
        data_sock_port = int(port_res.data)

        # Create socket and connect to data channel
        client_data_sock = createClientSocket("localhost", data_sock_port)
        print(" ", "Connected to data socket on port", data_sock_port, "\n")
        print(" ", "File transfer started")

        # If get command
        if cmd == "get":
            # Try to send the file
            error = handleSendFile(file_dir, arg, client_data_sock)

            status = "FAILURE" if error else status

        # If put command
        if cmd == "put":
            # Receive the file
            res = recvFile(client_data_sock)
            # Handle error and write to disk
            error = handleRecvFile(res, file_dir)

            status = "FAILURE" if error else status

        # Close the socket
        client_data_sock.close()
        print(" ", "Data socket closed\n")

    print(" ", f"[{cmd.upper()}]", status, "\n")
    print("Waiting for next command...\n")


# Close our side
client_sock.close()
server_sock.close()
print("Control socket closed")
