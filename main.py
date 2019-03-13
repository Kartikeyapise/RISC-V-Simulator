from execute import execute

Execute = execute()
Execute.assemble("code.mc")
Execute.run()
print("Memory:")
Execute.printMemory()
print("Registers:")
Execute.printRegisters()