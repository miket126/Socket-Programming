import sys

from socket_utils.receive import recvData, recvFile
from socket_utils.send import sendCmd, sendData
from socket_utils.socketUtil import (
    createClientSocket,
    createServerSocket,
    handleRecvFile,
    handleSendFile,
)
from socket_utils.utils import validateCmd, validateDir

# Command line checks
if len(sys.argv) < 3:
    print("USAGE python " + sys.argv[0] + " <HOST NAME> <PORT NUMBER>\n")
    exit()

# The host name of the server
hostname = sys.argv[1]

# The port of the server
server_port = int(sys.argv[2])

# Create a socket and connect
client_sock = createClientSocket(hostname, server_port)

# Define directory for files
file_dir = "client_files"

# If file directory doesn't exist, create one
validateDir(file_dir)

# Output command usage
print("\nUsage")
print("'ls' to list file in server")
print("'get <file name>' to download file")
print("'put <file name>' to upload file")
print("'quit' to exit\n")

while True:
    # Get the user input
    _input = input("ftp> ").lower().split(" ")

    # Get the command and argument
    cmd, arg, valid = validateCmd(_input)

    if not valid:
        continue

    # Send the command
    sendCmd(client_sock, cmd, arg)
    # print("Command sent to server:", cmd, arg)

    # Receive response
    res = recvData(client_sock)
    print(res.data)

    # If command is QUIT, exit
    if cmd == "quit":
        break

    # If command is GET or PUT, open a socket
    if cmd == "get" or cmd == "put":
        # Create a data server sock
        data_sock, data_sock_port = createServerSocket()
        print(" ", "Data socket created")
        print(" ", "Data socket listening on " + str(data_sock_port) + "...")

        # Send the port number to the server
        sendData(client_sock, str(data_sock_port).encode())

        # Accept connections
        client_data_sock, addr = data_sock.accept()
        print(" ", "Accepted connection from client: ", addr, "\n")
        print(" ", "File transfer started")

        # If GET command
        if cmd == "get":
            # Receive the file
            res = recvFile(client_data_sock)
            # Handle error and write to disk
            handleRecvFile(res, file_dir)

        # If PUT command
        if cmd == "put":
            # Try to send the file
            handleSendFile(file_dir, arg, client_data_sock)

        # Close sockets
        data_sock.close()
        client_data_sock.close()
        print(" ", "Data socket closed\n")


# Close the socket
client_sock.close()
print("Control socket closed")
