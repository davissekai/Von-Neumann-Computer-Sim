from memory import Memory
from cpu import CPU

# Sample program: add two numbers and store the result
program = [
    ('LOAD', 'A', 0),      # Load value from memory[0] into register A
    ('LOAD', 'B', 1),      # Load value from memory[1] into register B
    ('ADD', 'C', 'A', 'B'),# Add A and B, store result in C
    ('STORE', 'C', 2),     # Store result from C into memory[2]
    ('HALT',)              # Stop execution
]

# Initialize memory and set values at addresses 0 and 1
memory = Memory(size=256)
memory.write(0, 7)  # First number
memory.write(1, 5)  # Second number

# Load program into memory (as instructions)
for i, instr in enumerate(program):
    memory.write(i, instr)

# Create CPU and run the program
cpu = CPU(memory)
cpu.run()

# Print results
print('Register values:', cpu.registers)
print('Memory[2] (result):', memory.read(2))
