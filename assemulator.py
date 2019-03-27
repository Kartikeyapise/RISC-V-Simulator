from bitstring import BitArray


mnemonic_fmt = {
    'lb':['I', '0000011', '000'],
    'lh':['I', '0000011', '001'],
    'lw':['I', '0000011', '010'],
    'ld':['I', '0000011', '011'],
    'lbu':['I', '0000011', '100'],
    'lhu':['I', '0000011', '101'],
    'lwu':['I', '0000011', '110'],
    'fence':['I', '0001111', '000'],
    'fence.i':['I', '0001111', '001'],
    'addi':['I', '0010011', '000'],
    'slli':['I', '0010011', '001', '0000000'],
    'slti':['I', '0010011', '010'],
    'sltiu':['I', '0010011', '011'],
    'xori':['I', '0010011', '100'],
    'srli':['I', '0010011', '101', '0000000'],
    'srai':['I', '0010011', '101', '0100000'],
    'ori':['I', '0010011', '110'],
    'andi':['I', '0010011', '111'],
    'auipc':['U', '0010111'],
    'addiw':['I', '0011011', '000'],
    'slliw':['I', '0011011', '001', '0000000'],
    'srliw':['I', '0011011', '101', '0000000'],
    'sraiw':['I', '0011011', '101', '0100000'],
    'sb':['S', '0100011', '000'],
    'sh':['S', '0100011', '001'],
    'sw':['S', '0100011', '010'],
    'sd':['I', '0100011', '011'],
    'add':['R', '0110011', '000', '0000000'],
    'sub':['R', '0110011', '000', '0100000'],
    'mul':['R', '0110011', '000', '0000001'],
    'div':['R', '0110011', '100', '0000001'],
    'sll':['R', '0110011', '001', '0000000'],
    'slt':['R', '0110011', '010', '0000000'],
    'sltu':['R', '0110011', '011', '0000000'],
    'xor':['R', '0110011', '100', '0000000'],
    'srl':['R', '0110011', '101', '0000000'],
    'sra':['R', '0110011', '101', '0100000'],
    'or':['R', '0110011', '110', '0000000'],
    'and':['R', '0110011', '111', '0000000'],
    'lui':['U', '0110111'],
    'addw':['R', '0111011', '000', '0000000'],
    'subw':['R', '0111011', '000', '0100000'],
    'sllw':['R', '0111011', '001', '0000000'],
    'srlw':['R', '0111011', '101', '0000000'],
    'sraw':['R', '0111011', '101', '0100000'],
    'beq':['SB', '1100011', '000'],
    'bne':['SB', '1100011', '001', ],
    'blt':['SB', '1100011', '100'],
    'bge':['SB', '1100011', '101'],
    'bltu':['SB', '1100011', '110'],
    'bgeu':['SB', '1100011', '111'],
    'jalr':['I', '1100111', '000'],
    'jal':['UJ', '1101111'],
    'ecall':['I', '1110011', '000', '000000000000'],
    'ebreak':['I', '1110011', '000', '000000000001'],
    'CSRRW':['I', '1110011', '001'],
    'CSRRS':['I', '1110011', '010'],
    'CSRRC':['I', '1110011', '011'],
    'CSRRWI':['I', '1110011', '101'],
    'CSRRSI':['I', '1110011', '110'],
    'CSRRCI':['I', '1110011', '111'],
}

def R_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    funct7=mnemonic_fmt[words[0]][3]

    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in R_type in ',words)
    try:
        rs1='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rs1\' in R_type in ',words)
    try:
        rs2='{0:05b}'.format(int(words[3][1:]))
    except:
        print('problem in getting \'rs2\' in R_type in ',words)
    try:
        machine_code=funct7 + rs2 + rs1 + funct3 + rd + opcode
        return machine_code
    except:
        print('problem in generating machine_code in R_type in ',words)

def I_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in I_type in ',words)
    try:
        rs1='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rd\' in I_type in ',words)
    imm=''

    if(words[3][0:2] == '0x'):
        try:
            imm='{0:012b}'.format(int(words[3][2:], 16))
        except:
            print('problem in getting hexadecimal immediate value in I_type in ',words)

    elif(words[3][0:2] == '0b'):
        try:
            imm='{0:012b}'.format(int(words[3][2:], 2))
        except:
            print('problem in getting binary immediate value in I_type in ',words)

    else:
        try:
            imm=BitArray(int=int(words[3]), length=12).bin
        except:
            print('problem in getting other type of immediate value in I_type in ',words)

    try:
        machine_code = imm + rs1 + funct3 + rd + opcode
        return machine_code
    except:
        print('problem in generating machine code in I_type in ',words)

def S_type(words):
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rs2='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rs2\' in S_type in ',words)

    temp_str=''
    # third word should be in the format like 986(x7)
    for i in range(2, len(words)):
        temp_str += words[i]

    offset = temp_str[0:temp_str.find('(')]
    # handling of -ve offset left
    try:
        rs1=int(temp_str[temp_str.find('(')+2:temp_str.find(')')])
        rs1='{0:05b}'.format(rs1)
    except:
        print('problem in getting \'rs1\' in S_type in ',words)

    imm=''
    if(offset[0:2] == '0x'):
        try:
            imm='{0:012b}'.format(int(offset[2:], 16))
        except:
            print('problem in getting hexadecimal immediate value in S_type in ',words)

    elif(offset[0:2] == '0b'):
        try:
            imm='{0:012b}'.format(int(offset[2:], 2))
        except:
            print('problem in getting binary immediate value in S_type in ',words)
        
    else:
        try:
            imm=BitArray(int=int(offset), length=12).bin
        except:
            print('problem in getting other type of immediate value in S_type in ',words)

    try:
        machine_code = imm[0:7] + rs2 + rs1 + funct3 + imm[7:12] + opcode
        return machine_code
    except:
        print('problem in generating machine_code in S_type in ',words)


def SB_type(words, label_offset):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    try:
        rs1='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rs1\' in SB_type in ',words)

    try:
        rs2='{0:05b}'.format(int(words[2][1:]))
    except:
        print('problem in getting \'rs2\' in SB_type in ',words)

    try:
        imm=BitArray(int=int(str(label_offset)), length=12).bin
    except:
        print('problem in generating immediate in SB_type in ',words)

    try:
        machine_code = imm[0] + imm[2:8] + rs2 + rs1 + funct3 + imm[8:12] + imm[1] + opcode
        return machine_code
    except:
        print('problem in generating machine_code in SB_type in ',words)

def U_type(words):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in U_type in ',words)
    var_address = ''
    
    if(words[2][0:2] == '0x'):
        try:
            var_address='{0:020b}'.format(int(words[2][2:], 16))
        except:
            print('problem in getting hexadecimal var_address in U_type in ',words)

    elif(words[2][0:2] == '0b'):
        try:
            var_address='{0:020b}'.format(int(words[2][2:], 2))
        except:
            print('problem in getting binary var_address in U_type in ',words)
        
    else:
        try:
            var_address=BitArray(int=int(words[2]), length=20).bin
        except:
            print('problem in getting other type of var_address in U_type in ',words)

    try:
        machine_code = var_address + rd + opcode
        return machine_code
    except:
        print('problem in generating machine_code in U_type in ',words)

def UJ_type(words, label_address):
    opcode=mnemonic_fmt[words[0]][1]
    try:
        rd='{0:05b}'.format(int(words[1][1:]))
    except:
        print('problem in getting \'rd\' in UJ_type in ',words)

    try:
        label_address='{0:021b}'.format(int(label_address))
    except:
        print('problem in getting label_address in UJ_type in ',words)
    try:
        machine_code = label_address[0] + label_address[10:20] + label_address[9] + label_address[1:9] + rd + opcode ##to be corrected and checked
        return machine_code
    except:
        print('problem in generating machine_code in UJ_type in ',words)
def mc_generator(asm_text=""):
    file_write= open("write_file.mc","w")
    
    return_txt=''
    if asm_text=="":
        file_read = open("read_file.asm","r")
        if file_read.mode=='r':
            asm_code=file_read.read()
        # .data and .text part of the code can come in any order
    else:
        asm_code=asm_text
    dictionary = {}                                                                 #Declaration of a dictionary(to be used later as reference to memory addresses)
    if(asm_code.find('.data') >= 0):
        data = ''
        text = ''
        
        if asm_code.find(".data") < asm_code.find('.text') :
            data = asm_code[asm_code.find(".data")+5:asm_code.find(".text")].strip()        #Sheky have looked into for 5
            text = asm_code[asm_code.find('.text')+5:].strip()
        else:
            text = asm_code[asm_code.find('.text')+5:asm_code.find('.data')].strip()
            data = asm_code[asm_code.find('.data')+5:].strip()

        #Handling of data part of code starts here
        instructions = data.split('\n')
        data_address = int("0x10000000", 0)
        for i in range(len(instructions)):
            if(instructions[i]==''):                                                    #removal of '\n's
                del instructions[i]
            else:
                dictionary[instructions[i][:instructions[i].find(':')].strip()] = hex(data_address)
                if instructions[i].find('.word')>=0:
                    for word in (instructions[i][instructions[i].find('.word'):].strip()).split():
                        try:
                            return_txt+=str(hex(data_address))+' '+str(hex(int(word)))+'\n'
                            data_address=data_address+4
                        except: pass
                if instructions[i].find('.byte')>=0:
                    for byte in (instructions[i][instructions[i].find('.byte'):].strip()).split():
                        try:
                            return_txt+=str(hex(data_address))+' '+str(hex(int(byte)))+'\n'
                            data_address=data_address+1
                        except: pass
                #file_write.write(hex(data_address)+' \n')
        print(instructions)
        print(dictionary)

        # Handling of data part ends here
        #registers = {'x0':0, 'x1':0, 'x2':2147483632, 'x3':268435456, 'x4':0, 'x5':0, 'x6':0, 'x7':0, 'x8':0, 'x9':0, 'x10':0, 'x11':0, 'x12':0, 'x13':0, 'x14':0, 'x15':0, 'x16':0, 'x17':0, 'x18':0, 'x19':0, 'x20':0, 'x21':0, 'x22':0, 'x23':0, 'x24':0, 'x25':0, 'x26':0, 'x27':0, 'x28':0, 'x29':0, 'x30':0, 'x31':0}
        #print(len(registers))
        #print(registers)
    if(asm_code.find('.data') == -1):
        text=asm_code
    instructions = list(filter(bool, text.splitlines()))
    # Assuming there is no extra '\n' in the text part of the code
    n=len(instructions)
    i=0
    
    label_position={}
    while(i<n):
        instructions[i]=instructions[i].strip()
        a=instructions[i].find('#')
        if(a==0):
            del instructions[i]
            n=n-1
            continue
        elif(a>0):
            instructions[i]=instructions[i][0:a]

        k=instructions[i].find(':')
        if (k > 0):
            instructions[i]=instructions[i].strip()
            label=instructions[i][:k]
            if(len(instructions[i][k+1:]) > 0):
                instructions[i]=instructions[i][k+1:]
            else:
                del instructions[i]
                i=i-1
                n=n-1
            label_position[label]=i
        i=i+1

    pc=0

    for i in range(0, n):
        instructions[i]=instructions[i].replace(',', ' ')
        words=instructions[i].split()

        if(mnemonic_fmt[words[0]][0] == 'R'):
            return_txt+=hex(pc)+' '
            return_txt+='0x' + '{0:08x}'.format(int(R_type(words), 2)) + '\n'
        elif(mnemonic_fmt[words[0]][0] == 'I'):
            return_txt+=hex(pc)+' '
            ###file_write.write(hex(pc)+' ')
            if(words[0] == 'lb' or words[0] == 'lw'):
            #     pass
            # elif(words[0] == 'lw'):
                #if using a data label:
                
                if words[2] in dictionary:
                    words_extra=['auipc',words[1],'0b00010000000000000000']
                    return_txt+='0x' + '{0:08x}'.format(int(U_type(words_extra), 2)) + '\n'
                    new_offset=BitArray(int=int(dictionary[words[2]], 16)-int('0x10000000', 16)-pc, length=12).bin
                    words[2]=words[1]
                    words.append('0b'+new_offset)
                    pc=pc+4
                    return_txt+=hex(pc)+' '
                    #print('0x' + '{0:08x}'.format(int(I_type(words), 2)))
                    return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2)) + '\n'
                ##if not using a data label, instead loading as offset + register:
                else:
                    temp_str=''
                    # third word should be in the format like 986(x7)
                    for i in range(2, len(words)):
                        temp_str += words[i]
                    offset = temp_str[0:temp_str.find('(')]
                    # handling of -ve offset left
                    rs2=temp_str[temp_str.find('(')+1:temp_str.find(')')]
                    words=[words[0],words[1],rs2,offset]
                    return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2))+'\n'
            else:
                return_txt+='0x' + '{0:08x}'.format(int(I_type(words), 2))+'\n'
                ###file_write.write('0x' + '{0:08x}'.format(int(I_type(words), 2)))
                ###file_write.write('\n')
        elif(mnemonic_fmt[words[0]][0] == 'S'):
            return_txt+=hex(pc)+' '
            return_txt+='0x' + '{0:08x}'.format(int(S_type(words), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'SB'):
            var=(label_position[words[3]])*4-pc
            #print('0x' + '{0:08x}'.format(int(SB_type(words, var), 2)))
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(SB_type(words, var)))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'U'):
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(U_type(words), 2))+'\n'
        elif(mnemonic_fmt[words[0]][0] == 'UJ'):
            return_txt+=hex(pc)+' '+'0x' + '{0:08x}'.format(int(UJ_type(words, '10101'), 2))
        pc=pc+4
    if(asm_text==''):
        file_write.write(return_txt)
    else:
        return return_txt
if __name__ == "__main__":
    abc=mc_generator('''.data
var: .word 10
var2: .word 11



.text
lw x5 var
add x6 x5 x0''')