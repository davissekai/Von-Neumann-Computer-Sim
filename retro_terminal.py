"""
Retro Terminal Interface for Von Neumann Computer Simulator
Provides classic green-on-black terminal styling with vintage computer aesthetics
"""

import os
import sys
import time
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.live import Live
from rich import print as rprint
from colorama import init, Fore, Back, Style
from datetime import datetime

# Initialize colorama for Windows compatibility
init(autoreset=True)

class RetroTerminal:
    def __init__(self):
        self.console = Console()
        self.setup_terminal()
        
    def setup_terminal(self):
        """Configure terminal for retro appearance"""
        if os.name == 'nt':  # Windows
            os.system('color 02')  # Green on black
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def typewriter_print(self, text, delay=0.02, color="green"):
        """Print text with typewriter effect"""
        for char in text:
            if color == "green":
                print(Fore.GREEN + char, end='', flush=True)
            elif color == "yellow":
                print(Fore.YELLOW + char, end='', flush=True)
            elif color == "red":
                print(Fore.RED + char, end='', flush=True)
            elif color == "cyan":
                print(Fore.CYAN + char, end='', flush=True)
            else:
                print(char, end='', flush=True)
            time.sleep(delay)
        print()  # New line at the end
        
    def show_ascii_art(self):
        """Display retro computer ASCII art"""
        ascii_art = """
╔══════════════════════════════════════════════════════════════╗
║  ██╗   ██╗ ██████╗ ███╗   ██╗    ███╗   ██╗███████╗██╗   ██╗ ║
║  ██║   ██║██╔═══██╗████╗  ██║    ████╗  ██║██╔════╝██║   ██║ ║
║  ██║   ██║██║   ██║██╔██╗ ██║    ██╔██╗ ██║█████╗  ██║   ██║ ║
║  ╚██╗ ██╔╝██║   ██║██║╚██╗██║    ██║╚██╗██║██╔══╝  ██║   ██║ ║
║   ╚████╔╝ ╚██████╔╝██║ ╚████║    ██║ ╚████║███████╗╚██████╔╝ ║
║    ╚═══╝   ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═══╝╚══════╝ ╚═════╝  ║
║                                                              ║
║              COMPUTER SIMULATOR v1.0                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.typewriter_print(ascii_art, delay=0.001, color="green")
        
    def show_startup_sequence(self):
        """Display retro computer startup sequence"""
        self.clear_screen()
        
        # Boot messages
        boot_messages = [
            "SYSTEM INITIALIZING...",
            "CHECKING MEMORY... 256 BYTES OK",
            "LOADING CPU... OK", 
            "INITIALIZING REGISTERS... OK",
            "SETTING UP I/O SUBSYSTEM... OK",
            "SYSTEM READY",
            ""
        ]
        
        for message in boot_messages:
            self.typewriter_print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}", 
                                delay=0.03, color="green")
            time.sleep(0.5)
            
        # Show ASCII art
        self.show_ascii_art()
        time.sleep(1)
        
        # Welcome message
        welcome_text = """
WELCOME TO THE VON NEUMANN COMPUTER SIMULATOR

This is a faithful recreation of a classic stored-program computer
based on the revolutionary Von Neumann architecture.

Your computer is equipped with:
• 256 bytes of unified memory for programs and data
• 8-bit CPU with arithmetic and logic unit
• Three general-purpose registers (A, B, C)
• Built-in assembler and debugger
• Retro green-screen interface for authentic experience

Type 'help' for available commands or 'demo' for a quick demonstration.
        """
        
        self.typewriter_print(welcome_text, delay=0.01, color="green")
        
    def show_prompt(self):
        """Display the command prompt"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        prompt_text = f"[{timestamp}] VON-NEU> "
        print(Fore.GREEN + prompt_text, end='')
        
    def get_input(self, prompt_text=""):
        """Get user input with retro styling"""
        if prompt_text:
            print(Fore.GREEN + prompt_text, end='')
        user_input = input()
        return user_input.strip()
        
    def print_error(self, message):
        """Print error message in red"""
        self.typewriter_print(f"ERROR: {message}", color="red")
        
    def print_warning(self, message):
        """Print warning message in yellow"""
        self.typewriter_print(f"WARNING: {message}", color="yellow")
        
    def print_info(self, message):
        """Print info message in cyan"""
        self.typewriter_print(f"INFO: {message}", color="cyan")
        
    def print_success(self, message):
        """Print success message in green"""
        self.typewriter_print(f"SUCCESS: {message}", color="green")
        
    def show_memory_dump(self, memory, start_addr=0, end_addr=None):
        """Display memory contents in hex format"""
        if end_addr is None:
            end_addr = min(len(memory.cells), start_addr + 16)
            
        print(Fore.GREEN + "\n═══ MEMORY DUMP ═══")
        print(Fore.GREEN + "ADDR  +0 +1 +2 +3 +4 +5 +6 +7  +8 +9 +A +B +C +D +E +F  ASCII")
        print(Fore.GREEN + "────  ── ── ── ── ── ── ── ──  ── ── ── ── ── ── ── ──  ─────")
        
        for addr in range(start_addr, end_addr, 16):
            hex_line = f"{addr:04X}  "
            ascii_line = ""
            
            for offset in range(16):
                if addr + offset < len(memory.cells):
                    value = memory.cells[addr + offset]
                    if isinstance(value, tuple):  # Instructions
                        hex_line += "██ "
                        ascii_line += "■"
                    else:
                        hex_line += f"{value:02X} "
                        ascii_line += chr(value) if 32 <= value <= 126 else "."
                else:
                    hex_line += "   "
                    ascii_line += " "
                    
                if offset == 7:
                    hex_line += " "
                    
            print(Fore.GREEN + hex_line + " " + ascii_line)
            
    def show_cpu_status(self, cpu):
        """Display CPU status information"""
        print(Fore.GREEN + "\n═══ CPU STATUS ═══")
        print(Fore.GREEN + f"Program Counter: {cpu.pc:04X}")
        print(Fore.GREEN + f"Running: {'YES' if cpu.running else 'NO'}")
        print(Fore.GREEN + "\n═══ REGISTERS ═══")
        for reg, value in cpu.registers.items():
            print(Fore.GREEN + f"Register {reg}: {value:02X} ({value})")
            
    def show_help(self):
        """Display help information"""
        help_text = """
═══ AVAILABLE COMMANDS ═══

SYSTEM COMMANDS:
  help         - Show this help message
  clear        - Clear the screen
  quit/exit    - Exit the simulator
  about        - About this computer
  time         - Show current time
  date         - Show current date
  
FILE OPERATIONS (Easy!):
  create <file>    - Create a new file
  write <file>     - Write text to a file
  append <file>    - Add text to existing file
  type <file>      - Display file contents
  copy <old> <new> - Copy a file
  rename <old> <new> - Rename a file
  delete <file>    - Delete a file
  dir/ls          - List files in directory
  
TEXT EDITING:
  editor <file>   - Simple text editor
  notepad <file>  - Same as editor
  
COMPUTER OPERATIONS:
  status       - Show CPU and memory status
  memory       - Display memory contents
  registers    - Show register values
  reset        - Reset the computer
  
PROGRAMMING (Advanced):
  load <file>  - Load a program from file
  run          - Execute loaded program
  step         - Execute one instruction
  assemble     - Enter assembly programming mode
  demo         - Run demonstration program
  samples      - Browse sample programs
  tutorial     - Interactive tutorial
  
FUN STUFF:
  calc         - Calculator
  games        - Play retro games
  hello        - Hello World message
  banner <text> - Create a text banner
  
For detailed help on any command, type: help <command>
Try 'demo' for a quick start or 'tutorial' to learn!
        """
        self.typewriter_print(help_text, delay=0.003, color="green")
        
    def show_separator(self):
        """Show a visual separator"""
        print(Fore.GREEN + "═" * 60)

if __name__ == "__main__":
    # Test the retro terminal
    terminal = RetroTerminal()
    terminal.show_startup_sequence()
    
    while True:
        terminal.show_prompt()
        command = terminal.get_input()
        
        if command.lower() in ['quit', 'exit']:
            terminal.typewriter_print("SHUTTING DOWN... GOODBYE!", color="green")
            break
        elif command.lower() == 'help':
            terminal.show_help()
        elif command.lower() == 'clear':
            terminal.clear_screen()
        else:
            terminal.print_error(f"Unknown command: {command}")