from execute import execute

Execute = execute("code.mc")
Execute.run()
print("Memory:")
Execute.printMemory()
print("Registers:")
Execute.printRegisters()