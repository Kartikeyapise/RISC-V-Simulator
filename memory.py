from bitstring import BitArray

class memory:
    def __init__(self):
        self.memory = {}
    
    def readWord(self,address):
        b = ""
        for i in range(4):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        #print(b)
        return BitArray(bin = b).int

    def readByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).int
        else:
            return 0

    def readDoubleByte(self, address):
        b = ""
        for i in range(2):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        #print(b)
        return BitArray(bin = b).int

    def readUnsignedByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).uint
        else:
            return 0

    def readUnsignedDoubleByte(self, address):
        b = ""
        for i in range(2):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        #print(b)
        return BitArray(bin = b).uint
    
    def writeWord(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"         #for gui purpose
                
        value = BitArray(int = value, length = 32).bin
        b3 = value[0:8]
        b2 = value[8:16]
        b1 = value[16:24]
        b0 = value[24:32]
        self.memory[address] = b0
        self.memory[address+1] = b1
        self.memory[address+2] = b2
        self.memory[address+3] = b3

    def writeByte(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"           #for gui purpose

        value = BitArray(int = value, length = 8).bin
        self.memory[address] = value

    def writeDoubleByte(self,address,value):
        if address%4 != 0:
            address_to_be_written = address - address%4
            if not address_to_be_written in self.memory:
                self.memory[address_to_be_written] = "00000000"           #for gui purpose

        value = BitArray(int = value, length = 32).bin
        b1 = value[16:24]
        b0 = value[24:32]
        self.memory[address] = b0
        self.memory[address+1] = b1

    def printall(self):
        print(self.memory)

    def returnAll(self):
        return self.memory

    def flush(self):
        self.memory.clear()