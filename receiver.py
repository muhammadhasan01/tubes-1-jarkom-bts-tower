import socket
import utils
from packet import Packet
import sys
import os

IPAdress = ""
bufferSize = (1 << 16) 
encoding = 'utf-8'

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

# Take arguments (port)
listofSysArg = list(sys.argv)
lenSysArg = len(listofSysArg)
if lenSysArg < 2:
    print("Arguments not correct, please input arguments of [port]")
    exit() 

# Create a datagram socket
UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)

# Bind to address and ip
Port = int(listofSysArg[1])
UDPServerSocket.bind((IPAdress, Port))

print("UDP server up and listening")

fileToWrite = ''


mapSeq = {}

# Listen for incoming datagrams
while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    RAW = bytesAddressPair[0]
    address = bytesAddressPair[1]
    packet = utils.turnRawToPacket(RAW)
    type = packet.type
    data = packet.data
    sequence = packet.sequenceNumber
    
    if sequence in mapSeq:
        print("Sequence already received")
        continue

    mapSeq[sequence] = True

    if not packet.isChecksumValid():
        print("Received packet isCheckSum is not valid")
        continue

    # print("Received packet of type", type, "with a sequence", sequence, \
    #      "and length", packet.length)

    # If packet type is DATA, send ACK
    if type == b'\x00':
        
        fileToWrite += str(packet.data, encoding)
        ACK = Packet(b'\x01', 18, sequence, b'Packet is received', packet.checksum)
        bytesToSend = ACK.getRAW()
        UDPServerSocket.sendto(bytesToSend, address)

    # If packet type is FIN, save to file and send FINACK
    elif type == b'\x02':
        fileToWrite += str(packet.data, encoding)
        # Make new directory
        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, r'./out')
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        # Save to file
        complete_dir = os.path.join(final_dir, 'downloaded')
        textFile = open(complete_dir, "w")
        textFile.write(fileToWrite)
        textFile.close()

        # Send FINACK
        FINACK = Packet(b'\x03', 18, sequence, b'File is downloaded', packet.checksum)
        bytesToSend = FINACK.getRAW() # Send packet in the form of RAW
        UDPServerSocket.sendto(bytesToSend, address)

        # Finish
        exit()