class memory:
    def __init__(self):
        self.sp=0x7ffffffc
        self.memory = {}
    
    def readWord(self,address):
        b = ""
        for i in range(4):
            if address+i in self.memory:
                b = self.memory[address] + b
            else:
                b = "00000000" + b
        
        return int(b,2)

    def readByte(self,address):
        if address in self.memory:
            return int(self.memory[address],2)
        else:
            return 0
    
    def writeWord(self,address,value):
        value = '{:032b}'.format(value)
        b3 = value[0:8]
        b2 = value[8:16]
        b1 = value[16:24]
        b0 = value[24:32]
        self.memory[address] = b0
        self.memory[address+1] = b1
        self.memory[address+2] = b2
        self.memory[address+3] = b3

    def writeByte(self,address,value):
        value = '{:08b}'.format(value)
        self.memory[address] = value

    def printall(self):
        print(self.memory)