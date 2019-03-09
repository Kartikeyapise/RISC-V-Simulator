class register:
    def __init__(self):
        self.registers = {}
        for i in range(32):
            self.registers["x"+str(i)] = 0x0
    def readA(self,address):
        return self.registers[address]

    def readB(self,address):
        return self.registers[address]
    
    def writeC(self,address,value):
        if not address=="x0":
            self.registers[address] = value