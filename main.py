from registers import register

RegisterFile = register()

RegisterFile.writeC("x0",0x7e87)
print(RegisterFile.readA("x31"))