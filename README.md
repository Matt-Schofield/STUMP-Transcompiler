# STUMP-Transcompiler
Simple python based program that converts from STUMP, a 16-bit RISC assembly language, to binary. 

Binary output intended to be ran on emulated CPU datapath via an FPGA. A full breakdown of the STUMP language is NOT provided here.

## Overview of STUMP instruction set
Available Basic Instructions:
- ADD  -  Add
- ADC  -  Add with carry
- SUB  -  Subtract
- SBC  -  Subtract with carry
- AND  -  Logical AND
- OR   -  Logical OR
- LD   -  Load from register
- ST   -  Store to register

Available Pseudo-Instructions / Directives:
- MUL  -  Multiply
- MOV  -  Move to register
- ORG (Not implemented)
- EQU (Not implemented)
- DATA (Not implemented)

Available Branch Instructions:
-  BAL  -   Always
-  BNV  -   Never (uninteresting)
-  BHI  -   HIgher
-  BLS  -   Lower or Same
-  BCC  -   Carry Clear
-  BCS  -   Carry Set
-  BNE  -   Not Equal
-  BEQ  -   EQual
-  BVC  -   oVerflow Clear
-  BVS  -   oVerflow Set
-  BPL  -   PLus (positive)
-  BMI  -   MInus (negative)
-  BGE  -   Greater or Equal
-  BLT  -   Less Than
-  BGT  -   Greater Than
-  BLE  -   Less or Equal 

Available Shift-Ops:
- ASR  -  Arithmetic Shift Right
- ROR  -  Rotate Right (Move carry)
- RRC  -  Rotate Right (Leave carry)
