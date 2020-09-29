class Packet:
    def __init__(self, tipe = b'\x00', length = 0, sequenceNumber = 0, data = b'', checksum = None):
        self.type = tipe
        self.length = length
        self.sequenceNumber = sequenceNumber
        self.data = data
        if checksum is None:
            self.checksum = self.generateChecksum()
        else:
            self.checksum = checksum

    def getRAW(self):
        return  self.type + \
                self.length.to_bytes(2, 'big') + \
                self.sequenceNumber.to_bytes(2, 'big') + \
                self.checksum + \
                self.data
    
    def generateChecksum(self, size = 2):
        rawNoChecksum = self.type + \
                        self.length.to_bytes(2, 'big') + \
                        self.sequenceNumber.to_bytes(2, 'big') + \
                        self.data
        
        ret, it = 0, 0
        while it < len(rawNoChecksum):
            ret ^= int.from_bytes(rawNoChecksum[it: it + size], 'big')
            it += size
        return ret.to_bytes(size, 'big')

    def isChecksumValid(self):
        return self.checksum == self.generateChecksum()