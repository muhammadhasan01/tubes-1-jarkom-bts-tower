import socket
import packet
import sys
import os

IPAdress = "127.0.0.1"
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

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    packet = bytesAddressPair[0]
    address = bytesAddressPair[1]
    type = packet.type
    data = packet.data

    # If packet type is DATA, send ACK
    while (type == b'\x00' and packet.isCheckSumValid()):
        clientMsg = "Message from Client:{}".format(data)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        fileToWrite += str(packet.data, encoding)
        ACK = packet.Packet(b'\x01', 0, 0, b'Packet is received')
        UDPServerSocket.sendto(ACK, address)
    
    # If packet type is FIN, save to file and send FINACK
    if (type == b'\x02'):
        # Make new directory
        current_dir = os.getcwd()
        final_dir = os.path.join(current_dir, r'./out')
        if not os.path.exists(final_dir):
            os.makedirs(final_dir)

        # Save to file
        complete_dir = os.path.join(final_dir, 'downloaded.txt')
        textFile = open(complete_dir, "w")
        textFile.write(fileToWrite)
        textFile.close()

        # Send FINACK
        FINACK = packet.Packet(b'\x03', 0, 0, b'File is downloaded')
        UDPServerSocket.sendto(FINACK, address)

        # Prepare for next file
        fileToWrite =''
