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

# Define directory for files
file_dir = "server_files"


# Control Channel
while True:
    # Receive the command and argument
    cmd, arg = recvCmd(client_sock)
    print("Command received:", cmd, arg, "\n")

    # Handle QUIT command
    if cmd == "quit":
        sendData(client_sock, "\nClosing connection".encode())
        break

    # Handle LS command
    if cmd == "ls":
        # Get the current working directory
        current_directory = os.getcwd()

        # List all files and directories in the current working directory
        files_and_directories = os.listdir(os.path.join(current_directory, file_dir))

        # Generate the string containing the file names
        fileStr = "\nFiles on server:\n"
        for item in files_and_directories:
            fileStr += "- " + item + "\n"

        # Send the data back
        sendData(client_sock, fileStr.encode())

    # Handle GET or PUT command
    if cmd == "get" or cmd == "put":
        # Send acknowledgement
        sendData(client_sock, "".encode())

        # Receive the port number from client
        port_res = recvData(client_sock)
        data_sock_port = int(port_res.data)

        # Create socket and connect to data channel
        client_data_sock = createClientSocket("localhost", data_sock_port)
        print("Connected to data socket on port", data_sock_port, "\n")
        print("File transfer started")

        # If get command
        if cmd == "get":
            # Try to send the file
            handleSendFile(file_dir, arg, client_data_sock)

        # If put command
        if cmd == "put":
            # Receive the file
            res = recvFile(client_data_sock)
            # Handle error and write to disk
            handleRecvFile(res, file_dir)

        # Close the socket
        client_data_sock.close()
        print("Data socket closed\n")
        
    print("Waiting for next command...")


# Close our side
client_sock.close()
server_sock.close()
print("Control socket closed")
