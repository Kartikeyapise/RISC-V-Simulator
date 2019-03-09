class memory:
    def __init__(self):
        self.sp=0x7ffffffc
        self.memory = {}
    
    def readMEMORY(self,address):
        return self.memory[address]
    
    def writeMEMORY(self,address,value):
        self.memory[address] = value