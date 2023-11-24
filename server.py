
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket


# The port on which to listen
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(("localhost", listenPort))

# Start listening on the socket
welcomeSock.listen()

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

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


print("Waiting for connections...")
	
# Accept connections
clientSock, addr = welcomeSock.accept()

print("Accepted connection from client: ", addr)
print("\n")

nameSize = recvAll(clientSock, 10)
filename = recvAll(clientSock, int(nameSize.decode())).decode()
print(filename)
fileSize = 0
fileData = str()

# Accept connections forever
while True:
	
	# The buffer to all data received from the
	# the client.
	
	
	# The temporary buffer to store the received
	# data.
	#recvBuff = str()
	
	# The size of the incoming file
	tempSize = str()
	
 
	# Receive the first 10 bytes indicating the
	# size of the file
	
	tempSize = recvAll(clientSock, 10)
	
	
 
	# If other side close conn
	if not tempSize:
		break

	

	print(tempSize)
	fileSize += int(tempSize.decode())
	
	
	# Get the file data
	fileData += (recvAll(clientSock, int(tempSize.decode()))).decode()

	
 
print("The file size is ", fileSize, "bytes")
	
#print("The file data is: ", fileData)
 
file = open(filename, "wb")
file.write(fileData.encode())
file.close()

# Close our side
clientSock.close()
welcomeSock.close()
 