from registers import register
from memory import memory

class execute:
    def __init__(self,fName):
        self.RegisterFile = register()
        self.Memory = memory()
        self.PC = 0
        self.IR = 0
        MC = open(fName,"r")
        for line in MC:
            address,value = line.split()
            address = int(address,16)
            value = int(value,16)
            self.Memory.writeMEMORY(address,value)
            #print(self.Memory.readMEMORY(address))

    def run(self):
        self.printMemory()
        while self.Memory.readMEMORY(self.PC) != 0:
            self.fetch()

    def fetch(self): 
        self.IR = self.Memory.readMEMORY(self.PC)
        self.IR = '{:032b}'.format(self.IR)
        print("IR:"+str(self.IR))
        self.PC = self.PC + 4
        self.decode()
    
    def decode(self):
        self.opcode = self.IR[25:32]
        print("opcode:"+self.opcode)
        self.memory_enable = False
        self.write_enable = True
        self.muxY = 0
        self.RZ = 0
        format = self.checkFormat()
        print("format:"+format)
        if format == "r":
            self.decodeR()
        elif format == "iORs":
            self.RS1 = self.IR[12:17]
            print("RS1:"+self.RS1)
            self.RA = self.RegisterFile.readA(self.RS1)
            print("RA:"+str(self.RA))
            self.funct3 = self.IR[17:20]
            if self.opcode == "0100011" and self.funct3 != "011":
                self.decodeS()
            else:
                self.decodeI()
        elif format == "sb":
            self.decodeSB()
    
    def alu(self,op):
        print("OP:",op)
        if op == "add":
            if self.muxB == 0:
                self.RZ = self.RA + self.RB
            if self.muxB == 1:
                self.RZ = self.RA + self.imm
        elif op == "beq":
            if self.RA == self.RB:
                self.PC = self.PC - 4 + self.imm
        self.memAccess()
        
    def memAccess(self):
        if self.memory_enable:
            self.Memory.writeMEMORY(self.RZ,self.RM)
        if self.muxY == 0:
            self.RY = self.RZ
        self.writeReg()

    def writeReg(self):
        if self.write_enable:
            self.RegisterFile.writeC(self.RD, self.RY)

    def checkFormat(self):
        iORs = "0000011 0001111 0010011 0011011 0100011 1100111 1110011".split()
        r = "0110011 0111011".split()
        u = "0010111 0110111".split()
        sb = "1100011"
        uj = "1101111"

        for c in r:
            if self.opcode == c:
                return "r"
        for c in u:
            if self.opcode == c:
                return "u"
        if self.opcode == sb:
            return "sb"
        if self.opcode == uj:
            return "uj"
        for c in iORs:
            if self.opcode == c:
                return "iORs"
        return "none"

    def decodeR(self):
        self.RS1 = self.IR[12:17]
        print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        self.RA = self.RegisterFile.readA(self.RS1)
        print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        self.funct7 = self.IR[0:7]
        if(self.funct3 == "000" and self.funct7 == "0000000"):
            self.muxY=0
            self.alu("add")

    def decodeI(self):
        print("I-format")
        self.imm = int(self.IR[0:12],2)
        print("imm:"+str(self.imm))
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        self.muxB = 1
        if self.opcode == "0010011" and self.funct3 == "000":
            self.muxY = 0
            self.alu("add")
    
    def decodeS(self):
        print("S-format")
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        imm1 = self.IR[0:7]
        imm2 = self.IR[20:25]
        self.write_enable = False
        self.imm = int(imm1+imm2,2)
        if self.funct3 == "010":
            self.RM = self.RB
            self.muxB = 1
            self.memory_enable = True
            self.alu("add")

    def decodeSB(self):
        self.RS1 = self.IR[12:17]
        print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RA = self.RegisterFile.readA(self.RS1)
        print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        imm1 = self.IR[0]
        imm2 = self.IR[24]
        imm3 = self.IR[1:7]
        imm4 = self.IR[20:24]
        self.write_enable = False
        self.imm = int(imm1 + imm2 + imm3 + imm4 + "0", 2)
        if self.funct3 == "000":
            print("going to beq")
            self.alu("beq")
        
    

    def printRegisters(self):
        self.RegisterFile.printall()

    def printMemory(self):
        self.Memory.printall()
    