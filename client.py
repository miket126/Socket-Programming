
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
	print ("USAGE python " + sys.argv[0] + " <FILE NAME>" )

# The name of the file
fileName = sys.argv[1]


# Open the file
fileObj = open(fileName, "r", encoding="utf8")
#fileObj = open("file.txt", "rb")



# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = str()

# Get file size
filesize = str(os.path.getsize(fileName))
print(filesize)

# Turn file size into 10 bytes header
while len(filesize) < 10:
	filesize = '0' + filesize
print(filesize)

connSock.send(filesize.encode())

i = 0

# Keep sending until all is sent
while True:
    
	# Read 65536 bytes of data every time
	fileData = fileObj.read(65536)
	numSent = 0
	print(i+1)
	# Make sure we did not hit EOF
	if fileData:
		# Send the data!
		while len(fileData) > numSent:
			numSent += connSock.send(fileData[numSent:].encode())
			
	# The file has been read. We are done
	else:
		break


print ("Sent ", numSent, " bytes.")

connSock.send(fileName.encode())
	
# Close the socket and the file
connSock.close()
fileObj.close()
	


