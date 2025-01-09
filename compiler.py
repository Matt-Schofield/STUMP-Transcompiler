# TODO
# Labels - EQU (Macros), DATA (Pointer sort of thing), ORG (Begin at line)
# Check branching add to PC or becomes PC
# Extras

import sys

def mov(tokens):
    return parse("ADD " + tokens[1] + ", R0, " + tokens[2])

def mul(tokens):
    print("MUL")
    dest = tokens[1] # Ra,
    srcA = tokens[2] # Rb,
    srcB = tokens[3] # Rc

    print(tokens)

    if srcB.strip().startswith("#"):
        return "Fail - MUL instruction must be type 1"

    mul_out = (parse("EQU mul" + str(label_counter)) + 
               parse("ADD " + dest + srcA + srcB) + 
               parse("SUBS " + dest + srcA + "#1") + 
               parse("BGT mul" + str(label_counter)))

    label_counter += 1

    return mul_out

INSTR_CODES = {
    "ADD":"000",
    "ADC":"001",
    "SUB":"010",
    "SBC":"011",
    "AND":"100",
    "OR": "101",
    "LD": "110",
    "ST": "110"
}

EXTRA_CODES = {
    "MUL":  mul,
    "MOV":  mov,
    "ORG":  "org",
    "EQU":  "equ",
    "DATA": "data"
}

# For ensuring complier generated labels are unique
label_counter = 0

BRANCH_CONS = {
    "BAL": "0000",  # Always
    "BNV": "0001",  # Never (uninteresting)
    "BHI": "0010",  # HIgher
    "BLS": "0011",  # Lower or Same
    "BCC": "0100",  # Carry Clear
    "BCS": "0101",  # Carry Set
    "BNE": "0110",  # Not Equal
    "BEQ": "0111",  # EQual
    "BVC": "1000",  # oVerflow Clear
    "BVS": "1001",  # oVerflow Set
    "BPL": "1010",  # PLus (positive)
    "BMI": "1011",  # MInus (negative)
    "BGE": "1100",  # Greater or Equal
    "BLT": "1101",  # Less Than
    "BGT": "1110",  # Greater Than
    "BLE": "1111"   # Less or Equal 
}

SHIFT_OPS = {
    "ASR": "01",
    "ROR": "10",
    "RRC": "11"
}

def parse(ln: str) -> str:
    # Binary output
    res = ""

    # 1) Standardise string
    # print(ln)
    ln = ln.upper()

    # 2) Tokenise string
    tokens = ln.split(" ")
    
    # Skip line if token count too low
    if len(tokens) <= 1:
        return "Empty"

    instr = tokens[0]

    # 3) Determine if instruction is branch
    if instr[0] == "B":
        instr_type = 3

        offset = int(tokens[1][1:])

        if instr not in BRANCH_CONS.keys():
            return "Fail - Invalid branch condition"

        res += "1111" + BRANCH_CONS[instr]
        
        if offset > 127 or offset < -128:
            return "Fail - Branch offset out of bounds"

        # (int) offset -> signed binary immediate
        if offset < 0:
            res += bin((0b11111111 ^ abs(offset)) + 1)[2:].rjust(8, "0")
        else:
            res += bin(offset)[2:].rjust(8, "0")

        return res

    # 4) Determine non-branch instruction 
    # Assume flags are not to be set
    

    # Check validity
    if instr in INSTR_CODES.keys():
        flags = False
    elif instr[:-1] in INSTR_CODES.keys():
        flags = True
    elif instr in EXTRA_CODES.keys():
        flags = False
        return EXTRA_CODES[instr](tokens)
    else:
        return "Fail - Invalid operation"        

    # Otherwise code is valid, add appropriate binary to result
    res += INSTR_CODES[instr] if flags == False else INSTR_CODES[instr[:-1]]

    # Override flag value if instruction is LD/ST
    if instr == "ST":
        flags = True

    # 5) Determine instruction type & determine register values
    # Check dest and srcA registers are valid
    dest = int(tokens[1][1])
    if dest > 7 or dest < 0:
            return "Fail - Destination reigster invalid"

    srcA = int(tokens[2][1])
    if srcA > 7 or srcA < 0:
            return "Fail - srcA reigster invalid"

    # Determine type and set appropriate srcB value
    srcB_or_imm = tokens[3].replace(",", "")
    if srcB_or_imm[0] == "R":
        # Type 1
        instr_type = "0"

        # Check srcB register is valid
        srcB_or_imm = int(srcB_or_imm[1])
        if srcB_or_imm > 7 or srcB_or_imm < 0:
            return "Fail - srcB reigster invalid"

        srcB_or_imm = bin(srcB_or_imm)[2:].rjust(3, "0")

        # Determine shifter
        if len(tokens) <= 4:
            shift = "00"
        else:
            shift = tokens[4].replace(",", "")
            # Check if shift op valid
            if shift not in SHIFT_OPS.keys():
                return "Fail - Invalid shift operation"

            shift = SHIFT_OPS[shift]
    else:
        # Type 2
        instr_type = "1"
        
        # Check immediate is in range
        imm = int(srcB_or_imm[1:])
        if imm > 15 or imm < -16:
            return "Fail - Immediate out of bounds"

        # (int) imm -> signed binary immediate
        if imm < 0:
            srcB_or_imm = bin((0b11111 ^ abs(imm)) + 1)[2:]
        else:
            srcB_or_imm = bin(imm)[2:].rjust(5, "0") 
        
        # Ensure shift variable is defined
        shift = None

    # 6) Aggregate remaing components into binary result
    res += (instr_type + str(int(flags))
         + bin(dest)[2:].rjust(3, "0")
         + bin(srcA)[2:].rjust(3, "0") 
         + srcB_or_imm)

    res += shift if shift != None else ""

    return res

# Open file from path specified on command line
try:
    source = open(sys.argv[1], "r")
except FileNotFoundError:
    print("ERROR: file '" + sys.argv[1] + "' not found.")
    sys.exit()

binary = open(sys.argv[2], "w")

# Parse file contents line by line
line_count = 0
for line in source:
    line = line.strip()
        
    line_count += 1

    res = ""

    # Instr --> Bin for each line in source file that isn't a comment
    if line == "" or (line[0] == "/" and line[1] == "/"):
        continue
        
    else:
        res = parse(line)

    # Check for parse failiure
    if res[0] == "F":
        print("ERROR: Parse error on line [" + str(line_count) + "] " + res[5:] + " '" + line[:-1] + "'")
        binary.close()
        source.close()
        sys.exit()
    elif res[0] == "E":
        continue
        
    else:
        binary.write(res + "\n")

binary.close()
source.close()

