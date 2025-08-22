"""
Interactive Assembler for Von Neumann Computer Simulator
Converts human-readable assembly code to machine instructions

Supported Instructions:
- LOAD reg, addr     : Load value from memory address into register
- STORE reg, addr    : Store register value into memory address  
- ADD dest, src1, src2 : Add two registers and store result
- SUB dest, src1, src2 : Subtract src2 from src1 and store result
- MUL dest, src1, src2 : Multiply two registers
- DIV dest, src1, src2 : Divide src1 by src2
- CMP reg1, reg2     : Compare two registers and set flags
- JUMP addr          : Unconditional jump to address
- JZ addr           : Jump if zero flag is set
- JNZ addr          : Jump if zero flag is not set
- INPUT reg         : Read input into register
- OUTPUT reg        : Output register value
- NOP              : No operation
- HALT             : Stop execution

Labels and Comments:
- Labels: LABEL_NAME:
- Comments: ; This is a comment
- Data declarations: DB value  (define byte)
"""

import re
from typing import Dict, List, Tuple, Any, Optional

class Assembler:
    def __init__(self):
        self.labels = {}
        self.instructions = []
        self.data_section = {}
        self.current_address = 0
        self.errors = []
        
        # Define valid registers
        self.registers = {'A', 'B', 'C'}
        
        # Define instruction formats
        self.instruction_formats = {
            'LOAD': 2,    # reg, addr
            'STORE': 2,   # reg, addr
            'ADD': 3,     # dest, src1, src2
            'SUB': 3,     # dest, src1, src2
            'MUL': 3,     # dest, src1, src2
            'DIV': 3,     # dest, src1, src2
            'CMP': 2,     # reg1, reg2
            'JUMP': 1,    # addr
            'JZ': 1,      # addr
            'JNZ': 1,     # addr
            'INPUT': 1,   # reg
            'OUTPUT': 1,  # reg
            'NOP': 0,     # no operands
            'HALT': 0,    # no operands
        }
        
    def reset(self):
        """Reset assembler state"""
        self.labels.clear()
        self.instructions.clear()
        self.data_section.clear()
        self.current_address = 0
        self.errors.clear()
        
    def preprocess_line(self, line: str) -> str:
        """Clean and preprocess a line of assembly code"""
        # Remove comments
        if ';' in line:
            line = line[:line.index(';')]
        
        # Strip whitespace and convert to uppercase
        line = line.strip().upper()
        
        return line
        
    def parse_operand(self, operand: str) -> Any:
        """Parse an operand (register, number, or label)"""
        operand = operand.strip()
        
        # Check if it's a register
        if operand in self.registers:
            return operand
            
        # Check if it's a number (decimal or hex)
        if operand.startswith('0X'):
            try:
                return int(operand, 16)
            except ValueError:
                self.errors.append(f"Invalid hexadecimal number: {operand}")
                return 0
        elif operand.startswith('#'):
            try:
                return int(operand[1:])
            except ValueError:
                self.errors.append(f"Invalid immediate value: {operand}")
                return 0
        elif operand.isdigit():
            return int(operand)
            
        # Check if it's a label reference
        if operand in self.labels:
            return self.labels[operand]
        elif self.is_valid_label_name(operand):
            # Forward reference - will be resolved in second pass
            return operand
        else:
            self.errors.append(f"Invalid operand: {operand}")
            return 0
            
    def is_valid_label_name(self, name: str) -> bool:
        """Check if a name is a valid label"""
        return re.match(r'^[A-Z][A-Z0-9_]*$', name) is not None
        
    def parse_instruction(self, line: str, line_num: int) -> Optional[Tuple]:
        """Parse a single instruction line"""
        if not line:
            return None
            
        # Check for label definition
        if line.endswith(':'):
            label_name = line[:-1]
            if self.is_valid_label_name(label_name):
                self.labels[label_name] = self.current_address
                return None
            else:
                self.errors.append(f"Line {line_num}: Invalid label name: {label_name}")
                return None
                
        # Check for data declaration
        if line.startswith('DB '):
            try:
                value = int(line[3:])
                if 0 <= value <= 255:
                    return ('DATA', value)
                else:
                    self.errors.append(f"Line {line_num}: Data value out of range (0-255): {value}")
                    return None
            except ValueError:
                self.errors.append(f"Line {line_num}: Invalid data value: {line[3:]}")
                return None
                
        # Parse instruction
        parts = line.split()
        if not parts:
            return None
            
        opcode = parts[0]
        
        if opcode not in self.instruction_formats:
            self.errors.append(f"Line {line_num}: Unknown instruction: {opcode}")
            return None
            
        expected_operands = self.instruction_formats[opcode]
        
        if expected_operands == 0:
            if len(parts) != 1:
                self.errors.append(f"Line {line_num}: {opcode} takes no operands")
                return None
            return (opcode,)
            
        # Parse operands
        if len(parts) < expected_operands + 1:
            self.errors.append(f"Line {line_num}: {opcode} requires {expected_operands} operands")
            return None
            
        operands = []
        operand_text = ' '.join(parts[1:])
        operand_parts = [op.strip() for op in operand_text.split(',')]
        
        if len(operand_parts) != expected_operands:
            self.errors.append(f"Line {line_num}: {opcode} requires {expected_operands} operands, got {len(operand_parts)}")
            return None
            
        for operand in operand_parts:
            parsed_operand = self.parse_operand(operand)
            operands.append(parsed_operand)
            
        return (opcode, *operands)
        
    def resolve_labels(self):
        """Resolve forward label references"""
        for i, instruction in enumerate(self.instructions):
            if instruction and len(instruction) > 1:
                resolved_operands = []
                for operand in instruction[1:]:
                    if isinstance(operand, str) and operand in self.labels:
                        resolved_operands.append(self.labels[operand])
                    elif isinstance(operand, str) and self.is_valid_label_name(operand):
                        self.errors.append(f"Undefined label: {operand}")
                        resolved_operands.append(0)
                    else:
                        resolved_operands.append(operand)
                self.instructions[i] = (instruction[0], *resolved_operands)
                
    def assemble(self, source_code: str) -> Tuple[List[Any], List[str]]:
        """Assemble source code into machine instructions"""
        self.reset()
        
        lines = source_code.split('\n')
        
        # First pass: parse instructions and collect labels
        for line_num, line in enumerate(lines, 1):
            processed_line = self.preprocess_line(line)
            
            if not processed_line:
                continue
                
            instruction = self.parse_instruction(processed_line, line_num)
            
            if instruction:
                self.instructions.append(instruction)
                self.current_address += 1
            else:
                # Check if it was just a label definition
                if processed_line.endswith(':'):
                    continue
                self.instructions.append(None)
                
        # Second pass: resolve labels
        self.resolve_labels()
        
        # Filter out None instructions
        final_instructions = [instr for instr in self.instructions if instr is not None]
        
        return final_instructions, self.errors
        
    def disassemble(self, instructions: List[Tuple]) -> str:
        """Convert machine instructions back to assembly code"""
        assembly_lines = []
        
        for addr, instruction in enumerate(instructions):
            if not instruction:
                continue
                
            opcode = instruction[0]
            
            if opcode == 'DATA':
                assembly_lines.append(f"{addr:04X}: DB {instruction[1]}")
                continue
                
            line = f"{addr:04X}: {opcode}"
            
            if len(instruction) > 1:
                operands = []
                for operand in instruction[1:]:
                    if isinstance(operand, str) and operand in self.registers:
                        operands.append(operand)
                    else:
                        operands.append(str(operand))
                line += " " + ", ".join(operands)
                
            assembly_lines.append(line)
            
        return '\n'.join(assembly_lines)
        
    def create_listing(self, source_code: str, instructions: List[Tuple]) -> str:
        """Create a program listing with addresses and machine code"""
        lines = source_code.split('\n')
        listing = []
        listing.append("ADDRESS  MACHINE CODE    SOURCE")
        listing.append("-------  ------------    ------")
        
        instruction_index = 0
        
        for line_num, line in enumerate(lines):
            processed_line = self.preprocess_line(line)
            
            if not processed_line or processed_line.endswith(':'):
                listing.append(f"                         {line}")
                continue
                
            if instruction_index < len(instructions):
                instruction = instructions[instruction_index]
                addr_str = f"{instruction_index:04X}"
                
                # Format machine code
                if instruction[0] == 'DATA':
                    machine_str = f"DB {instruction[1]:02X}"
                else:
                    machine_str = f"{instruction[0]}"
                    if len(instruction) > 1:
                        operands = [str(op) for op in instruction[1:]]
                        machine_str += f" {','.join(operands)}"
                        
                listing.append(f"{addr_str}     {machine_str:<12}   {line}")
                instruction_index += 1
            else:
                listing.append(f"                         {line}")
                
        return '\n'.join(listing)
        
    def get_sample_programs(self) -> Dict[str, str]:
        """Return a collection of sample programs"""
        return {
            "Hello World": """
; Simple Hello World program
; Outputs ASCII values for "HELLO"

LOAD A, #72    ; 'H'
OUTPUT A
LOAD A, #69    ; 'E' 
OUTPUT A
LOAD A, #76    ; 'L'
OUTPUT A
OUTPUT A       ; Second 'L'
LOAD A, #79    ; 'O'
OUTPUT A
HALT
            """,
            
            "Add Two Numbers": """
; Add two numbers and output result

LOAD A, NUM1   ; Load first number
LOAD B, NUM2   ; Load second number  
ADD C, A, B    ; Add them
OUTPUT C       ; Output result
HALT

NUM1: DB 15    ; First number
NUM2: DB 27    ; Second number
            """,
            
            "Count to 10": """
; Count from 1 to 10

LOAD A, #1     ; Start at 1
LOAD B, #10    ; Count to 10

LOOP:
OUTPUT A       ; Output current number
ADD A, A, #1   ; Increment counter
CMP A, B       ; Compare with limit
JZ DONE        ; Jump if equal
JUMP LOOP      ; Continue loop

DONE:
HALT
            """,
            
            "Fibonacci": """
; Calculate Fibonacci sequence

LOAD A, #0     ; F(0) = 0
LOAD B, #1     ; F(1) = 1
LOAD C, #8     ; Calculate 8 numbers

OUTPUT A       ; Output F(0)
OUTPUT B       ; Output F(1)

LOOP:
ADD A, A, B    ; F(n) = F(n-1) + F(n-2)
OUTPUT A       ; Output result
SUB B, A, B    ; Update F(n-1)
SUB C, C, #1   ; Decrement counter
JZ DONE        ; Done if counter = 0
JUMP LOOP      ; Continue

DONE:
HALT
            """
        }

if __name__ == "__main__":
    # Test the assembler
    assembler = Assembler()
    
    # Test with a simple program
    test_program = """
    ; Test program
    LOAD A, #5
    LOAD B, #3
    ADD C, A, B
    OUTPUT C
    HALT
    """
    
    instructions, errors = assembler.assemble(test_program)
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  {error}")
    else:
        print("Assembly successful!")
        print("\nInstructions:")
        for i, instr in enumerate(instructions):
            print(f"  {i}: {instr}")
            
        print("\nDisassembly:")
        print(assembler.disassemble(instructions))