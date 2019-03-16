from bitstring import BitArray

class memory:
    def __init__(self):
        self.sp=0x7ffffffc
        self.memory = {}
    
    def readWord(self,address):
        b = ""
        for i in range(4):
            if address+i in self.memory:
                b = self.memory[address+i] + b
            else:
                b = "00000000" + b
        print(b)
        return BitArray(bin = b).int

    def readByte(self,address):
        if address in self.memory:
            return BitArray(bin = self.memory[address]).int
        else:
            return 0
    
    def writeWord(self,address,value):
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
        value = BitArray(int = value, length = 8).bin
        self.memory[address] = value

    def printall(self):
        print(self.memory)

    def returnAll(self):
        return self.memory

    def flush(self):
        self.memory.clear()