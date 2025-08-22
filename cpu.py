'''
Enhanced CPU with debugging capabilities for Von Neumann Computer Simulator

The CPU is the brain of the computer with two main components:
1. The Control Unit - handles fetching, decoding, and control flow
2. The Arithmetic Logic Unit (ALU) - performs arithmetic and logical operations

Features:
- Step-by-step execution mode
- Breakpoint support
- Instruction trace logging
- Register monitoring
- Stack operations
'''

import time
from typing import List, Dict, Any, Optional

class CPU:
    # class to define the CPU
    def __init__(self, memory):
        self.memory = memory
        self.pc = 0 # Program Counter
        self.registers = {'A': 0, 'B': 0, 'C': 0}
        self.running = True
        
        # Debugging features
        self.debug_mode = False
        self.step_mode = False
        self.breakpoints = set()
        self.instruction_count = 0
        self.execution_history = []
        self.max_history = 100
        
        # Status flags
        self.flags = {
            'zero': False,
            'negative': False,
            'overflow': False,
            'carry': False
        }
        
        # I/O buffers
        self.input_buffer = []
        self.output_buffer = []

    # function to fetch instructions
    def fetch(self):
        """Fetch instruction from memory at program counter"""
        if self.pc >= len(self.memory.cells):
            self.running = False
            return None
            
        instruction = self.memory.read(self.pc)
        
        # Log instruction fetch in debug mode
        if self.debug_mode:
            self.log_instruction(f"FETCH: PC={self.pc:04X}, INSTR={instruction}")
            
        self.pc += 1
        return instruction
    
    def decode(self, instruction):
        """Decode instruction and return components"""
        if not instruction:
            return None, [], None
            
        if isinstance(instruction, tuple):
            opcode = instruction[0]
            operands = list(instruction[1:]) if len(instruction) > 1 else []
        else:
            opcode = instruction
            operands = []
            
        return opcode, operands, instruction
    
    # function to execute instructions
    def execute(self, instruction):
        """Execute a single instruction with enhanced debugging"""
        if not instruction:
            self.running = False
            return
            
        opcode, operands, full_instr = self.decode(instruction)
        
        if not opcode:
            self.running = False
            return
            
        # Log execution in debug mode
        old_registers = self.registers.copy() if self.debug_mode else None
            
        # Execute instruction based on opcode
        try:
            if opcode == 'LOAD':
                self._execute_load(operands)
            elif opcode == 'STORE':
                self._execute_store(operands)
            elif opcode == 'ADD':
                self._execute_add(operands)
            elif opcode == 'SUB':
                self._execute_sub(operands)
            elif opcode == 'MUL':
                self._execute_mul(operands)
            elif opcode == 'DIV':
                self._execute_div(operands)
            elif opcode == 'JUMP':
                self._execute_jump(operands)
            elif opcode == 'JZ':
                self._execute_jump_zero(operands)
            elif opcode == 'JNZ':
                self._execute_jump_not_zero(operands)
            elif opcode == 'CMP':
                self._execute_compare(operands)
            elif opcode == 'INPUT':
                self._execute_input(operands)
            elif opcode == 'OUTPUT':
                self._execute_output(operands)
            elif opcode == 'HALT':
                self._execute_halt()
            elif opcode == 'NOP':
                pass  # No operation
            else:
                raise ValueError(f"Unknown instruction: {opcode}")
                
            self.instruction_count += 1
            
            # Log changes in debug mode
            if self.debug_mode and old_registers is not None:
                self.log_execution(opcode, operands, old_registers)
                
        except Exception as e:
            if self.debug_mode:
                self.log_instruction(f"ERROR: {e}")
            self.running = False
    
    def _execute_load(self, operands):
        """LOAD reg, addr - Load value from memory address into register"""
        reg, addr = operands[0], operands[1]
        value = self.memory.read(addr)
        self.registers[reg] = value
        self._update_flags(value)
    
    def _execute_store(self, operands):
        """STORE reg, addr - Store register value into memory address"""
        reg, addr = operands[0], operands[1]
        self.memory.write(addr, self.registers[reg])
    
    def _execute_add(self, operands):
        """ADD dest, src1, src2 - Add two registers and store result"""
        dest, src1, src2 = operands[0], operands[1], operands[2]
        result = self.registers[src1] + self.registers[src2]
        
        # Check for overflow (8-bit arithmetic)
        if result > 255:
            self.flags['carry'] = True
            self.flags['overflow'] = True
            result = result & 0xFF  # Keep only lower 8 bits
        else:
            self.flags['carry'] = False
            self.flags['overflow'] = False
            
        self.registers[dest] = result
        self._update_flags(result)
    
    def _execute_sub(self, operands):
        """SUB dest, src1, src2 - Subtract src2 from src1 and store result"""
        dest, src1, src2 = operands[0], operands[1], operands[2]
        result = self.registers[src1] - self.registers[src2]
        
        if result < 0:
            self.flags['carry'] = True
            result = 256 + result  # Two's complement for 8-bit
        else:
            self.flags['carry'] = False
            
        self.registers[dest] = result
        self._update_flags(result)
    
    def _execute_mul(self, operands):
        """MUL dest, src1, src2 - Multiply two registers"""
        dest, src1, src2 = operands[0], operands[1], operands[2]
        result = self.registers[src1] * self.registers[src2]
        
        if result > 255:
            self.flags['overflow'] = True
            result = result & 0xFF
        else:
            self.flags['overflow'] = False
            
        self.registers[dest] = result
        self._update_flags(result)
    
    def _execute_div(self, operands):
        """DIV dest, src1, src2 - Divide src1 by src2"""
        dest, src1, src2 = operands[0], operands[1], operands[2]
        
        if self.registers[src2] == 0:
            raise ValueError("Division by zero")
            
        result = self.registers[src1] // self.registers[src2]
        self.registers[dest] = result
        self._update_flags(result)
    
    def _execute_jump(self, operands):
        """JUMP addr - Unconditional jump to address"""
        addr = operands[0]
        self.pc = addr
    
    def _execute_jump_zero(self, operands):
        """JZ addr - Jump if zero flag is set"""
        if self.flags['zero']:
            addr = operands[0]
            self.pc = addr
    
    def _execute_jump_not_zero(self, operands):
        """JNZ addr - Jump if zero flag is not set"""
        if not self.flags['zero']:
            addr = operands[0]
            self.pc = addr
    
    def _execute_compare(self, operands):
        """CMP reg1, reg2 - Compare two registers and set flags"""
        reg1, reg2 = operands[0], operands[1]
        val1, val2 = self.registers[reg1], self.registers[reg2]
        
        result = val1 - val2
        self._update_flags(result)
    
    def _execute_input(self, operands):
        """INPUT reg - Read input into register"""
        reg = operands[0]
        if self.input_buffer:
            self.registers[reg] = self.input_buffer.pop(0)
        else:
            self.registers[reg] = 0  # Default if no input
    
    def _execute_output(self, operands):
        """OUTPUT reg - Output register value"""
        reg = operands[0]
        value = self.registers[reg]
        self.output_buffer.append(value)
    
    def _execute_halt(self):
        """HALT - Stop execution"""
        self.running = False
    
    def _update_flags(self, value):
        """Update CPU flags based on value"""
        self.flags['zero'] = (value == 0)
        self.flags['negative'] = (value < 0 if isinstance(value, int) else False)

    def run(self):
        """Run program in continuous mode"""
        self.step_mode = False
        
        while self.running:
            # Check for breakpoints
            if self.pc in self.breakpoints:
                if self.debug_mode:
                    self.log_instruction(f"BREAKPOINT HIT at {self.pc:04X}")
                self.step_mode = True
                return
                
            instruction = self.fetch()
            if instruction is None:
                break
                
            self.execute(instruction)
            
            # Add small delay for visual effect in debug mode
            if self.debug_mode and self.step_mode:
                time.sleep(0.1)
    
    def step(self):
        """Execute single instruction (step mode)"""
        if not self.running:
            return False
            
        instruction = self.fetch()
        if instruction is None:
            return False
            
        self.execute(instruction)
        return True
    
    def reset(self):
        """Reset CPU to initial state"""
        self.pc = 0
        self.registers = {'A': 0, 'B': 0, 'C': 0}
        self.running = True
        self.instruction_count = 0
        self.execution_history.clear()
        self.flags = {
            'zero': False,
            'negative': False,
            'overflow': False,
            'carry': False
        }
        self.input_buffer.clear()
        self.output_buffer.clear()
    
    # Debug and monitoring methods
    def enable_debug(self):
        """Enable debug mode"""
        self.debug_mode = True
    
    def disable_debug(self):
        """Disable debug mode"""
        self.debug_mode = False
        
    def set_breakpoint(self, address):
        """Set breakpoint at address"""
        self.breakpoints.add(address)
    
    def remove_breakpoint(self, address):
        """Remove breakpoint at address"""
        self.breakpoints.discard(address)
    
    def clear_breakpoints(self):
        """Clear all breakpoints"""
        self.breakpoints.clear()
    
    def log_instruction(self, message):
        """Log instruction for debugging"""
        if len(self.execution_history) >= self.max_history:
            self.execution_history.pop(0)
        self.execution_history.append(f"[{self.instruction_count:04d}] {message}")
    
    def log_execution(self, opcode, operands, old_registers):
        """Log detailed execution information"""
        reg_changes = []
        for reg, old_val in old_registers.items():
            new_val = self.registers[reg]
            if old_val != new_val:
                reg_changes.append(f"{reg}: {old_val:02X}→{new_val:02X}")
        
        changes = f" [{', '.join(reg_changes)}]" if reg_changes else ""
        self.log_instruction(f"EXEC: {opcode} {operands}{changes}")
    
    def get_status(self):
        """Get comprehensive CPU status"""
        return {
            'pc': self.pc,
            'registers': self.registers.copy(),
            'flags': self.flags.copy(),
            'running': self.running,
            'instruction_count': self.instruction_count,
            'debug_mode': self.debug_mode,
            'step_mode': self.step_mode,
            'breakpoints': list(self.breakpoints),
            'output_buffer': self.output_buffer.copy()
        }
    
    def add_input(self, value):
        """Add value to input buffer"""
        self.input_buffer.append(value)
    
    def get_output(self):
        """Get and clear output buffer"""
        output = self.output_buffer.copy()
        self.output_buffer.clear()
        return output
