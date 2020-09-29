import socket
import sys

# Take arguments
# Arguments should be in the format [filePath] [addresses...] [port]
listOfSysArg = list(sys.argv)
lenSysArg = len(listOfSysArg)

# Check number of arguments
if lenSysArg <= 3: # Notice that the script py file (sender.py) is included
    print("Arguments not correct, please input arguments of [addr] port")
    exit()

# Parse arguments (assumes that is in the correct format)

# Take fileContent
try:
    fileContent = open(listOfSysArg[1], 'r').read()
except:
    print("Error file not found in the specified path")
    exit()

# Take server addresses
listOfAddresses = [listOfSysArg[i] for i in range(2, lenSysArg - 1)]

# Take port
port = listOfSysArg[-1]

print(fileContent)
print(listOfAddresses)
print(port)

# TODO: Turn fileContent to packets
# TODO: Handle retransmission time

msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
print(bytesToSend)
port = 20001
serverAddressPort = ("127.0.0.1", port)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)