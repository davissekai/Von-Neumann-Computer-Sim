'''
Memory will be a big list/array.. with cells for storing data and instructions/programs
Each cell will have an address (its position in the list), so you can read from or write stuff to that cell. 
The CPU will also fetch instructions and data from memory by specifying the address. 
'''


class Memory:
    def __init__(self, size=256):
        self.cells = [0] * size # Initialize memory with zeros

    def read(self, address):
        return self.cells[address]
    
    def write(self, address, value):
        self.cells[address] = value


        