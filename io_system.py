"""
I/O System for Von Neumann Computer Simulator
Handles input and output operations with retro terminal styling

Features:
- Character-based I/O with ASCII support
- Buffered input/output streams
- Terminal control sequences
- Retro styling with typewriter effects
- Input validation and formatting
- File I/O operations
"""

import time
import threading
from queue import Queue, Empty
from typing import List, Optional, Union, Callable
from colorama import Fore, Back, Style, init
import sys
import os

# Initialize colorama
init(autoreset=True)

class IOSystem:
    def __init__(self, terminal=None):
        self.terminal = terminal
        self.input_queue = Queue()
        self.output_buffer = []
        self.input_buffer = []
        
        # I/O configuration
        self.echo_input = True
        self.auto_scroll = True
        self.output_delay = 0.02  # Typewriter effect delay
        self.buffer_size = 1024
        
        # Terminal dimensions
        self.terminal_width = 80
        self.terminal_height = 24
        
        # Colors for different I/O types
        self.colors = {
            'input_prompt': Fore.CYAN + Style.BRIGHT,
            'input_text': Fore.WHITE,
            'output_text': Fore.GREEN,
            'error_text': Fore.RED + Style.BRIGHT,
            'status_text': Fore.YELLOW,
            'debug_text': Fore.MAGENTA
        }
        
        # I/O state
        self.input_mode = 'character'  # 'character', 'line', 'binary'
        self.output_mode = 'character'
        self.cursor_visible = True
        
    def write_char(self, char_code: int):
        """Write a single character to output"""
        if 0 <= char_code <= 255:
            if char_code == 10:  # Newline
                self.output_buffer.append('\n')
                if self.terminal:
                    print()
            elif char_code == 13:  # Carriage return
                if self.terminal:
                    print('\r', end='', flush=True)
            elif char_code == 8:  # Backspace
                if self.output_buffer and self.output_buffer[-1] != '\n':
                    self.output_buffer.pop()
                if self.terminal:
                    print('\b \b', end='', flush=True)
            elif 32 <= char_code <= 126:  # Printable ASCII
                char = chr(char_code)
                self.output_buffer.append(char)
                if self.terminal:
                    print(self.colors['output_text'] + char, end='', flush=True)
                    time.sleep(self.output_delay)
            else:
                # Non-printable character - show as hex
                hex_rep = f"\\x{char_code:02X}"
                self.output_buffer.append(hex_rep)
                if self.terminal:
                    print(self.colors['debug_text'] + hex_rep, end='', flush=True)
                    
    def write_string(self, text: str):
        """Write a string to output with typewriter effect"""
        for char in text:
            self.write_char(ord(char))
            
    def write_number(self, number: int, base: int = 10):
        """Write a number in specified base"""
        if base == 16:
            text = f"0x{number:X}"
        elif base == 8:
            text = f"0o{oct(number)[2:]}"
        elif base == 2:
            text = f"0b{bin(number)[2:]}"
        else:
            text = str(number)
            
        self.write_string(text)
        
    def read_char(self, timeout: Optional[float] = None) -> Optional[int]:
        """Read a single character from input"""
        try:
            if self.input_buffer:
                return self.input_buffer.pop(0)
                
            # Get input from user
            if self.terminal:
                self.terminal.show_prompt()
                user_input = self.terminal.get_input("Enter character: ")
                if user_input:
                    char_code = ord(user_input[0])
                    return char_code
            else:
                # Fallback to standard input
                char = sys.stdin.read(1)
                if char:
                    return ord(char)
                    
            return None
            
        except (EOFError, KeyboardInterrupt):
            return None
            
    def read_line(self) -> Optional[str]:
        """Read a line of text from input"""
        try:
            if self.terminal:
                line = self.terminal.get_input("INPUT> ")
                return line
            else:
                return input()
        except (EOFError, KeyboardInterrupt):
            return None
            
    def read_number(self) -> Optional[int]:
        """Read a number from input"""
        line = self.read_line()
        if line is None:
            return None
            
        line = line.strip()
        
        # Try different number formats
        try:
            if line.startswith('0x'):
                return int(line, 16)
            elif line.startswith('0b'):
                return int(line, 2)
            elif line.startswith('0o'):
                return int(line, 8)
            else:
                return int(line)
        except ValueError:
            if self.terminal:
                self.terminal.print_error(f"Invalid number format: {line}")
            return None
            
    def clear_screen(self):
        """Clear the terminal screen"""
        if self.terminal:
            self.terminal.clear_screen()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            
    def set_cursor_position(self, row: int, col: int):
        """Set cursor position (if supported)"""
        if 0 <= row < self.terminal_height and 0 <= col < self.terminal_width:
            # ANSI escape sequence for cursor positioning
            print(f'\033[{row + 1};{col + 1}H', end='', flush=True)
            
    def show_cursor(self, visible: bool = True):
        """Show or hide cursor"""
        self.cursor_visible = visible
        if visible:
            print('\033[?25h', end='', flush=True)  # Show cursor
        else:
            print('\033[?25l', end='', flush=True)  # Hide cursor
            
    def bell(self):
        """Ring the terminal bell"""
        print('\a', end='', flush=True)
        
    def display_banner(self, text: str):
        """Display a banner with retro styling"""
        width = len(text) + 4
        border = "═" * width
        
        banner_lines = [
            f"╔{border}╗",
            f"║  {text}  ║",
            f"╚{border}╝"
        ]
        
        for line in banner_lines:
            if self.terminal:
                self.terminal.typewriter_print(line, delay=0.01, color="green")
            else:
                print(Fore.GREEN + line)
                
    def display_status_line(self, cpu_status: dict):
        """Display a status line with CPU information"""
        pc = cpu_status.get('pc', 0)
        registers = cpu_status.get('registers', {})
        flags = cpu_status.get('flags', {})
        running = cpu_status.get('running', False)
        
        status_parts = [
            f"PC:{pc:04X}",
            f"A:{registers.get('A', 0):02X}",
            f"B:{registers.get('B', 0):02X}",
            f"C:{registers.get('C', 0):02X}",
            f"{'RUN' if running else 'HALT'}"
        ]
        
        # Add flags
        flag_indicators = []
        if flags.get('zero'):
            flag_indicators.append('Z')
        if flags.get('carry'):
            flag_indicators.append('C')
        if flags.get('negative'):
            flag_indicators.append('N')
        if flags.get('overflow'):
            flag_indicators.append('V')
            
        if flag_indicators:
            status_parts.append(f"FLAGS:{','.join(flag_indicators)}")
            
        status_line = " | ".join(status_parts)
        
        # Display with retro styling
        border = "─" * len(status_line)
        if self.terminal:
            print(Fore.CYAN + border)
            print(Fore.CYAN + status_line)
            print(Fore.CYAN + border)
        else:
            print(border)
            print(status_line)
            print(border)
            
    def load_from_file(self, filename: str) -> Optional[List[int]]:
        """Load binary data from file"""
        try:
            with open(filename, 'rb') as f:
                data = f.read()
                return [b for b in data]
        except FileNotFoundError:
            if self.terminal:
                self.terminal.print_error(f"File not found: {filename}")
            return None
        except Exception as e:
            if self.terminal:
                self.terminal.print_error(f"Error reading file: {e}")
            return None
            
    def save_to_file(self, filename: str, data: List[int]) -> bool:
        """Save binary data to file"""
        try:
            with open(filename, 'wb') as f:
                bytes_data = bytes(data)
                f.write(bytes_data)
            if self.terminal:
                self.terminal.print_success(f"Data saved to {filename}")
            return True
        except Exception as e:
            if self.terminal:
                self.terminal.print_error(f"Error saving file: {e}")
            return False
            
    def load_text_file(self, filename: str) -> Optional[str]:
        """Load text from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            if self.terminal:
                self.terminal.print_error(f"File not found: {filename}")
            return None
        except Exception as e:
            if self.terminal:
                self.terminal.print_error(f"Error reading file: {e}")
            return None
            
    def save_text_file(self, filename: str, text: str) -> bool:
        """Save text to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
            if self.terminal:
                self.terminal.print_success(f"Text saved to {filename}")
            return True
        except Exception as e:
            if self.terminal:
                self.terminal.print_error(f"Error saving file: {e}")
            return False
            
    def get_output_buffer(self) -> str:
        """Get current output buffer contents"""
        return ''.join(self.output_buffer)
        
    def clear_output_buffer(self):
        """Clear the output buffer"""
        self.output_buffer.clear()
        
    def add_input_chars(self, chars: List[int]):
        """Add characters to input buffer"""
        self.input_buffer.extend(chars)
        
    def add_input_string(self, text: str):
        """Add string to input buffer as character codes"""
        char_codes = [ord(c) for c in text]
        self.add_input_chars(char_codes)
        
    def create_input_dialog(self, prompt: str, input_type: str = 'string') -> Optional[Union[str, int]]:
        """Create an input dialog with validation"""
        if self.terminal:
            self.terminal.typewriter_print(prompt, color="cyan")
            
        while True:
            if input_type == 'string':
                result = self.read_line()
                if result is not None:
                    return result
            elif input_type == 'number':
                result = self.read_number()
                if result is not None:
                    return result
            elif input_type == 'char':
                result = self.read_char()
                if result is not None:
                    return result
                    
            # If we get here, input failed
            if self.terminal:
                self.terminal.print_error("Invalid input, please try again.")
            else:
                print("Invalid input, please try again.")
                
    def simulate_paper_tape(self, data: List[int]):
        """Simulate paper tape output with visual representation"""
        if self.terminal:
            self.terminal.typewriter_print("PAPER TAPE OUTPUT:", color="yellow")
            
        # Create visual representation of paper tape
        tape_lines = []
        
        for i in range(0, len(data), 8):
            # Address
            addr_line = f"{i:04X}: "
            
            # Binary representation
            binary_line = ""
            ascii_line = ""
            
            for j in range(8):
                if i + j < len(data):
                    byte = data[i + j]
                    binary_line += f"{byte:08b} "
                    ascii_line += chr(byte) if 32 <= byte <= 126 else "."
                else:
                    binary_line += "         "
                    ascii_line += " "
                    
            tape_lines.append(addr_line + binary_line + " | " + ascii_line)
            
        # Display with typewriter effect
        for line in tape_lines:
            if self.terminal:
                self.terminal.typewriter_print(line, delay=0.005, color="green")
            else:
                print(line)
                
if __name__ == "__main__":
    # Test the I/O system
    from retro_terminal import RetroTerminal
    
    terminal = RetroTerminal()
    io_system = IOSystem(terminal)
    
    # Test banner
    io_system.display_banner("I/O SYSTEM TEST")
    
    # Test character output
    test_message = "Hello, World!"
    io_system.write_string(test_message)
    io_system.write_char(10)  # Newline
    
    # Test number output
    io_system.write_string("Number: ")
    io_system.write_number(42)
    io_system.write_char(10)
    
    # Test hex output
    io_system.write_string("Hex: ")
    io_system.write_number(255, 16)
    io_system.write_char(10)
    
    print("\nOutput buffer contents:")
    print(repr(io_system.get_output_buffer()))