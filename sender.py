import socket, sys
from packet import Packet
from utils import parseSenderArgument, turnMessageToPackets, turnRawToPacket

# Take arguments
# Arguments should be in the format [filePath] [addresses...] [port]
(fileContent, listOfAddresses, port) = parseSenderArgument(sys.argv)

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
# Set buffersize to 2^16 to be safe
bufferSize = (1 << 16) 

# print(fileContent)

# Turn fileContent to packets
packets = turnMessageToPackets(fileContent)

# Send message/packets to every receiver
for address in listOfAddresses:
    # TODO: Handle Scheduling
    serverAddressPort = (address, port)
    for p in packets:
        print("Sending packet number", p.sequenceNumber, "to", serverAddressPort)
        print("PACKET INFO:", p.type, p.length, p.sequenceNumber, p.checksum, p.data, sep = '\n')
        bytesToSend = p.getRAW() # Send packet in the form of RAW
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize) # Received Packet in the form of RAW
        receivedPacket = turnRawToPacket(bytesToSend)
        # TODO: Handle packet type
        print("Received packet of type", receivedPacket.type)