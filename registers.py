class register:
    def __init__(self):
        self.registers = {}
        for i in range(32):
            self.registers['{0:05b}'.format(i)] = 0
    def readA(self,address):
        return self.registers[address]

    def readB(self,address):
        return self.registers[address]
    
    def writeC(self,address,value):
        if not address=="00000":
            self.registers[address] = value

    def printall(self):
        print(self.registers)

    def returnAll(self):
        return self.registers