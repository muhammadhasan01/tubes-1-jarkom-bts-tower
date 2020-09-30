import socket, sys
from packet import Packet
from utils import parseSenderArgument, turnMessageToPackets, turnRawToPacket

# Take arguments
# Arguments should be in the format [filePath] [addresses...] [port]
(fileContent, listOfAddresses, port) = parseSenderArgument(sys.argv)

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
# Set buffersize to 2^16 just to be safe
bufferSize = (1 << 16)

# Turn fileContent to packets
packets = turnMessageToPackets(fileContent)



def send(p: Packet, target):
    try:
        bytesToSend = p.getRAW() # Send packet in the form of RAW
        UDPClientSocket.sendto(bytesToSend, target)
        UDPClientSocket.settimeout(1)
        (msgFromServer, _) = UDPClientSocket.recvfrom(bufferSize) # Received Packet in the form of RAW
        # print("MESSAGE:", msgFromServer)
        receivedPacket = turnRawToPacket(msgFromServer)
        # TODO: Handle packet type
        print("Received packet of type", receivedPacket.type, "with no", receivedPacket.sequenceNumber)
        return True
    except socket.timeout:
        print("Timeout, try to send packet again")
        return False

# Send message/packets to every receiver
for address in listOfAddresses:
    # TODO: Handle Scheduling
    serverAddressPort = (address, port)
    for p in packets:
        print("Sending packet number", p.sequenceNumber, "with length", p.length, \
              "to", serverAddressPort)
        while not send(p,serverAddressPort):
            pass