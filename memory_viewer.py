"""
Visual Memory Viewer for Von Neumann Computer Simulator
Provides hexadecimal and ASCII representation of memory contents
with highlighting for different data types and program sections

Features:
- Hexadecimal memory dump with addresses
- ASCII representation of memory contents  
- Highlighting for instructions vs data
- Search functionality
- Memory editing capabilities
- Program counter and register highlighting
"""

from colorama import Fore, Back, Style, init
from typing import Optional, List, Tuple, Dict, Any
import re

# Initialize colorama
init(autoreset=True)

class MemoryViewer:
    def __init__(self, memory, cpu=None):
        self.memory = memory
        self.cpu = cpu
        self.bytes_per_row = 16
        self.current_view_start = 0
        self.highlight_addresses = set()
        
        # Color scheme for different data types
        self.colors = {
            'address': Fore.CYAN,
            'instruction': Fore.YELLOW + Style.BRIGHT,
            'data': Fore.GREEN,
            'zero': Fore.BLACK + Style.DIM,
            'pc_highlight': Back.RED + Fore.WHITE + Style.BRIGHT,
            'register_highlight': Back.BLUE + Fore.WHITE + Style.BRIGHT,
            'ascii_printable': Fore.GREEN,
            'ascii_control': Fore.RED,
            'separator': Fore.WHITE
        }
        
    def format_hex_byte(self, value: Any, address: int) -> str:
        """Format a single byte with appropriate coloring"""
        if isinstance(value, tuple):
            # This is an instruction
            return self.colors['instruction'] + "██"
        elif isinstance(value, int):
            if value == 0:
                return self.colors['zero'] + f"{value:02X}"
            else:
                return self.colors['data'] + f"{value:02X}"
        else:
            return self.colors['data'] + "??"
            
    def format_ascii_char(self, value: Any) -> str:
        """Format ASCII representation of a byte"""
        if isinstance(value, tuple):
            return self.colors['instruction'] + "■"
        elif isinstance(value, int):
            if 32 <= value <= 126:  # Printable ASCII
                return self.colors['ascii_printable'] + chr(value)
            else:
                return self.colors['ascii_control'] + "."
        else:
            return "?"
            
    def display_memory_range(self, start_addr: int, end_addr: int) -> str:
        """Display memory contents in hex dump format"""
        output_lines = []
        
        # Header
        header = self.colors['separator'] + "ADDR  "
        for i in range(16):
            header += f"+{i:X} "
            if i == 7:
                header += " "
        header += " ASCII"
        output_lines.append(header)
        
        # Separator line
        separator = self.colors['separator'] + "────  "
        separator += "── " * 8 + " " + "── " * 8 + " ─────"
        output_lines.append(separator)
        
        # Memory rows
        for addr in range(start_addr, end_addr, self.bytes_per_row):
            # Address column
            addr_color = self.colors['address']
            if self.cpu and addr == self.cpu.pc:
                addr_color = self.colors['pc_highlight']
                
            line = addr_color + f"{addr:04X}  "
            ascii_line = ""
            
            # Hex bytes
            for offset in range(self.bytes_per_row):
                current_addr = addr + offset
                
                if current_addr < len(self.memory.cells):
                    value = self.memory.cells[current_addr]
                    
                    # Special highlighting for PC and register values
                    hex_str = self.format_hex_byte(value, current_addr)
                    if self.cpu and current_addr == self.cpu.pc:
                        hex_str = self.colors['pc_highlight'] + f"{value if isinstance(value, int) else '██'}"
                        
                    line += hex_str + " "
                    ascii_line += self.format_ascii_char(value)
                else:
                    line += self.colors['zero'] + "   "
                    ascii_line += " "
                    
                # Add separator after 8 bytes
                if offset == 7:
                    line += " "
                    
            # Add ASCII representation
            line += " " + ascii_line
            output_lines.append(line)
            
        return '\n'.join(output_lines)
        
    def display_memory_page(self, page_size: int = 256) -> str:
        """Display a page of memory starting from current view position"""
        end_addr = min(self.current_view_start + page_size, len(self.memory.cells))
        return self.display_memory_range(self.current_view_start, end_addr)
        
    def display_around_pc(self, context_lines: int = 8) -> str:
        """Display memory around the program counter"""
        if not self.cpu:
            return "No CPU available for PC reference"
            
        pc = self.cpu.pc
        start_addr = max(0, pc - (context_lines * self.bytes_per_row // 2))
        end_addr = min(len(self.memory.cells), 
                      pc + (context_lines * self.bytes_per_row // 2))
        
        # Align to row boundaries
        start_addr = (start_addr // self.bytes_per_row) * self.bytes_per_row
        end_addr = ((end_addr + self.bytes_per_row - 1) // self.bytes_per_row) * self.bytes_per_row
        
        output = self.colors['separator'] + f"╔══ MEMORY AROUND PC ({pc:04X}) ══╗\n"
        output += self.display_memory_range(start_addr, end_addr)
        output += "\n" + self.colors['separator'] + "╚" + "═" * 30 + "╝"
        
        return output
        
    def search_memory(self, pattern: str, search_type: str = 'hex') -> List[int]:
        """Search for pattern in memory"""
        matches = []
        
        if search_type == 'hex':
            # Search for hex pattern
            try:
                if pattern.startswith('0x'):
                    pattern = pattern[2:]
                hex_bytes = [int(pattern[i:i+2], 16) for i in range(0, len(pattern), 2)]
                
                for addr in range(len(self.memory.cells) - len(hex_bytes) + 1):
                    match = True
                    for i, byte_val in enumerate(hex_bytes):
                        mem_val = self.memory.cells[addr + i]
                        if isinstance(mem_val, int) and mem_val == byte_val:
                            continue
                        else:
                            match = False
                            break
                    if match:
                        matches.append(addr)
                        
            except ValueError:
                pass  # Invalid hex pattern
                
        elif search_type == 'ascii':
            # Search for ASCII string
            pattern_bytes = [ord(c) for c in pattern]
            
            for addr in range(len(self.memory.cells) - len(pattern_bytes) + 1):
                match = True
                for i, byte_val in enumerate(pattern_bytes):
                    mem_val = self.memory.cells[addr + i]
                    if isinstance(mem_val, int) and mem_val == byte_val:
                        continue
                    else:
                        match = False
                        break
                if match:
                    matches.append(addr)
                    
        return matches
        
    def analyze_memory_usage(self) -> Dict[str, Any]:
        """Analyze memory usage and return statistics"""
        stats = {
            'total_size': len(self.memory.cells),
            'instructions': 0,
            'data_bytes': 0,
            'zero_bytes': 0,
            'non_zero_data': 0,
            'instruction_addresses': [],
            'data_ranges': []
        }
        
        current_data_start = None
        
        for addr, value in enumerate(self.memory.cells):
            if isinstance(value, tuple):
                stats['instructions'] += 1
                stats['instruction_addresses'].append(addr)
                
                # End any current data range
                if current_data_start is not None:
                    stats['data_ranges'].append((current_data_start, addr - 1))
                    current_data_start = None
                    
            elif isinstance(value, int):
                stats['data_bytes'] += 1
                
                if value == 0:
                    stats['zero_bytes'] += 1
                else:
                    stats['non_zero_data'] += 1
                    
                # Start or continue data range
                if current_data_start is None:
                    current_data_start = addr
                    
        # Close final data range if needed
        if current_data_start is not None:
            stats['data_ranges'].append((current_data_start, len(self.memory.cells) - 1))
            
        stats['utilization'] = ((stats['instructions'] + stats['non_zero_data']) / 
                               stats['total_size'] * 100)
        
        return stats
        
    def display_memory_map(self) -> str:
        """Display a visual memory map showing code and data sections"""
        output_lines = []
        output_lines.append(self.colors['separator'] + "╔══ MEMORY MAP ══╗")
        
        stats = self.analyze_memory_usage()
        
        # Summary
        output_lines.append(f"Total Size: {stats['total_size']} bytes")
        output_lines.append(f"Instructions: {stats['instructions']}")
        output_lines.append(f"Data Bytes: {stats['data_bytes']}")
        output_lines.append(f"Utilization: {stats['utilization']:.1f}%")
        output_lines.append("")
        
        # Visual map (simplified)
        map_width = 64
        bytes_per_char = max(1, len(self.memory.cells) // map_width)
        
        map_line = ""
        for i in range(0, len(self.memory.cells), bytes_per_char):
            has_instruction = False
            has_data = False
            
            for j in range(bytes_per_char):
                if i + j < len(self.memory.cells):
                    value = self.memory.cells[i + j]
                    if isinstance(value, tuple):
                        has_instruction = True
                    elif isinstance(value, int) and value != 0:
                        has_data = True
                        
            if has_instruction:
                map_line += self.colors['instruction'] + "█"
            elif has_data:
                map_line += self.colors['data'] + "▓"
            else:
                map_line += self.colors['zero'] + "░"
                
        output_lines.append("Memory Layout:")
        output_lines.append(map_line)
        output_lines.append(self.colors['instruction'] + "█ Instructions  " +
                           self.colors['data'] + "▓ Data  " +
                           self.colors['zero'] + "░ Empty")
        
        output_lines.append(self.colors['separator'] + "╚" + "═" * 16 + "╝")
        
        return '\n'.join(output_lines)
        
    def export_hex_dump(self, filename: str, start_addr: int = 0, 
                       end_addr: Optional[int] = None) -> bool:
        """Export memory contents to Intel HEX format"""
        if end_addr is None:
            end_addr = len(self.memory.cells)
            
        try:
            with open(filename, 'w') as f:
                # Write hex records
                for addr in range(start_addr, end_addr, 16):
                    # Data record
                    record_data = []
                    byte_count = min(16, end_addr - addr)
                    
                    for i in range(byte_count):
                        value = self.memory.cells[addr + i]
                        if isinstance(value, int):
                            record_data.append(value)
                        else:
                            record_data.append(0)  # Instructions as 0 for now
                            
                    # Format Intel HEX record
                    checksum = (byte_count + (addr >> 8) + (addr & 0xFF) + 
                               sum(record_data)) & 0xFF
                    checksum = (0x100 - checksum) & 0xFF
                    
                    hex_data = ''.join(f"{b:02X}" for b in record_data)
                    f.write(f":{byte_count:02X}{addr:04X}00{hex_data}{checksum:02X}\n")
                    
                # End of file record
                f.write(":00000001FF\n")
                
            return True
        except Exception:
            return False
            
    def set_view_position(self, address: int):
        """Set the starting position for memory view"""
        self.current_view_start = max(0, address)
        
    def navigate_up(self, lines: int = 1):
        """Navigate up in memory view"""
        self.current_view_start = max(0, 
                                     self.current_view_start - (lines * self.bytes_per_row))
        
    def navigate_down(self, lines: int = 1):
        """Navigate down in memory view"""
        max_addr = len(self.memory.cells) - self.bytes_per_row
        self.current_view_start = min(max_addr,
                                     self.current_view_start + (lines * self.bytes_per_row))

if __name__ == "__main__":
    # Test the memory viewer
    from memory import Memory
    from cpu import CPU
    
    # Create test memory with some data
    memory = Memory(256)
    
    # Add some test instructions and data
    memory.write(0, ('LOAD', 'A', 10))
    memory.write(1, ('LOAD', 'B', 11))
    memory.write(2, ('ADD', 'C', 'A', 'B'))
    memory.write(3, ('HALT',))
    
    # Add some test data
    memory.write(10, 42)
    memory.write(11, 58)
    
    # Test string "HELLO"
    hello = "HELLO"
    for i, char in enumerate(hello):
        memory.write(20 + i, ord(char))
    
    # Create CPU and viewer
    cpu = CPU(memory)
    viewer = MemoryViewer(memory, cpu)
    
    print("Memory Viewer Test")
    print("=" * 50)
    print(viewer.display_memory_range(0, 64))
    print("\n" + viewer.display_memory_map())
    
    # Test search
    matches = viewer.search_memory("HELLO", "ascii")
    print(f"\nFound 'HELLO' at addresses: {matches}")
    
    # Test around PC
    print("\n" + viewer.display_around_pc())