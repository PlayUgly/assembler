"""Assembler as defined in chapter 6 of The Elements of Computing Systems:
Building a Modern Computer From First Principles by Noam Nisan
and Shimon Schocken.

The assembler translates Hack assembly code to the Hack binary language
specified in chapter 4.

This program accepts one argument: path/filename.asm.  It outputs a single
file filename.hack to the same directory.
"""

import sys

def SymbolIsValid(symbol):
    """Return True if an asm symbol does not contain any invalid characters."""

    if symbol[0].isdigit():
        return False

    else:
        for character in symbol:
            if character.isalpha() or \
               character.isdigit() or \
               character == "_" or \
               character == "." or \
               character == "$" or \
               character == ":":
                    pass
            else:
                    return False

        return True


def InitializeDestinationDictionary():
    """Relate the destination registers to a binary snippet with a dictionary"""

   destination = {
           "M"  :"001",
           "D"  :"010",
           "MD" :"011",
           "A"  :"100",
           "AM" :"101",
           "AD" :"110",
           "AMD":"111"
           } 

   return destination


def InitializeComputationDictionary():
    """Relate a computation to a binary snippet with a dictionary"""

    computation = {
            "0"     :"1110101010",
            "1"     :"1110111111",
            "-1"    :"1110111010",
            "D"     :"1110001100",
            "A"     :"1110110000",
            "!D"    :"1110001101",
            "!A"    :"1110110001",
            "-D"    :"1110001111",
            "-A"    :"1110110011",
            "D+1"   :"1110011111",
            "A+1"   :"1110110111",
            "D-1"   :"1110001110",
            "A-1"   :"1110110010",
            "D+A"   :"1110000010",
            "D-A"   :"1110010011",
            "A-D"   :"1110000111",
            "D&A"   :"1110000000",
            "D|A"   :"1110010101",
            "M"     :"1111110000",
            "!M"    :"1111110001",
            "-M"    :"1111110011",
            "M+1"   :"1111110111",
            "M-1"   :"1111110010",
            "D+M"   :"1111000010",
            "D-M"   :"1111010011",
            "M-D"   :"1111000111",
            "D&M"   :"1111000000",
            "D|M"   :"1111010101"
            }

    return computation

    
def InitializeJumpsDictionary():
    """Relate a jump command to a binary snippet with a dictionary"""

    JMP = {
            "JGT":"001",
            "JEQ":"010",
            "JGE":"011",
            "JLT":"100",
            "JNE":"101",
            "JLE":"110",
            "JMP":"111"
            }

    return JMP


def InitializeSymbols():
    """Relate the default labels to a binary register address with a dictionary"""

    symbols = {
            "SP"    :"000000000000000",
            "LCL"   :"000000000000001",
            "ARG"   :"000000000000010",
            "THIS"  :"000000000000011",
            "THAT"  :"000000000000100",
            "R0"    :"000000000000000",
            "R1"    :"000000000000001",
            "R2"    :"000000000000010",
            "R3"    :"000000000000011",
            "R4"    :"000000000000100",
            "R5"    :"000000000000101",
            "R6"    :"000000000000110",
            "R7"    :"000000000000111",
            "R8"    :"000000000001000",
            "R9"    :"000000000001001",
            "R10"   :"000000000001010",
            "R11"   :"000000000001011",
            "R12"   :"000000000001100",
            "R13"   :"000000000001101",
            "R14"   :"000000000001110",
            "R15"   :"000000000001111",
            "SCREEN":"100000000000000",
            "KBD"   :"110000000000000"
            }

    return symbols


"""The main program converts assembly to binary in two steps.  First it reads
the .asm file, discards comments, strips whitespace, parses the assembly 
commands, and converts them into a list of binary commands.  Then it writes the 
binary commands to the outputPath.

If any invalid assembly lines are found, they are written to the screen along
with their line numbers, and the binary translation stops without creating a 
file.
"""

inputPath = sys.argv[1]
outputFilePath = inputPath[:-3] + "hack"

errors = []

with open(inputPath,"r") as f:
    lines = f.readlines()

lines = [x.strip() for x in lines]

computationDictionary = InitializeComputationDictionary()
destinationDictionary = InitializeDestinationDictionary()
jumpsDictionary = InitializeJumpsDictionary()
symbolsDictionary = InitializeSymbols()

fileLineNumber = 1
processedLineNumber = 0

errors = []

while processedLineNumber < len(lines):

    error = False
    message = ""

    #strip out comments
    commentStart = lines[processedLineNumber].find("//")

    if commentStart > -1:
        lines[processedLineNumber] = lines[processedLineNumber][0:commentStart]

    lines[processedLineNumber] = lines[processedLineNumber].strip()
    

    line = lines[processedLineNumber]

    if len(line) == 0:
        del lines[processedLineNumber]
        processedLineNumber -= 1
                
    elif line[0] == "@":
        address = line[1:len(line)]
        
        if not address.isdigit():
            if not SymbolIsValid(address):
                error = True
                message = "Invalid symbol name"

    elif line.count(";") > 1 or line.count("=") > 1:
        error = True
        message = "Too many operations"

    elif ";" in line:
        jump = line.split(";")

        if "=" in jump[0]:
            equation = jump[0].split("=")

            if equation[0] in destinationDictionary and equation[1] in computationDictionary and jump[1] in jumpsDictionary:
                pass

            else:
                error = True
                message = "Invalid operation"

        else:
            if jump[0] in computationDictionary and jump[1] in jumpsDictionary:
                pass

            else:
                error = True
                message = "Invalid operation"
                
    elif "=" in line:
        equation = line.split("=")
            
        if equation[0] in destinationDictionary and equation[1] in computationDictionary:
            pass
            #print(equation[0] + " " + computationDictionary[equation[0]] + "    " + equation[1] + " " + jumpsDictionary[equation[1]])

        else:
            error = True
            message = "Invalid operation"

    elif line[0] == "(" and line[-1] == ")":
        label = line[1:len(line) - 1]

        if label in symbolsDictionary:
            error = True
            message = "Duplicate label" 

        else:
            if SymbolIsValid(label):
                #print(label + " added")
                symbolsDictionary[label] = format(processedLineNumber, "015b")

                del lines[processedLineNumber]
                processedLineNumber -= 1
                
            else:
                error = True
                message = "Invalid label name"

    else:
        error = True
        message = "Invalid statement" 

    if error:
        errors.append(message + " in line " + str(fileLineNumber) + ": " + line)

    fileLineNumber += 1
    processedLineNumber += 1

if len(errors) > 0:
    for error in errors:
        print(error)

else:
    nextMemoryAddress = 16

    binaryInstructions=[]

    for line in lines:
        if line[0] == "@":
            address = line[1:len(line)]
        
            if address.isdigit():
                binaryInstructions.append("0" + format(int(address), "015b"))

            else:
                if not address in symbolsDictionary:
                    symbolsDictionary[address] = format(nextMemoryAddress, "015b")
                    nextMemoryAddress += 1

                binaryInstructions.append("0" + symbolsDictionary[address])

        elif ";" in line:
            jump = line.split(";")

            if "=" in jump[0]:
                equation = jump[0].split("=")

                binaryInstructions.append(computationDictionary[equation[1]] + destinationDictionary[equation[0]] + jumpsDictionary[jump[1]])

            else:
                binaryInstructions.append(computationDictionary[jump[0]] + "000" + jumpsDictionary[jump[1]])
                
        elif "=" in line:
            equation = line.split("=")
                
            binaryInstructions.append(computationDictionary[equation[1]] + destinationDictionary[equation[0]] + "000")


    writer = open(outputFilePath, "w")

    for instruction in binaryInstructions:
        writer.write(instruction + "\n")
