
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
fileObj = open(fileName, "rb")
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
numTotal = 0

# The file data
fileData = None

i = 0
# Keep sending until all is sent
while True:
    
    # Make sure to read 65536 bytes everytime from file
	fileData = fileObj.read(65536)
	# Make sure we did not hit EOF
	if fileData:
			
		# Get the size of the data read
		# and convert it to string
		dataSizeStr = str(len(fileData))
		
		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr
	
		# Prepend the size of the data to the
		# file data.
		fileData = dataSizeStr.encode() + fileData	
		
		# The number of bytes sent
		numSent = 0
		
		# Send the data!
		while len(fileData) > numSent:
			numSent += connSock.send(fileData[numSent:])
			numTotal += numSent
	
	# The file has been read. We are done
	else:
		break


print ("Sent ", numTotal, " bytes.")

connSock.send(fileName.encode())
	
# Close the socket and the file
connSock.close()
fileObj.close()
	


