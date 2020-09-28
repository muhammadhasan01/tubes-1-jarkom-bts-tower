class Packet:
    def __init__(self, raw):
        self.type = raw[0]
        self.length = int(raw[1:3])
        self.sequenceNumber = int(raw[3:5])
        self.checksum = raw[5:7]
        self.data = raw[7:7+self.length]

    def __init__(self, tipe, length, sequenceNumber, data):
        self.type = tipe
        self.length = length
        self.sequenceNumber = sequenceNumber
        self.data = data
        self.checksum = self.generateChecksum()
    
    def generateChecksum(self):
        rawNoChecksum = self.type.to_bytes(1,'big')+self.length.to_bytes(2,'big')+self.sequenceNumber(2,'big')+self.data
        result = int.from_bytes(rawNoChecksum[0:2],'big')
        i = 2
        length = len(rawNoChecksum)
        while i < length:
            result ^= int.from_bytes(rawNoChecksum[i:i+2],'big')
            i += 2
        return result

    def isChecksumValid(self):
        return self.checksum == self.generateChecksum()

    def getRAW(self):
        return self.type.to_bytes(1,'big')+self.length.to_bytes(2,'big')+self.sequenceNumber(2,'big')+self.checksum+self.data