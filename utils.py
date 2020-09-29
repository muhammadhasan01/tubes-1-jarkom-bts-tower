from packet import Packet

def parseSenderArgument(args):
    listOfSysArg = list(args)
    lenSysArg = len(listOfSysArg)

    # Check number of arguments
    if lenSysArg <= 3: # Notice that the script py file (sender.py) is included
        print("Arguments not correct, please input arguments of [path] [address..] [port]")
        exit()

    # Parse arguments (assumes that is in the correct format)
    # Take fileContent
    try:
        fileContent = str.encode(open(listOfSysArg[1], 'r').read())
    except:
        print("Error file not found in the specified path")
        exit()

    # Take server addresses
    listOfAddresses = [listOfSysArg[i] for i in range(2, lenSysArg - 1)]

    # Take port
    port = int(listOfSysArg[-1])

    return (fileContent, listOfAddresses, port)

def turnMessageToPackets(msg, maxSize = 32767):
    packets = []
    it, lenMsg = 0, len(msg)
    while it < lenMsg:
        # (TYPE, LENGTH, SEQUENCE NUMBER, CHECKSUM, DATA)
        newPacket = Packet(b'\x00' if it + maxSize < lenMsg else b'\x02', \
                           min(lenMsg - it, maxSize), it, \
                           msg[it: it + maxSize])
        packets += [newPacket]
        it += maxSize
    return packets

def turnRawToPacket(raw):
    tipe = int(raw[0]).to_bytes(1, 'big')
    length = int(from_bytes(raw[1: 3], 'big'))
    sequenceNumber = int(from_bytes(raw[3: 5], 'big'))
    checksum = raw[5: 7]
    data = raw[7: 7 + length]
    return Packet(tipe, length, sequenceNumber, data, checksum)
