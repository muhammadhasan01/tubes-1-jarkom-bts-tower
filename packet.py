class Packet:
    def __init__(self, tipe=b'\x00', length=0, sequenceNumber=0, data=b'HelloWorld!'):
        self.type = tipe
        self.length = length
        self.sequenceNumber = sequenceNumber
        self.data = data
        self.checksum = self.generateChecksum()
    
    def generateChecksum(self):
        rawNoChecksum = self.type+self.length.to_bytes(2,'big')+self.sequenceNumber.to_bytes(2,'big')+self.data
        result = int.from_bytes(rawNoChecksum[0:2],'big')
        i = 2
        length = len(rawNoChecksum)
        while i < length:
            result ^= int.from_bytes(rawNoChecksum[i:i+2],'big')
            i += 2
        return result.to_bytes(2,'big')

    def isChecksumValid(self):
        return self.checksum == self.generateChecksum()

    def getRAW(self):
        return self.type+self.length.to_bytes(2,'big')+self.sequenceNumber.to_bytes(2,'big')+self.checksum+self.data

    def fromRAW(self, raw):
        self.type = int(raw[0]).to_bytes(1,'big')
        self.length = int.from_bytes(raw[1:3],'big')
        self.sequenceNumber = int.from_bytes(raw[3:5],'big')
        self.checksum = raw[5:7]
        self.data = raw[7:7+self.length]