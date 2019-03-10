from registers import register
from memory import memory

class execute:
    def __init__(self,fName):
        self.RegisterFile = register()
        self.RegisterFile.writeC("00011",3)
        self.RegisterFile.writeC("00010",5)
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
        while self.Memory.readMEMORY(self.PC) != 0:
            self.fetch()

    def fetch(self): 
        self.IR = self.Memory.readMEMORY(self.PC)
        self.IR = '{:032b}'.format(self.IR)
        print("IR:"+str(self.IR))
        self.PC = self.PC + 4
        self.decode()
    
    def decode(self):
        opcode = self.IR[25:32]
        print("opcode:"+opcode)
        format = self.checkFormat(opcode)
        print("format:"+format)
        if format == "r":
            RS1 = self.IR[12:17]
            print("RS1:"+RS1)
            RS2 = self.IR[7:12]
            print("RS2:"+RS2)
            self.RD = self.IR[20:25] 
            print("RD:"+self.RD)
            self.RA = self.RegisterFile.readA(RS1)
            print("RA:"+str(self.RA))
            self.RB = self.RegisterFile.readB(RS2)
            print("RB:"+str(self.RB))
            self.muxB = 0
            funct3 = self.IR[17:20]
            funct7 = self.IR[0:7]
            if(funct3 == "000" and funct7 == "0000000"):
                self.write_enable = True
                self.muxY=0
                self.alu("add")
        if format == "iORs":
            RS1 = self.IR[12:17]
            print("RS1:"+RS1)
            self.RA = self.RegisterFile.readA(RS1)
            print("RA:"+str(self.RA))
            funct3 = self.IR[17:20]
            if opcode == "0100011" and funct3 != "011":
                a=1
            else:
                self.imm = int(self.IR[0:11],2)
                print("imm:"+str(self.imm))
                self.RD = self.IR[20:25] 
                print("RD:"+self.RD)
                self.muxB = 1
                if opcode == "0010011" and funct3 == "000":
                    self.write_enable = True
                    self.muxY = 0
                    self.alu("add")
    
    def alu(self,op):
        print("OP:",op)
        if op == "add":
            if self.muxB == 0:
                self.RZ = self.RA + self.RB
            if self.muxB == 1:
                self.RZ = self.RA + self.imm
        self.memAccess()
        
    def memAccess(self):
        if self.muxY == 0:
            self.RY = self.RZ
        self.writeReg()

    def writeReg(self):
        if self.write_enable:
            self.RegisterFile.writeC(self.RD, self.RY)
        print(self.RegisterFile.readA("00001"))

    def checkFormat(self,opcode):
        iORs = "0000011 0001111 0010011 0011011 0100011 1100111 1110011".split()
        r = "0110011 0111011".split()
        u = "0010111 0110111".split()
        sb = "1100011"
        uj = "1101111"

        for c in r:
            if opcode == c:
                return "r"
        for c in u:
            if opcode == c:
                return "u"
        if opcode == sb:
            return "sb"
        if opcode == uj:
            return "uj"
        for c in iORs:
            if opcode == c:
                return "iORs"
        return "none"

    