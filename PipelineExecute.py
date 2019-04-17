from bitstring import BitArray

from registers import register
from memory import memory

class PipelineExecute:
    def __init__(self):
        self.RegisterFile = register()
        self.Memory = memory()
        self.sp=0x7ffffffc
        self.PC = 0
        self.IR = 0
        self.RZ = 0
        self.RA = 0
        self.RB = 0
        self.RY = 0
        self.RM = 0
        self.imm = 0
        self.cycle = 0
        self.stalls_data = 0
        self.stalls_control = 0
        self.do_dataForwarding = True
        self.memAccess_run = False
        self.alu_run = False
        self.decode_run = False
        self.fetch_run = False
        self.stopPipeLine = False
        self.RDQueue = []
        self.branchTaken = False
        self.total_ins = 0
        self.total_control_ins = 0
        self.total_data_ins = 0
        self.total_alu_ins = 0
        self.data_hazards = 0
        self.control_hazards = 0
        self.was_data_hazard = False
        self.knob3 = False
        self.knob4 = False
        self.knob5 = False
        self.buffer_line_no = 0

    def runPipeLineStep(self):
        print('Cycle No. : '+str(self.cycle) + ' ------------------------------------')
        if self.memAccess_run:
            #print('---------------------------')
            self.writeReg()
            #print('---------------------------')
        if self.alu_run:
            #print('---------------------------')
            self.memAccess()
            if self.knob4 or self.PC == (self.buffer_line_no - 1)/4:
                print('RY : ' + str(self.RY))
                print('RM : ' + str(self.RM))
            #print('---------------------------')
        else:
            self.memAccess_run = False
        if self.decode_run:
            #print('---------------------------')
            self.alu()
            if self.knob4:
                print('RZ : ' + str(self.RZ))
            #print(self.alu_buffer)
            #print('---------------------------')
        else:
            self.alu_run = False
        if self.fetch_run:
            #print('---------------------------')
            self.decode()
            if self.knob4:
                print('RA : ' + str(self.RA))
                if self.muxB == 0:
                    print('RB : ' + str(self.RB))
                else:
                    print('imm : ' + str(self.imm))
            #print(self.decode_buffer)
            #print('---------------------------')
        else:
            self.decode_run = False
        if self.nextIR() != 0:
            if self.PC/4 == (self.buffer_line_no - 1):
                self.knob5 = True
            #print('---------------------------')
            self.fetch()
            #print('---------------------------')
        else:
            self.fetch_run = False
        
        self.cycle = self.cycle+1
        if self.knob3:
            self.RegisterFile.printall()
        if self.knob4:
            print('IR : ' + self.IR)

        if self.knob5:
            print('IR : ' + self.IR)
            print('RA : ' + str(self.RA))
            if self.muxB == 0:
                print('RB : ' + str(self.RB))
            else:
                print('imm : ' + str(self.imm))
            print('RZ : ' + str(self.RZ))
            print('RY : ' + str(self.RY))
            print('RM : ' + str(self.RM))
            self.knob5 = False

        if (self.nextIR() == 0) and (not self.memAccess_run) and (not self.alu_run) and (not self.decode_run) and (not self.fetch_run):
            self.stopPipeLine = True
            #print('PipeLine Stoped!')

    def runPipeLine(self):
        self.runPipeLineStep()
        
        if not self.stopPipeLine:
            self.runPipeLine()
        else:
            self.stopPipeLine = False
            return


    def assemble(self,mc_code):
        self.RDQueue.clear()
        self.RegisterFile.flush()
        self.Memory.flush()
        self.PC = 0
        self.cycle = 0
        self.stalls_data = 0
        self.stalls_control = 0
        self.total_ins = 0
        self.total_control_ins = 0
        self.total_data_ins = 0
        self.total_alu_ins = 0
        self.data_hazards = 0
        self.control_hazards = 0
        self.was_data_hazard = False
        self.RegisterFile.writeC("00010", self.sp)          #setting x2 as stack pointer
        mc_code = mc_code.splitlines()
        for line in mc_code:
            try:
                address,value = line.split()
                address = int(address,16)
                value = BitArray(hex = value).int
                self.Memory.writeWord(address,value)
                ##print(self.Memory.readWord(address))
            except:
                return "fail"

    def run(self):
        self.printRegisters()
        while self.nextIR() != 0:
            self.fetch()

    def fetch(self): 
        #print(self.RDQueue)
        self.fetch_run = True
        self.IR = self.nextIR()
        self.IR = BitArray(int = self.IR, length = 32).bin
        #print("IR:"+str(self.IR))
        self.PC = self.PC + 4
        #self.decode()
    
    def decode(self):
        self.decode_run = True
        try:
            self.preload = self.decode_buffer['load']
        except:
            self.preload = False
        self.decode_buffer = {'mem_enable' : '-1', 'RD' : '-1', 'muxY' : 0, 'load' : False}
        self.opcode = self.IR[25:32]
        #print("opcode:"+self.opcode)
        self.RB = 0
        format = self.checkFormat()
        #print("format:"+format)
        self.RS1 = '00000'
        self.RS2 = '00000'
        if format == "r":
            self.decodeR()
        elif format == "iORs":
            self.RS1 = self.IR[12:17]
            #print("RS1:"+self.RS1)
            self.RA = self.RegisterFile.readA(self.RS1)
            #print("RA:"+str(self.RA))
            self.funct3 = self.IR[17:20]
            #print("funct3:"+self.funct3)
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
    
    def alu(self):
        self.alu_run = True
        if self.do_dataForwarding:
            reversedQueue = list(reversed(self.RDQueue))
            if self.preload:
                second = reversedQueue[1]
                if self.RS1 == second:
                    self.RA = self.RY
                    self.stalls_data = self.stalls_data + 1
                    self.cycle = self.cycle + 1
                if self.RS2 == second:
                    self.RB = self.RY
                    self.stalls_data = self.stalls_data + 1
                    self.cycle = self.cycle + 1
        operation = self.decode_buffer['op']
        self.alu_buffer = {'RD' : self.decode_buffer['RD'], 'RM' : self.RB}
        self.muxY = self.decode_buffer['muxY']
        self.memory_enable = self.decode_buffer['mem_enable']
        #print("OP:", operation)
        self.RZ = 0
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
                self.PC = self.PC - 8 + self.imm
                self.fetch_run = False
                self.stalls_control = self.stalls_control + 1
        elif operation == "bne":
            if self.RA != self.RB:
                self.PC = self.PC - 8 + self.imm
                self.fetch_run = False
                self.stalls_control = self.stalls_control + 1
        elif operation == "bge":
            if self.RA >= self.RB:
                self.PC = self.PC - 8 + self.imm
                self.fetch_run = False
                self.stalls_control = self.stalls_control + 1
        elif operation == "blt":
            if self.RA < self.RB:
                self.PC = self.PC - 8 + self.imm
                self.fetch_run = False
                self.stalls_control = self.stalls_control + 1
        elif operation == "auipc":
            self.RZ = self.PC - 8 + self.imm
        elif operation == "jal":
            self.PC_temp = self.decode_buffer['PC_temp']
            #self.PC = self.PC - 4 + self.imm 
        elif operation == "jalr":
            self.PC_temp = self.decode_buffer['PC_temp']
            #self.PC = self.RA + self.imm
        elif operation == "slli":
            self.RZ = BitArray(int=self.RA, length=32) << self.imm
            self.RZ = self.RZ.int
        elif operation == "srli":
            self.RZ = BitArray(int=self.RA, length=32) >> self.imm
            self.RZ = self.RZ.int
        elif operation == "srai":
            self.RZ = self.RA >> self.imm
        elif operation == "or":
            if self.muxB == 0:
                self.RZ = self.RA | self.RB
            elif self.muxB == 1:
                self.RZ = self.RA | self.imm
        elif operation == "and":
            if self.muxB == 0:
                self.RZ = self.RA & self.RB
            elif self.muxB == 1:
                self.RZ = self.RA & self.imm
        elif operation == "xor":
            if self.muxB == 0:
                self.RZ = self.RA ^ self.RB
            elif self.muxB == 1:
                self.RZ = self.RA ^ self.imm
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
            if self.muxB == 0:
                self.RZ = 1 if self.RA < self.RB else 0                 #slt
            elif self.muxB == 1:
                self.RZ = 1 if self.RA < self.imm else 0                #slti
        elif operation == "sltu":
            if self.muxB == 0:
                self.RA = BitArray(int = self.RA, length = 32).uint
                self.RB = BitArray(int = self.RB, length = 32).uint
                self.RZ = 1 if self.RA < self.RB else 0                 #sltu
            elif self.muxB == 1:
                self.RA = BitArray(int = self.RA, length = 32).uint
                self.imm = BitArray(int = self.imm, length = 32).uint
                self.RZ = 1 if self.RA < self.imm else 0                #sltiu
            
        #self.memAccess()
        
    def memAccess(self):
        self.memAccess_run = True
        self.RD = self.alu_buffer['RD']
        self.RM = self.alu_buffer['RM']
        if self.memory_enable != '-1':
            self.total_data_ins = self.total_data_ins + 1
            if self.memory_enable == "lw":
                self.data = self.Memory.readWord(self.RZ)           #lw
            elif self.memory_enable == "lb":
                self.data = self.Memory.readByte(self.RZ)           #lb
            elif self.memory_enable == "lh":
                self.data = self.Memory.readDoubleByte(self.RZ)     #lh
            elif self.memory_enable == "lbu":
                self.data = self.Memory.readUnsignedByte(self.RZ)   #lbu
            elif self.memory_enable == "lhu":
                self.data = self.Memory.readUnsignedDoubleByte(self.RZ)     #lhu
            elif self.memory_enable == "sw":                        #sw
                self.Memory.writeWord(self.RZ,self.RM)
                #print('RM and RZ : '+str(self.RM)+' '+str(self.RM))
            elif self.memory_enable == "sb":                        #sb
                self.Memory.writeByte(self.RZ,self.RM)
                #print('RM and RZ : '+str(self.RM)+' '+str(self.RM))
            elif self.memory_enable == "sh":                        #sh
                self.Memory.writeDoubleByte(self.RZ, self.RM)
                #print('RM and RZ : '+str(self.RM)+' '+str(self.RM))
        #writing in  muxY
        if self.muxY == 0:
            self.RY = self.RZ
        elif self.muxY == 1:
            self.RY = self.data
        elif self.muxY == 2:
            self.RY = self.PC_temp
        #print("muxY: "+str(self.muxY))
        #print("RY: "+str(self.RY))
        #self.writeReg()

    def writeReg(self):
        self.total_ins = self.total_ins + 1
        #print("in write RD: "+self.RD)
        #print("in write RY: "+str(self.RY))
        if self.RD != '-1':
            self.RegisterFile.writeC(self.RD, self.RY)
        try:
            self.RDQueue = self.RDQueue[1:]
        except:
            print('Queue Empty!')

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
        #print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        #print("RS2:"+self.RS2)
        RD = self.IR[20:25] 
        #print("RD:"+RD)
        self.RA = self.RegisterFile.readA(self.RS1)
        #print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        #print("RB:"+str(self.RB))
        if self.RS1 in self.RDQueue or self.RS2 in self.RDQueue:
            if self.do_dataForwarding:
                reversedQueue = list(reversed(self.RDQueue))
                first = reversedQueue[0]
                if self.RS1 == first:
                    self.RA = self.RZ
                    self.was_data_hazard = True
                if self.RS2 == first:
                    self.RB = self.RZ
                    self.was_data_hazard = True
                try:
                    second = reversedQueue[1]
                    if first != second:
                        if self.RS1 == second:
                            self.RA = self.RY
                            self.was_data_hazard = True
                        if self.RS2 == second:
                            self.RB = self.RY
                            self.was_data_hazard = True
                except:
                    print('not applicable!')
            else:
                self.was_data_hazard = True
                self.decode_run = False
                self.PC = self.PC - 4
                #print('Stalling!')
                self.stalls_data = self.stalls_data + 1
                return
        if self.was_data_hazard:
            self.data_hazards = self.data_hazards + 1
            self.was_data_hazard = False
        self.decode_buffer['RD'] = RD
        self.RDQueue.append(RD)
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        self.funct7 = self.IR[0:7]
        #self.muxY=0
        self.total_alu_ins = self.total_alu_ins + 1
        if self.funct3 == "000" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("add")                 #add
        elif self.funct3 == "000" and self.funct7 == "0000001":
            self.decode_buffer['op'] = ("mul")                 #mul
        elif self.funct3 == "110" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("or")                  #or
        elif self.funct3 == "111" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("and")                 #and
        elif self.funct3 == "100" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("xor")                 #xor
        elif self.funct3 == "000" and self.funct7 == "0100000":
            self.decode_buffer['op'] = ("sub")                 #sub
        elif self.funct3 == "001" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("sll")                 #sll
        elif self.funct3 == "010" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("slt")                 #slt
        elif self.funct3 == "011" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("sltu")                #sltu
        elif self.funct3 == "101" and self.funct7 == "0000000":
            self.decode_buffer['op'] = ("srl")                 #srl
        elif self.funct3 == "101" and self.funct7 == "0100000":
            self.decode_buffer['op'] = ("sra")                 #sra
        elif self.funct3 == "100" and self.funct7 == "0000001":
            self.decode_buffer['op'] = ("div")                 #div
        elif self.funct3 == "110" and self.funct7 == "0000001":
            self.decode_buffer['op'] = ("rem")                 #rem


    def decodeI(self):
        #print("I-format")
        self.imm = BitArray(bin = self.IR[0:12]).int
        #print("imm:"+str(self.imm))
        RD = self.IR[20:25] 
        self.RS1 = self.IR[12:17]
        if self.RS1 in self.RDQueue:
            if self.do_dataForwarding:
                reversedQueue = list(reversed(self.RDQueue))
                first = reversedQueue[0]
                if self.RS1 == first:
                    self.RA = self.RZ
                    self.was_data_hazard = True
                try:
                    second = reversedQueue[1]
                    if first != second:
                        if self.RS1 == second:
                            self.RA = self.RY
                            self.was_data_hazard = True
                except:
                    print('not applicable!')
            else:
                self.was_data_hazard = True
                self.decode_run = False
                self.PC = self.PC - 4
                #print('Stalling!')
                self.stalls_data = self.stalls_data + 1
                return
        if self.was_data_hazard:
            self.data_hazards = self.data_hazards + 1
            self.was_data_hazard = False
        #print("RD:"+RD)
        self.decode_buffer['RD'] = RD
        self.RDQueue.append(RD)
        self.muxB = 1
        if self.opcode == "0010011" and self.funct3 == "000":
            #self.muxY = 0
            self.total_alu_ins = self.total_alu_ins + 1
            self.decode_buffer['op'] = 'add'                 #addi
        elif self.opcode == "0000011" and (self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001" or self.funct3 == "100" or self.funct3 == "101"):
            #self.muxY = 1
            self.decode_buffer['muxY'] = 1
            #self.memory_enable = True
            self.decode_buffer['load'] = True
            self.decode_buffer['op'] = 'add'
            if self.funct3 == "010":
                self.decode_buffer['mem_enable'] = 'lw'     #lw
            elif self.funct3 == "000":
                self.decode_buffer['mem_enable'] = 'lb'     #lb
            elif self.funct3 == "001":
                self.decode_buffer['mem_enable'] = 'lh'     #lh
            elif self.funct3 == "100":
                self.decode_buffer['mem_enable'] = 'lbu'    #lbu
            elif self.funct3 == "101":
                self.decode_buffer['mem_enable'] = 'lhu'    #lhu
        elif self.opcode == "1100111" and self.funct3 == "000":
            self.total_control_ins = self.total_control_ins + 1
            self.decode_buffer['muxY'] = 2
            self.decode_buffer['op'] = 'jalr'               #jalr 
            self.decode_buffer['PC_temp'] = self.PC
            self.PC = self.RA + self.imm
        elif self.opcode == "0010011":
            self.total_alu_ins = self.total_alu_ins + 1
            if self.funct3 == "001":
                self.funct7 = self.IR[0:7]
                self.imm = BitArray(bin = self.IR[7:12]).uint
                if self.funct7 == "0000000":
                    self.decode_buffer['op'] = 'slli'        #slli
            elif self.funct3 == "101":
                self.funct7 = self.IR[0:7]
                self.imm = BitArray(bin = self.IR[7:12]).uint
                if self.funct7 == "0000000":
                    self.decode_buffer['op'] = 'srli'     #srli
                if self.funct7 == "0100000":
                    self.decode_buffer['op'] = 'srai'     #srai (arithmetic right shift)
            elif self.funct3 == "010":
                self.decode_buffer['op'] = 'slti'         #slti
            elif self.funct3 == "011":
                self.decode_buffer['op'] = 'sltiu'        #sltiu 
            elif self.funct3 == "100":
                self.decode_buffer['op'] = 'xori'         #xori
            elif self.funct3 == "110":
                self.decode_buffer['op'] = 'ori'          #ori
            elif self.funct3 == "111":
                self.decode_buffer['op'] = 'andi'         #andi



    
    def decodeS(self):
        self.RS1 = self.IR[12:17]
        #print("S-format")
        self.RS2 = self.IR[7:12]
        #print("RS2:"+self.RS2)
        self.RB = self.RegisterFile.readB(self.RS2)
        #print("RB:"+str(self.RB))
        if self.RS1 in self.RDQueue or self.RS2 in self.RDQueue:
            if self.do_dataForwarding:
                reversedQueue = list(reversed(self.RDQueue))
                first = reversedQueue[0]
                if self.RS1 == first:
                    self.RA = self.RZ
                    self.was_data_hazard = True
                if self.RS2 == first:
                    self.RB = self.RZ
                    self.was_data_hazard = True
                try:
                    second = reversedQueue[1]
                    if first != second:
                        if self.RS1 == second:
                            self.RA = self.RY
                            self.was_data_hazard = True
                        if self.RS2 == second:
                            self.RB = self.RY
                            self.was_data_hazard = True
                except:
                    print('not applicable!')
            else:
                self.was_data_hazard = True
                self.decode_run = False
                self.PC = self.PC - 4
                #print('Stalling!')
                self.stalls_data = self.stalls_data + 1
                return
        if self.was_data_hazard:
            self.data_hazards = self.data_hazards + 1
            self.was_data_hazard = False
        self.RDQueue.append('-1')
        imm1 = self.IR[0:7]
        imm2 = self.IR[20:25]
        #self.write_enable = False
        self.imm = BitArray(bin = imm1+imm2).int
        if self.funct3 == "010" or self.funct3 == "000" or self.funct3 == "001":
            #self.RM = self.RB
            self.muxB = 1
            #self.memory_enable = True
            self.decode_buffer['op'] = 'add'
            if self.funct3 == "010":                        #sw
                self.decode_buffer['mem_enable'] = 'sw'
            elif self.funct3 == "000":                      #sb
                self.decode_buffer['mem_enable'] = 'sb'
            elif self.funct3 == "001":                      #sh
                self.decode_buffer['mem_enable'] = 'sh'

    def decodeSB(self):
        self.RS1 = self.IR[12:17]
        #print("RS1:"+self.RS1)
        self.RS2 = self.IR[7:12]
        #print("RS2:"+self.RS2)
        self.RA = self.RegisterFile.readA(self.RS1)
        #print("RA:"+str(self.RA))
        self.RB = self.RegisterFile.readB(self.RS2)
        #print("RB:"+str(self.RB))
        if self.RS1 in self.RDQueue or self.RS2 in self.RDQueue:
            if self.do_dataForwarding:
                reversedQueue = list(reversed(self.RDQueue))
                first = reversedQueue[0]
                if self.RS1 == first:
                    self.RA = self.RZ
                    self.was_data_hazard = True
                if self.RS2 == first:
                    self.RB = self.RZ
                    self.was_data_hazard = True
                try:
                    second = reversedQueue[1]
                    if first != second:
                        if self.RS1 == second:
                            self.RA = self.RY
                            self.was_data_hazard = True
                        if self.RS2 == second:
                            self.RB = self.RY
                            self.was_data_hazard = True
                except:
                    print('not applicable!')
            else:
                self.was_data_hazard = True
                self.decode_run = False
                self.PC = self.PC - 4
                #print('Stalling!')
                self.stalls_data = self.stalls_data + 1
                return
        if self.was_data_hazard:
            self.data_hazards = self.data_hazards + 1
            self.was_data_hazard = False
        self.RDQueue.append('-1')
        self.muxB = 0
        self.funct3 = self.IR[17:20]
        imm1 = self.IR[0]
        imm2 = self.IR[24]
        imm3 = self.IR[1:7]
        imm4 = self.IR[20:24]
        #self.write_enable = False
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.total_control_ins = self.total_control_ins + 1
        self.control_hazards = self.control_hazards + 1
        
        if self.funct3 == "000":
            #print("going to beq")
            self.decode_buffer['op'] = 'beq'         #beq
        elif self.funct3 == "101":
            self.decode_buffer['op'] = 'bge'         #bge
        elif self.funct3 == "100":
            self.decode_buffer['op'] = 'blt'         #blt    
        elif self.funct3 == "001":
            self.decode_buffer['op'] = 'bne'         #bne
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").uint     #for unsigned operations
        #print(str(self.imm))
        if self.funct3 == "111":
            self.decode_buffer['op'] = 'bge'         #bgeu
        elif self.funct3 == "110":
            self.decode_buffer['op'] = 'blt'         #bltu

        
    def decodeU(self):
        RD = self.IR[20:25] 
        #print("RD:"+RD)
        self.decode_buffer['RD'] = RD
        self.RDQueue.append(RD)
        imm1 = self.IR[0:20]
        imm2 = "000000000000"
        self.imm = BitArray(bin = imm1 + imm2).int
        #print('IMM : '+str(self.imm))
        self.total_alu_ins = self.total_alu_ins + 1
        if self.opcode == "0110111":
            self.RA = 0
            self.RB = 0
            self.muxB = 1
            self.decode_buffer['op'] = 'add'         #lui
        else:
            self.decode_buffer['op'] = 'auipc'       #auipc

    def decodeUJ(self):
        self.total_control_ins = self.total_control_ins + 1
        self.RA = 0
        self.RB = 0
        RD = self.IR[20:25] 
        #print("RD:"+RD)
        self.decode_buffer['RD'] = RD
        self.RDQueue.append(RD)
        imm1 = self.IR[0]
        imm2 = self.IR[12:20]
        imm3 = self.IR[11]
        imm4 = self.IR[1:11]
        self.imm = BitArray(bin = imm1 + imm2 + imm3 + imm4 + "0").int
        self.decode_buffer['muxY'] = 2
        self.decode_buffer['op'] = 'jal'                    #jal
        self.decode_buffer['PC_temp'] = self.PC
        self.PC = self.PC - 4 + self.imm
        

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

  