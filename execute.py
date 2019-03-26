from bitstring import BitArray

from registers import register
from memory import memory

class execute:
    def __init__(self):
        self.RegisterFile = register()
        self.Memory = memory()
        self.sp=0x7ffffffc
        self.PC = 0
        self.IR = 0

    def assemble(self,mc_code):
        self.RegisterFile.flush()
        self.Memory.flush()
        self.PC = 0
        self.RegisterFile.writeC("00010", self.sp)          #setting x2 as stack pointer
        mc_code = mc_code.splitlines()
        for line in mc_code:
            try:
                address,value = line.split()
                address = int(address,16)
                value = BitArray(hex = value).int
                self.Memory.writeWord(address,value)
                #print(self.Memory.readWord(address))
            except:
                return "fail"

    def run(self):
        self.printRegisters()
        while self.nextIR() != 0:
            self.fetch()

    def fetch(self): 
        self.IR = self.nextIR()
        self.IR = BitArray(int = self.IR, length = 32).bin
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
            print("funct3:"+self.funct3)
            if self.opcode == "0100011" and self.funct3 != "011":
                self.decodeS()
            else:
                self.decodeI()
        elif format == "sb":
            self.decodeSB()
        elif format == "u":
            self.decodeU()
        elif format == "uj":
            self.decodeUJ()
    
    def alu(self,operation):
        print("OP:",operation)
        if operation == "add":
            if self.muxB == 0:
                self.RZ = self.RA + self.RB
            if self.muxB == 1:
                self.RZ = self.RA + self.imm
        elif operation == "mul":
            self.RZ = self.RA * self.RB
        elif operation == "div":
            self.RZ = self.RA // self.RB
        elif operation == "rem":
            self.RZ = self.RA % self.RB
        elif operation == "beq":
            if self.RA == self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bne":
            if self.RA != self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "bge":
            if self.RA >= self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "blt":
            if self.RA < self.RB:
                self.PC = self.PC - 4 + self.imm
        elif operation == "auipc":
            self.RZ = self.PC - 4 + self.imm
        elif operation == "jal":
            self.PC_temp = self.PC
            self.PC = self.PC - 4 + self.imm 
        elif operation == "jalr":
            self.PC_temp = self.PC
            self.PC = self.RA + self.imm
        elif operation == "slli":
            self.RZ = BitArray(int=self.RA, length=32) << self.imm
            self.RZ = self.RZ.int
        elif operation == "srli":
            self.RZ = BitArray(int=self.RA, length=32) >> self.imm
            self.RZ = self.RZ.int
        elif operation == "srai":
            self.RZ = self.RA >> self.imm
        elif operation == "or":
            self.RZ = self.RA | self.RB
        elif operation == "and":
            self.RZ = self.RA & self.RB
        elif operation == "xor":
            self.RZ = self.RA ^ self.RB
        elif operation == "sub":
            self.RZ = self.RA - self.RB
        elif operation == "sll":
            self.RZ = BitArray(int=self.RA, length=32) << self.RB
            self.RZ = self.RZ.int
        elif operation == "srl":
            self.RZ = BitArray(int=self.RA, length=32) >> self.RB
            self.RZ = self.RZ.int
        elif operation == "sra":
            self.RZ = self.RA >> self.RB
        elif operation == "slt":
            self.RZ = 1 if self.RA < self.RB else 0
        elif operation == "sltu":
            self.RA = BitArray(int = self.RA, length = 32).uint
            self.RB = BitArray(int = self.RB, length = 32).uint
            self.RZ = 1 if self.RA < self.RB else 0
            
        self.memAccess()
        
    def memAccess(self):
        if self.memory_enable:
            if self.muxY == 1:
                if self.funct3 == "010":
                    self.data = self.Memory.readWord(self.RZ)
                elif self.funct3 == "000":
                    self.data = self.Memory.readByte(self.RZ)
            else:    
                if self.funct3 == "010":                        #sw
                    self.Memory.writeWord(self.RZ,self.RM)
                elif self.funct3 == "000":                      #sb
                    self.Memory.writeByte(self.RZ,self.RM)
                elif self.funct3 == "001":                      #sh
                    self.Memory.writeDoubleByte(self.RZ, self.RM)
        #writing in  muxY
        if self.muxY == 0:
            self.RY = self.RZ
        elif self.muxY == 1:
            self.RY = self.data
        elif self.muxY == 2:
            self.RY = self.PC_temp
        self.writeReg()

    def writeReg(self):
        if self.write_enable:
            self.RegisterFile.writeC(self.RD, self.RY)
            print("RY:"+str(self.RY))

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
        self.muxY=0
        if self.funct3 == "000" and self.funct7 == "0000000":
            self.alu("add")                 #add
        elif self.funct3 == "000" and self.funct7 == "0000001":
            self.alu("mul")                 #mul
        elif self.funct3 == "110" and self.funct7 == "0000000":
            self.alu("or")                  #or
        elif self.funct3 == "111" and self.funct7 == "0000000":
            self.alu("and")                 #and
        elif self.funct3 == "100" and self.funct7 == "0000000":
            self.alu("xor")                 #xor
        elif self.funct3 == "000" and self.funct7 == "0100000":
            self.alu("sub")                 #sub
        elif self.funct3 == "001" and self.funct7 == "0000000":
            self.alu("sll")                 #sub
        elif self.funct3 == "010" and self.funct7 == "0000000":
            self.alu("slt")                 #slt
        elif self.funct3 == "011" and self.funct7 == "0000000":
            self.alu("sltu")                 #sltu
        elif self.funct3 == "101" and self.funct7 == "0000000":
            self.alu("srl")                 #srl
        elif self.funct3 == "101" and self.funct7 == "0100000":
            self.alu("sra")                 #sra
        elif self.funct3 == "100" and self.funct7 == "0000001":
            self.alu("div")                 #div
        elif self.funct3 == "110" and self.funct7 == "0000001":
            self.alu("rem")                 #rem


    def decodeI(self):
        print("I-format")
        self.imm = BitArray(bin = self.IR[0:12]).int
        print("imm:"+str(self.imm))
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        self.muxB = 1
        if self.opcode == "0010011" and self.funct3 == "000":
            self.muxY = 0
            self.alu("add")                 #addi
        elif self.opcode == "0000011" and (self.funct3 == "010" or self.funct3 == "000"):
            self.muxY = 1
            self.memory_enable = True
            self.alu("add")                 #lw or lb
        elif self.opcode == "1100111" and self.funct3 == "000":
            self.muxY = 2
            self.alu("jalr")                #jalr 
        elif self.opcode == "0010011" and self.funct3 == "001":
            self.funct7 = self.IR[0:7]
            self.imm = BitArray(bin = self.IR[7:12]).uint
            if self.funct7 == "0000000":
                self.muxY = 0
                self.alu("slli")            #slli
        elif self.opcode == "0010011" and self.funct3 == "101":
            self.funct7 = self.IR[0:7]
            self.imm = BitArray(bin = self.IR[7:12]).uint
            if self.funct7 == "0000000":
                self.muxY = 0
                self.alu("srli")            #srli
            if self.funct7 == "0100000":
                self.muxY = 0
                self.alu("srai")            #srai (arithmetic right shift)


    
    def decodeS(self):
        print("S-format")
        self.RS2 = self.IR[7:12]
        print("RS2:"+self.RS2)
        self.RB = self.RegisterFile.readB(self.RS2)
        print("RB:"+str(self.RB))
        imm1 = self.IR[0:7]
        imm2 = self.IR[20:25]
        self.write_enable = False
        self.imm = BitArray(bin = imm1+imm2).int
        if self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001":
            self.RM = self.RB
            self.muxB = 1
            self.memory_enable = True
            self.alu("add")                 #sw or sb

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
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        if self.funct3 == "000":
            print("going to beq")
            self.alu("beq")                 #beq
        elif self.funct3 == "101":
            self.alu("bge")                 #bge
        elif self.funct3 == "100":
            self.alu("blt")                 #blt    
        elif self.funct3 == "001":
            self.alu("bne")                 #bne
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").uint             #for unsigned operations
        print(str(self.imm))
        if self.funct3 == "111":
            self.alu("bge")                 #bgeu
        elif self.funct3 == "110":
            self.alu("blt")                 #bltu

        
    def decodeU(self):
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        imm1 = self.IR[0:20]
        imm2 = "000000000000"
        self.imm = BitArray(bin = imm1 + imm2).int
        if self.opcode == "0110111":
            self.RA = 0
            self.muxB = 1
            self.alu("add")                 #lui
        else:
            self.alu("auipc")               #auipc

    def decodeUJ(self):
        self.RD = self.IR[20:25] 
        print("RD:"+self.RD)
        imm1 = self.IR[0]
        imm2 = self.IR[12:20]
        imm3 = self.IR[11]
        imm4 = self.IR[1:11]
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.muxY = 2
        self.alu("jal")                     #jal
        

    def printRegisters(self):
        self.RegisterFile.printall()

    def printMemory(self):
        self.Memory.printall()

    def returnRegisters(self):
        return self.RegisterFile.returnAll()

    def returnMemory(self):
        return self.Memory.returnAll()

    def readbyteMemory(self,address):
        return self.Memory.readByte(address)

    def nextIR(self):
        return self.Memory.readWord(self.PC)
    