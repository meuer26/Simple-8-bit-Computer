from time import sleep
import itertools
import random
from scipy.stats import entropy


# These are the global objects
ramByteArray = bytearray(256)
aRegister = bytearray(1)
xRegister = bytearray(1)
yRegister = bytearray(1)
statusRegister = bytearray(1)
instructionRegister = bytearray(1)
operandRegister = bytearray(1)
pcRegister = bytearray(1)
clockTicks = 0
maxClockTicks = 10000


def printRegs():
    print("\nClock Ticks: \t", clockTicks)
    print("RAM (bytes): \t", len(ramByteArray), "(", hex(len(ramByteArray)), ")")
    print("A Reg: \t\t", aRegister.hex())
    print("X Reg: \t\t", xRegister.hex())
    print("Y Reg: \t\t", yRegister.hex())
    print("Status Reg: \t", bin(int(statusRegister.hex(), 16)))
    print("Instrc Reg:     ", instructionRegister.hex())
    print("Operand Reg:    ", operandRegister.hex())
    print("PC Reg: \t", pcRegister.hex())


def stepIncrement():
    global pcRegister
    global instructionRegister
    global operandRegister
    global ramByteArray
    global clockTicks

    # Halt if max clock ticks is reached -- infinite loop
    if clockTicks >= maxClockTicks:
        print("\nMax clock ticks reached; forcing termination...")
        halt()

    #printRegs()
    

    # Fetching the Instruction or Operand
    # check to see if the PC register value is even or odd
    # even values are instructions; odd values are operands
    if (int(pcRegister.hex(), 16) % 2) == 0:
        nextInstruction = ramByteArray[int(pcRegister.hex(), 16)]
        instructionRegister = nextInstruction.to_bytes(length=1, byteorder='big')

    else:
        nextOperand = ramByteArray[int(pcRegister.hex(), 16)]
        operandRegister = nextOperand.to_bytes(length=1, byteorder='big')

        if instructionRegister[0] == 0xc:
            opcodeSTA()

        if instructionRegister[0] == 0xb:
            opcodeJMP()
        
        if instructionRegister[0] == 9:
            opcodeTAX()

        if instructionRegister[0] == 8:
            clearCarry()
        
        if instructionRegister[0] == 7:
            opcodeBCS()

        if instructionRegister[0] == 5:
            setCarry()

        if instructionRegister[0] == 4:
            opcodeADC()
        
        if instructionRegister[0] == 3:
            opcodeLDA()
        
        if instructionRegister[0] == 2:
            opcodeLDY()

        if instructionRegister[0] == 1:
            opcodeLDX()


    # Increment clock ticks and PC
    if int(pcRegister.hex(), 16) == (len(ramByteArray) -1):
        print("\n\nReached the end of RAM")
        halt()

    clockTicks += 1
    pcRegisterHex = int(pcRegister.hex(), 16)
    pcRegisterHex = pcRegisterHex + 1
    pcRegister = pcRegisterHex.to_bytes(length=1, byteorder='big')


def opcodeBCS():
    global operandRegister
    global statusRegister
    global pcRegister
    
    if int(statusRegister.hex(), 16) == 1:
        pcRegister = operandRegister
        stepIncrement()

    else:
        return


def opcodeSTA():
    global aRegister
    global operandRegister
    global ramByteArray

    ramList = list(ramByteArray)
    ramList[int(operandRegister.hex(), 16)] = int(aRegister.hex(), 16)
    ramByteArray = bytearray(ramList)


def opcodeADC():
    global aRegister
    global xRegister
    global yRegister

    aRegisterHex = int(aRegister.hex(), 16)
    xRegisterHex = int(xRegister.hex(), 16)
    yRegisterHex = int(yRegister.hex(), 16)

    aRegisterHex = xRegisterHex + yRegisterHex

    if aRegisterHex >= 255:
        aRegisterHex = aRegisterHex - 255

    aRegister = aRegisterHex.to_bytes(length=1, byteorder='big')



def opcodeJMP():
    global operandRegister
    global pcRegister

    pcRegisterHex = int(operandRegister.hex(), 16)
    pcRegister = pcRegisterHex.to_bytes(length=1, byteorder='big')
    stepIncrement()


def opcodeLDA():
    global operandRegister
    global aRegister
    
    aRegister = operandRegister


def clearCarry():
    global statusRegister

    newCarry = 0
    statusRegister = newCarry.to_bytes(length=1, byteorder='big')


def setCarry():
    global statusRegister

    newCarry = 1
    statusRegister = newCarry.to_bytes(length=1, byteorder='big')


def opcodeTAX():
    global aRegister
    global xRegister

    xRegister = aRegister


def opcodeLDX():
    global operandRegister
    global xRegister

    xRegister = operandRegister


def opcodeLDY():
    global operandRegister
    global yRegister

    yRegister = operandRegister


def changePC():
    global pcRegister

    newPCRegister = int(input("Enter new PC value in hex: "), 16)
    pcRegister = newPCRegister.to_bytes(length=1, byteorder='big')


def reset():
    global clockTicks
    clockTicks = 0
    printRegs()


def halt(): 
    print("\nClock Ticks: ", clockTicks)
    print("The program halted...\n")
    #mainLoop()
    exit()


def assemble():
    global pcRegister
    global ramByteArray

    assembleAddress = int(input('Enter Mem Address in hex: '), 16)
    pcRegister = assembleAddress.to_bytes(length=1, byteorder='big')

    while True:
        inputByte = int(input('Input Byte in hex (fff to exit): '), 16)
        if inputByte == 0xFFF:
            changePC()
            return
    
        else:

            ramList = list(ramByteArray)
            ramList[int(pcRegister.hex(), 16)] = inputByte
            ramByteArray = bytearray(ramList)
        
            pcRegisterHex = int(pcRegister.hex(), 16)
            pcRegisterHex = pcRegisterHex + 1
            pcRegister = pcRegisterHex.to_bytes(length=1, byteorder='big')


def displayMem():

    startLocation = 0
    sectorSize = len(ramByteArray)
    lines = 16
    iterations = int((sectorSize / lines))

    for x in range(0, iterations):
        startIndex = x * lines
        endIndex = (x + 1) * lines
        line = [str('%02X' %i) for i in ramByteArray[startIndex:endIndex]]
        strLine = '0x%02X    ' %(startLocation+startIndex) + str(line)
        print(strLine)


def run():

    speed = 0.000001
    #speed = float(input("Enter speed as fraction of sec (e.g., 0.1): "))

    while True:
        stepIncrement()
        sleep(speed)


def saveMemory():
    fileName = input("Enter the file name: ")

    fileRAM = open(fileName, "wb")
    fileRAM.write(ramByteArray)
    fileRAM.close()


def loadMemory():
    global ramByteArray

    fileName = input("Enter the file name: ")
    fileRAM = open(fileName, "rb")
    # ramByteArray = fileRAM.read()

    ramList = list(fileRAM.read())
    ramByteArray = bytearray(ramList)

    fileRAM.close()



def mainLoop(programByteArray):
    global ramByteArray

    ramByteArray = programByteArray

    run()



# ------------------------------------------------------------------------------------

opcodeList = [0xc, 0xb, 9, 8, 7, 5, 4, 3, 2, 1]
operandList = list(range(1, 255))
symbolSize = 126    # this cannot be higher than 126 due to the four zeros in the beginning
numberOfPrograms = 1

#randomList = [0, 0, 0, 0]

for y in range(0, numberOfPrograms):
    randomByteArray = bytearray(b'\x00\x00\x00\x00')
    for x in range(0, symbolSize):
        #randomList = [0, 0, 0, 0]
        opcode = random.choice(opcodeList)
        randomByteArray.append(opcode)
        operand = random.choice(operandList)
        randomByteArray.append(operand)
        
    #print('Entropy', entropy(randomList))
    print(randomByteArray)
    print('\nEntropy', entropy(randomByteArray))
    mainLoop(randomByteArray)