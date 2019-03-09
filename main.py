from registers import register
from memory import memory

RegisterFile = register()
Memory = memory()

MC = open("code.mc","r")
for line in MC:
    address,value = line.split()
    Memory.writeMEMORY(address,value)
    print(Memory.readMEMORY(address))



Memory.writeMEMORY("0x0",5)
Memory.readMEMORY("0x0")

RegisterFile.writeC("00001",2)
print(RegisterFile.readA("00001"))