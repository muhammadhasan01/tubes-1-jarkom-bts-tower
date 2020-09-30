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
    UDPClientSocket.settimeout(2)
    try:
        bytesToSend = p.getRAW() # Send packet in the form of RAW
        UDPClientSocket.sendto(bytesToSend, target)
        (msgFromServer, _) = UDPClientSocket.recvfrom(bufferSize) # Received Packet in the form of RAW
        # print("MESSAGE:", msgFromServer)
        receivedPacket = turnRawToPacket(msgFromServer)
        if receivedPacket.checksum != p.checksum:
            print("Checksum is not the same as the sended packet")
            return False
        print("Received packet of type", receivedPacket.type, "with a sequence", receivedPacket.sequenceNumber)
        return True 
    except socket.timeout:
        print("Timeout, try to send packet again")
        return False

# Send message/packets to every receiver
for address in listOfAddresses:
    serverAddressPort = (address, port)
    for p in packets:
        print("Sending packet number", p.sequenceNumber, "with length", p.length, \
              "and type", p.type, "to", serverAddressPort)
        while not send(p,serverAddressPort):
            pass