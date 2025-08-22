"""
Main Terminal Interface for Von Neumann Computer Simulator
Integrates all components into a cohesive retro computing experience

Features:
- Complete command-line interface with retro styling
- Interactive program editor and assembler
- Real-time debugging and monitoring
- Memory visualization and editing
- File operations and program management
- Built-in help system and tutorials
"""

import os
import sys
import time
from typing import Dict, List, Optional, Any

# Import our custom modules
from memory import Memory
from cpu import CPU
from retro_terminal import RetroTerminal
from assembler import Assembler
from memory_viewer import MemoryViewer
from io_system import IOSystem

class VonNeumannSimulator:
    def __init__(self):
        # Initialize core components
        self.memory = Memory(256)
        self.cpu = CPU(self.memory)
        self.terminal = RetroTerminal()
        self.assembler = Assembler()
        self.memory_viewer = MemoryViewer(self.memory, self.cpu)
        self.io_system = IOSystem(self.terminal)
        
        # Current state
        self.running = True
        self.current_program = ""
        self.program_loaded = False
        self.debug_mode = False
        
        # Command history
        self.command_history = []
        self.max_history = 50
        
        # Available commands
        self.commands = {
            # System commands
            'help': self.cmd_help,
            'clear': self.cmd_clear,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
            'about': self.cmd_about,
            
            # Computer operations
            'status': self.cmd_status,
            'reset': self.cmd_reset,
            'memory': self.cmd_memory,
            'registers': self.cmd_registers,
            
            # Programming commands
            'assemble': self.cmd_assemble,
            'load': self.cmd_load,
            'save': self.cmd_save,
            'edit': self.cmd_edit,
            'list': self.cmd_list,
            
            # Execution commands
            'run': self.cmd_run,
            'step': self.cmd_step,
            'continue': self.cmd_continue,
            'stop': self.cmd_stop,
            
            # Debugging commands
            'debug': self.cmd_debug,
            'breakpoint': self.cmd_breakpoint,
            'watch': self.cmd_watch,
            'trace': self.cmd_trace,
            
            # Sample programs
            'demo': self.cmd_demo,
            'samples': self.cmd_samples,
            'tutorial': self.cmd_tutorial,
            
            # File operations (user-friendly)
            'dir': self.cmd_dir,
            'ls': self.cmd_dir,  # Unix alias
            'type': self.cmd_type,
            'cat': self.cmd_type,  # Unix alias
            'create': self.cmd_create,
            'new': self.cmd_create,  # Alias for create
            'write': self.cmd_write,
            'append': self.cmd_append,
            'copy': self.cmd_copy,
            'rename': self.cmd_rename,
            'delete': self.cmd_delete,
            'del': self.cmd_delete,  # DOS alias
            'rm': self.cmd_delete,   # Unix alias
            
            # Text editor commands
            'notepad': self.cmd_simple_editor,
            'editor': self.cmd_simple_editor,
            'vi': self.cmd_simple_editor,  # Unix alias
            
            # Calculator and utilities
            'calc': self.cmd_calculator,
            'calculator': self.cmd_calculator,
            'time': self.cmd_time,
            'date': self.cmd_date,
            
            # Fun retro commands
            'games': self.cmd_games,
            'hello': self.cmd_hello_world,
            'banner': self.cmd_banner,
        }
        
    def start(self):
        """Start the simulator with startup sequence"""
        self.terminal.show_startup_sequence()
        time.sleep(1)
        
        # Show initial help
        self.terminal.typewriter_print(
            "Welcome! This is your personal retro computer - built by yours truly just like the classics from the 80s ;)",
            color="cyan"
        )
        self.terminal.typewriter_print(
            "Try 'create myfile.txt' to make a file, 'games' for fun, or 'demo' to see it work",
            color="yellow"
        )
        self.terminal.typewriter_print(
            "Type 'help' anytime to see what you can do. No programming knowledge required!",
            color="green"
        )
        
        # Main command loop
        self.main_loop()
        
    def main_loop(self):
        """Main command processing loop"""
        while self.running:
            try:
                self.terminal.show_prompt()
                command_line = self.terminal.get_input().strip()
                
                if not command_line:
                    continue
                    
                # Add to history
                self.add_to_history(command_line)
                
                # Parse and execute command
                self.execute_command(command_line)
                
            except KeyboardInterrupt:
                self.terminal.print_warning("\nUse 'quit' to exit.")
            except EOFError:
                break
                
        self.terminal.typewriter_print("Goodbye!", color="green")
        
    def execute_command(self, command_line: str):
        """Parse and execute a command"""
        parts = command_line.split()
        if not parts:
            return
            
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command in self.commands:
            try:
                self.commands[command](args)
            except Exception as e:
                self.terminal.print_error(f"Command error: {e}")
        else:
            self.terminal.print_error(f"Unknown command: {command}")
            self.terminal.print_info("Type 'help' for available commands.")
            
    def add_to_history(self, command: str):
        """Add command to history"""
        if len(self.command_history) >= self.max_history:
            self.command_history.pop(0)
        self.command_history.append(command)
        
    # Command implementations
    def cmd_help(self, args: List[str]):
        """Show help information"""
        if args:
            # Help for specific command
            command = args[0].lower()
            if command in self.commands:
                self.show_command_help(command)
            else:
                self.terminal.print_error(f"No help available for: {command}")
        else:
            self.terminal.show_help()
            
    def show_command_help(self, command: str):
        """Show detailed help for a specific command"""
        help_text = {
            'assemble': "ASSEMBLE - Enter interactive assembly mode\\nUsage: assemble",
            'load': "LOAD <filename> - Load program from file\\nUsage: load myprogram.asm",
            'run': "RUN - Execute loaded program\\nUsage: run",
            'step': "STEP [count] - Execute one or more instructions\\nUsage: step [5]",
            'debug': "DEBUG [on|off] - Enable/disable debug mode\\nUsage: debug on",
            'memory': "MEMORY [start] [end] - Show memory contents\\nUsage: memory 0 64",
            'breakpoint': "BREAKPOINT <add|remove|list> <addr> - Manage breakpoints\\nUsage: breakpoint add 10",
        }
        
        if command in help_text:
            self.terminal.typewriter_print(help_text[command], color="cyan")
        else:
            self.terminal.print_info("No detailed help available for this command.")
            
    def cmd_clear(self, args: List[str]):
        """Clear the screen"""
        self.terminal.clear_screen()
        
    def cmd_quit(self, args: List[str]):
        """Exit the simulator"""
        self.running = False
        
    def cmd_about(self, args: List[str]):
        """Show about information"""
        about_text = """
╔══════════════════════════════════════════════════╗
║          VON NEUMANN COMPUTER SIMULATOR          ║
║                                                  ║
║  A faithful recreation of a stored-program       ║
║  computer based on the Von Neumann architecture  ║
║                                                  ║
║  Created by: Davis                               ║
║  Version: 1.0                                    ║
║                                                  ║
║  Features:                                       ║
║  • 256 bytes unified memory                      ║
║  • 8-bit CPU with ALU                           ║
║  • Interactive assembler                         ║
║  • Real-time debugging                           ║
║  • Retro terminal interface                      ║
║                                                  ║
╚══════════════════════════════════════════════════╝
        """
        self.terminal.typewriter_print(about_text, delay=0.01, color="green")
        
    def cmd_status(self, args: List[str]):
        """Show system status"""
        self.terminal.show_separator()
        self.terminal.show_cpu_status(self.cpu)
        
        # Memory usage
        stats = self.memory_viewer.analyze_memory_usage()
        self.terminal.print_info(f"Memory: {stats['utilization']:.1f}% used, {stats['instructions']} instructions, {stats['non_zero_data']} data bytes")
        
        # Program status
        if self.program_loaded:
            self.terminal.print_success("Program loaded and ready")
        else:
            self.terminal.print_warning("No program loaded")
            
        self.terminal.show_separator()
        
    def cmd_reset(self, args: List[str]):
        """Reset the computer"""
        self.cpu.reset()
        self.memory = Memory(256)
        self.cpu.memory = self.memory
        self.memory_viewer.memory = self.memory
        self.program_loaded = False
        self.terminal.print_success("Computer reset complete")
        
    def cmd_memory(self, args: List[str]):
        """Show memory contents"""
        if len(args) == 0:
            # Show memory around PC
            output = self.memory_viewer.display_around_pc()
        elif len(args) == 1:
            try:
                start_addr = int(args[0], 16) if args[0].startswith('0x') else int(args[0])
                output = self.memory_viewer.display_memory_range(start_addr, start_addr + 64)
            except ValueError:
                self.terminal.print_error("Invalid address format")
                return
        elif len(args) == 2:
            try:
                start_addr = int(args[0], 16) if args[0].startswith('0x') else int(args[0])
                end_addr = int(args[1], 16) if args[1].startswith('0x') else int(args[1])
                output = self.memory_viewer.display_memory_range(start_addr, end_addr)
            except ValueError:
                self.terminal.print_error("Invalid address format")
                return
        else:
            self.terminal.print_error("Usage: memory [start] [end]")
            return
            
        print(output)
        
    def cmd_registers(self, args: List[str]):
        """Show register contents"""
        self.terminal.show_cpu_status(self.cpu)
        
    def cmd_assemble(self, args: List[str]):
        """Enter interactive assembly mode"""
        self.terminal.typewriter_print("Entering assembly mode. Type 'END' to finish, 'CANCEL' to abort.", color="cyan")
        self.terminal.typewriter_print("Enter your assembly code:", color="green")
        
        lines = []
        line_num = 1
        
        while True:
            prompt = f"{line_num:03d}> "
            print(f"\033[36m{prompt}\033[0m", end='')
            line = self.terminal.get_input()
            
            if line.upper() == 'END':
                break
            elif line.upper() == 'CANCEL':
                self.terminal.print_warning("Assembly cancelled")
                return
                
            lines.append(line)
            line_num += 1
            
        # Assemble the code
        source_code = '\n'.join(lines)
        instructions, errors = self.assembler.assemble(source_code)
        
        if errors:
            self.terminal.print_error("Assembly errors:")
            for error in errors:
                self.terminal.print_error(f"  {error}")
        else:
            # Load program into memory
            self.load_program_to_memory(instructions)
            self.current_program = source_code
            self.program_loaded = True
            self.terminal.print_success(f"Program assembled successfully! {len(instructions)} instructions loaded.")
            
            # Show listing
            listing = self.assembler.create_listing(source_code, instructions)
            self.terminal.typewriter_print("\nProgram Listing:", color="yellow")
            for line in listing.split('\n'):
                print(line)
                
    def load_program_to_memory(self, instructions: List[tuple]):
        """Load assembled instructions into memory"""
        for addr, instruction in enumerate(instructions):
            if addr < len(self.memory.cells):
                self.memory.write(addr, instruction)
                
    def cmd_load(self, args: List[str]):
        """Load program from file"""
        if not args:
            self.terminal.print_error("Usage: load <filename>")
            return
            
        filename = args[0]
        source_code = self.io_system.load_text_file(filename)
        
        if source_code is None:
            return
            
        # Assemble the loaded code
        instructions, errors = self.assembler.assemble(source_code)
        
        if errors:
            self.terminal.print_error("Assembly errors in loaded file:")
            for error in errors:
                self.terminal.print_error(f"  {error}")
        else:
            self.load_program_to_memory(instructions)
            self.current_program = source_code
            self.program_loaded = True
            self.terminal.print_success(f"Program loaded from {filename}! {len(instructions)} instructions.")
            
    def cmd_save(self, args: List[str]):
        """Save current program to file"""
        if not args:
            self.terminal.print_error("Usage: save <filename>")
            return
            
        if not self.current_program:
            self.terminal.print_error("No program to save")
            return
            
        filename = args[0]
        if self.io_system.save_text_file(filename, self.current_program):
            self.terminal.print_success(f"Program saved to {filename}")
            
    def cmd_run(self, args: List[str]):
        """Run the loaded program"""
        if not self.program_loaded:
            self.terminal.print_error("No program loaded. Use 'load' or 'assemble' first.")
            return
            
        self.terminal.print_success("Starting program execution...")
        
        # Reset CPU to start of program
        self.cpu.pc = 0
        self.cpu.running = True
        
        # Connect I/O system to CPU
        self.setup_io_connection()
        
        try:
            start_time = time.time()
            
            if self.debug_mode:
                self.run_with_debug()
            else:
                self.cpu.run()
                
            end_time = time.time()
            
            self.terminal.print_success(f"Program completed in {end_time - start_time:.3f} seconds")
            self.terminal.print_info(f"Instructions executed: {self.cpu.instruction_count}")
            
            # Show any output
            output = self.cpu.get_output()
            if output:
                self.terminal.typewriter_print("Program Output:", color="yellow")
                for value in output:
                    if 32 <= value <= 126:
                        print(chr(value), end='')
                    else:
                        print(f"[{value}]", end='')
                print()  # Newline
                
        except KeyboardInterrupt:
            self.terminal.print_warning("Program execution interrupted")
            self.cpu.running = False
            
    def run_with_debug(self):
        """Run program with debug output"""
        self.cpu.enable_debug()
        
        while self.cpu.running:
            # Show current instruction
            if self.cpu.pc < len(self.memory.cells):
                current_instr = self.memory.read(self.cpu.pc)
                self.terminal.print_info(f"PC:{self.cpu.pc:04X} -> {current_instr}")
                
            # Execute one step
            self.cpu.step()
            
            # Show registers after execution
            status = self.cpu.get_status()
            self.terminal.print_info(f"Registers: A={status['registers']['A']:02X} B={status['registers']['B']:02X} C={status['registers']['C']:02X}")
            
            time.sleep(0.1)  # Small delay for readability
            
    def setup_io_connection(self):
        """Connect I/O system to CPU"""
        # This would be where we connect the I/O system to the CPU
        # For now, we'll use the CPU's built-in I/O buffers
        pass
        
    def cmd_step(self, args: List[str]):
        """Execute one or more instructions"""
        if not self.program_loaded:
            self.terminal.print_error("No program loaded")
            return
            
        steps = 1
        if args:
            try:
                steps = int(args[0])
            except ValueError:
                self.terminal.print_error("Invalid step count")
                return
                
        for i in range(steps):
            if not self.cpu.running:
                self.terminal.print_warning("Program halted")
                break
                
            old_pc = self.cpu.pc
            if self.cpu.step():
                self.terminal.print_info(f"Step {i+1}: PC {old_pc:04X} -> {self.cpu.pc:04X}")
            else:
                self.terminal.print_warning("No more instructions")
                break
                
        # Show current status
        self.cmd_status([])
        
    def cmd_demo(self, args: List[str]):
        """Run demonstration program"""
        demo_program = """
; Demo: Add two numbers and display result
LOAD A, #15    ; Load 15 into register A
LOAD B, #27    ; Load 27 into register B
ADD C, A, B    ; Add A and B, store in C
OUTPUT C       ; Output the result (42)
HALT           ; Stop execution
        """
        
        self.terminal.typewriter_print("Loading demonstration program...", color="cyan")
        
        instructions, errors = self.assembler.assemble(demo_program)
        if not errors:
            self.load_program_to_memory(instructions)
            self.current_program = demo_program
            self.program_loaded = True
            
            self.terminal.print_success("Demo program loaded!")
            self.terminal.typewriter_print("Program listing:", color="yellow")
            
            for line in demo_program.strip().split('\n'):
                self.terminal.typewriter_print(line, delay=0.02, color="green")
                
            self.terminal.print_info("Type 'run' to execute the demonstration.")
            
    def cmd_samples(self, args: List[str]):
        """Show sample programs menu"""
        samples = self.assembler.get_sample_programs()
        
        self.terminal.typewriter_print("Available Sample Programs:", color="yellow")
        
        for i, (name, _) in enumerate(samples.items(), 1):
            self.terminal.typewriter_print(f"{i}. {name}", color="green")
            
        choice = self.terminal.get_input("\nSelect a program (1-{}) or press Enter to cancel: ".format(len(samples)))
        
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(samples):
                sample_names = list(samples.keys())
                selected_name = sample_names[choice_num - 1]
                selected_program = samples[selected_name]
                
                self.terminal.print_success(f"Loading: {selected_name}")
                
                instructions, errors = self.assembler.assemble(selected_program)
                if not errors:
                    self.load_program_to_memory(instructions)
                    self.current_program = selected_program
                    self.program_loaded = True
                    self.terminal.print_success("Sample program loaded! Type 'run' to execute.")
                else:
                    self.terminal.print_error("Error in sample program")
                    
    def cmd_tutorial(self, args: List[str]):
        """Show interactive tutorial"""
        tutorial_text = """
╔══════════════════════════════════════════════════╗
║              BASIC TUTORIAL                      ║
╚══════════════════════════════════════════════════╝

Welcome to the Von Neumann Computer Simulator!

This computer follows the stored-program concept where both
instructions and data are stored in the same memory.

BASIC OPERATIONS:
1. Write assembly code using 'assemble' command
2. Load programs from files using 'load filename'
3. Execute programs using 'run'
4. Debug step-by-step using 'step'

TRY THIS:
Type 'demo' to see a simple program in action!

AVAILABLE INSTRUCTIONS:
• LOAD reg, addr    - Load from memory to register
• STORE reg, addr   - Store register to memory  
• ADD dest, src1, src2 - Add two registers
• SUB dest, src1, src2 - Subtract registers
• OUTPUT reg        - Output register value
• HALT             - Stop execution

For more commands, type 'help'
        """
        
        self.terminal.typewriter_print(tutorial_text, delay=0.005, color="cyan")
        
    # Additional command implementations
    def cmd_debug(self, args: List[str]):
        """Enable/disable debug mode"""
        if not args:
            status = "ON" if self.debug_mode else "OFF"
            self.terminal.print_info(f"Debug mode is {status}")
        elif args[0].lower() in ['on', 'enable', 'true']:
            self.debug_mode = True
            self.terminal.print_success("Debug mode enabled")
        elif args[0].lower() in ['off', 'disable', 'false']:
            self.debug_mode = False
            self.terminal.print_success("Debug mode disabled")
        else:
            self.terminal.print_error("Usage: debug [on|off]")
            
    def cmd_breakpoint(self, args: List[str]):
        """Manage breakpoints"""
        if not args:
            breakpoints = list(self.cpu.breakpoints)
            if breakpoints:
                self.terminal.print_info("Active breakpoints:")
                for bp in sorted(breakpoints):
                    self.terminal.print_info(f"  {bp:04X}")
            else:
                self.terminal.print_info("No breakpoints set")
        elif args[0].lower() == 'add' and len(args) > 1:
            try:
                addr = int(args[1], 16) if args[1].startswith('0x') else int(args[1])
                self.cpu.set_breakpoint(addr)
                self.terminal.print_success(f"Breakpoint set at {addr:04X}")
            except ValueError:
                self.terminal.print_error("Invalid address")
        elif args[0].lower() == 'remove' and len(args) > 1:
            try:
                addr = int(args[1], 16) if args[1].startswith('0x') else int(args[1])
                self.cpu.remove_breakpoint(addr)
                self.terminal.print_success(f"Breakpoint removed from {addr:04X}")
            except ValueError:
                self.terminal.print_error("Invalid address")
        elif args[0].lower() == 'clear':
            self.cpu.clear_breakpoints()
            self.terminal.print_success("All breakpoints cleared")
        else:
            self.terminal.print_error("Usage: breakpoint [add|remove|clear] [address]")
            
    def cmd_continue(self, args: List[str]):
        """Continue execution from current position"""
        if not self.program_loaded:
            self.terminal.print_error("No program loaded")
            return
            
        self.terminal.print_info("Continuing execution...")
        self.cmd_run([])
        
    def cmd_stop(self, args: List[str]):
        """Stop current execution"""
        self.cpu.running = False
        self.terminal.print_warning("Execution stopped")
        
    def cmd_watch(self, args: List[str]):
        """Watch memory location or register"""
        self.terminal.print_info("Watch functionality not yet implemented")
        
    def cmd_trace(self, args: List[str]):
        """Show execution trace"""
        if hasattr(self.cpu, 'execution_history'):
            self.terminal.print_info("Execution trace:")
            for entry in self.cpu.execution_history[-10:]:  # Last 10 entries
                self.terminal.typewriter_print(entry, delay=0.01, color="green")
        else:
            self.terminal.print_info("No trace available")
            
    def cmd_dir(self, args: List[str]):
        """List files in current directory"""
        try:
            files = os.listdir('.')
            asm_files = [f for f in files if f.endswith('.asm') or f.endswith('.txt')]
            
            if asm_files:
                self.terminal.print_info("Assembly files:")
                for file in sorted(asm_files):
                    self.terminal.typewriter_print(f"  {file}", color="green")
            else:
                self.terminal.print_info("No assembly files found")
        except Exception as e:
            self.terminal.print_error(f"Error listing files: {e}")
            
    def cmd_type(self, args: List[str]):
        """Display file contents"""
        if not args:
            self.terminal.print_error("Usage: type <filename>")
            return
            
        filename = args[0]
        content = self.io_system.load_text_file(filename)
        
        if content:
            self.terminal.typewriter_print(f"Contents of {filename}:", color="yellow")
            for line in content.split('\n'):
                self.terminal.typewriter_print(line, delay=0.01, color="green")
                
    def cmd_edit(self, args: List[str]):
        """Simple text editor"""
        self.terminal.print_info("Simple editor mode. Type 'SAVE' to save, 'QUIT' to exit without saving.")
        
        lines = []
        line_num = 1
        
        while True:
            prompt = f"Edit {line_num:03d}> "
            print("\033[32m" + prompt, end='')
            line = input()
            
            if line.upper() == 'SAVE':
                if args:
                    filename = args[0]
                    content = '\n'.join(lines)
                    if self.io_system.save_text_file(filename, content):
                        self.terminal.print_success(f"File saved as {filename}")
                else:
                    self.terminal.print_error("No filename specified")
                break
            elif line.upper() == 'QUIT':
                self.terminal.print_warning("Edit cancelled")
                break
                
            lines.append(line)
            line_num += 1
            
    def cmd_list(self, args: List[str]):
        """List current program"""
        if self.current_program:
            self.terminal.typewriter_print("Current Program:", color="yellow")
            for i, line in enumerate(self.current_program.split('\n'), 1):
                self.terminal.typewriter_print(f"{i:03d}: {line}", delay=0.01, color="green")
        else:
            self.terminal.print_info("No program loaded")
    
    # ===== NEW USER-FRIENDLY FILE OPERATIONS =====
    
    def cmd_create(self, args: List[str]):
        """Create a new file"""
        if not args:
            filename = self.terminal.get_input("Enter filename: ")
        else:
            filename = args[0]
            
        if not filename:
            self.terminal.print_error("Filename cannot be empty")
            return
            
        # Check if file already exists
        if os.path.exists(filename):
            overwrite = self.terminal.get_input(f"File '{filename}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() not in ['y', 'yes']:
                self.terminal.print_info("File creation cancelled")
                return
                
        # Create empty file
        try:
            with open(filename, 'w') as f:
                f.write("")
            self.terminal.print_success(f"File '{filename}' created successfully!")
            self.terminal.print_info("Use 'write filename' to add content or 'editor filename' to edit")
        except Exception as e:
            self.terminal.print_error(f"Could not create file: {e}")
    
    def cmd_write(self, args: List[str]):
        """Write text to a file"""
        if not args:
            filename = self.terminal.get_input("Enter filename: ")
        else:
            filename = args[0]
            
        if not filename:
            self.terminal.print_error("Filename cannot be empty")
            return
            
        self.terminal.typewriter_print(f"Writing to '{filename}'. Type your text below.", color="cyan")
        self.terminal.typewriter_print("Type 'EOF' on a new line to finish, or 'CANCEL' to abort.", color="yellow")
        
        lines = []
        line_num = 1
        
        while True:
            prompt = f"{line_num:03d}> "
            print(f"\033[36m{prompt}\033[0m", end='')
            line = input()
            
            if line.upper() == 'EOF':
                break
            elif line.upper() == 'CANCEL':
                self.terminal.print_warning("Write operation cancelled")
                return
                
            lines.append(line)
            line_num += 1
            
        content = '\n'.join(lines)
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            self.terminal.print_success(f"Text written to '{filename}' successfully!")
            self.terminal.print_info(f"{len(lines)} lines, {len(content)} characters")
        except Exception as e:
            self.terminal.print_error(f"Could not write to file: {e}")
    
    def cmd_append(self, args: List[str]):
        """Append text to an existing file"""
        if not args:
            filename = self.terminal.get_input("Enter filename: ")
        else:
            filename = args[0]
            
        if not filename:
            self.terminal.print_error("Filename cannot be empty")
            return
            
        if not os.path.exists(filename):
            self.terminal.print_error(f"File '{filename}' does not exist. Use 'create' first.")
            return
            
        self.terminal.typewriter_print(f"Appending to '{filename}'. Type your text below.", color="cyan")
        self.terminal.typewriter_print("Type 'EOF' on a new line to finish, or 'CANCEL' to abort.", color="yellow")
        
        lines = []
        line_num = 1
        
        while True:
            prompt = f"A{line_num:02d}> "
            print(f"\033[36m{prompt}\033[0m", end='')
            line = input()
            
            if line.upper() == 'EOF':
                break
            elif line.upper() == 'CANCEL':
                self.terminal.print_warning("Append operation cancelled")
                return
                
            lines.append(line)
            line_num += 1
            
        content = '\n'.join(lines)
        
        try:
            with open(filename, 'a') as f:
                f.write('\n' + content)
            self.terminal.print_success(f"Text appended to '{filename}' successfully!")
        except Exception as e:
            self.terminal.print_error(f"Could not append to file: {e}")
    
    def cmd_copy(self, args: List[str]):
        """Copy a file"""
        if len(args) < 2:
            source = self.terminal.get_input("Enter source filename: ")
            dest = self.terminal.get_input("Enter destination filename: ")
        else:
            source, dest = args[0], args[1]
            
        if not source or not dest:
            self.terminal.print_error("Both source and destination filenames are required")
            return
            
        try:
            with open(source, 'r') as src_file:
                content = src_file.read()
                
            with open(dest, 'w') as dest_file:
                dest_file.write(content)
                
            self.terminal.print_success(f"File '{source}' copied to '{dest}' successfully!")
        except FileNotFoundError:
            self.terminal.print_error(f"Source file '{source}' not found")
        except Exception as e:
            self.terminal.print_error(f"Copy failed: {e}")
    
    def cmd_rename(self, args: List[str]):
        """Rename a file"""
        if len(args) < 2:
            old_name = self.terminal.get_input("Enter current filename: ")
            new_name = self.terminal.get_input("Enter new filename: ")
        else:
            old_name, new_name = args[0], args[1]
            
        if not old_name or not new_name:
            self.terminal.print_error("Both old and new filenames are required")
            return
            
        try:
            os.rename(old_name, new_name)
            self.terminal.print_success(f"File '{old_name}' renamed to '{new_name}' successfully!")
        except FileNotFoundError:
            self.terminal.print_error(f"File '{old_name}' not found")
        except Exception as e:
            self.terminal.print_error(f"Rename failed: {e}")
    
    def cmd_delete(self, args: List[str]):
        """Delete a file"""
        if not args:
            filename = self.terminal.get_input("Enter filename to delete: ")
        else:
            filename = args[0]
            
        if not filename:
            self.terminal.print_error("Filename cannot be empty")
            return
            
        if not os.path.exists(filename):
            self.terminal.print_error(f"File '{filename}' not found")
            return
            
        # Confirm deletion
        confirm = self.terminal.get_input(f"Are you sure you want to delete '{filename}'? (y/n): ")
        if confirm.lower() not in ['y', 'yes']:
            self.terminal.print_info("Deletion cancelled")
            return
            
        try:
            os.remove(filename)
            self.terminal.print_success(f"File '{filename}' deleted successfully!")
        except Exception as e:
            self.terminal.print_error(f"Delete failed: {e}")
    
    def cmd_simple_editor(self, args: List[str]):
        """Simple text editor like classic computers"""
        if not args:
            filename = self.terminal.get_input("Enter filename to edit (or new filename): ")
        else:
            filename = args[0]
            
        if not filename:
            self.terminal.print_error("Filename cannot be empty")
            return
            
        # Load existing content if file exists
        lines = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    lines = f.read().split('\n')
                self.terminal.print_success(f"Loaded '{filename}' - {len(lines)} lines")
            except Exception as e:
                self.terminal.print_error(f"Could not load file: {e}")
                return
        else:
            self.terminal.print_info(f"Creating new file '{filename}'")
            
        self.terminal.typewriter_print("=== SIMPLE TEXT EDITOR ===", color="yellow")
        self.terminal.typewriter_print("Commands: LIST (show all lines), SAVE (save and exit), QUIT (exit without saving)", color="cyan")
        self.terminal.typewriter_print("          INSERT n (insert at line n), DELETE n (delete line n), EDIT n (edit line n)", color="cyan")
        self.terminal.typewriter_print("Or just type line numbers to edit directly.", color="cyan")
        
        # Show current content
        if lines:
            self.terminal.typewriter_print("\nCurrent content:", color="green")
            for i, line in enumerate(lines, 1):
                print(f"{i:03d}: {line}")
        
        while True:
            command = self.terminal.get_input("\nEditor> ").strip()
            
            if command.upper() == 'SAVE':
                try:
                    with open(filename, 'w') as f:
                        f.write('\n'.join(lines))
                    self.terminal.print_success(f"File '{filename}' saved successfully!")
                    break
                except Exception as e:
                    self.terminal.print_error(f"Save failed: {e}")
                    
            elif command.upper() == 'QUIT':
                confirm = self.terminal.get_input("Quit without saving? (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    self.terminal.print_warning("Exited without saving")
                    break
                    
            elif command.upper() == 'LIST':
                if lines:
                    for i, line in enumerate(lines, 1):
                        print(f"{i:03d}: {line}")
                else:
                    self.terminal.print_info("File is empty")
                    
            elif command.upper().startswith('INSERT '):
                try:
                    line_num = int(command.split()[1])
                    if 1 <= line_num <= len(lines) + 1:
                        new_line = self.terminal.get_input(f"Enter text for line {line_num}: ")
                        lines.insert(line_num - 1, new_line)
                        self.terminal.print_success(f"Line {line_num} inserted")
                    else:
                        self.terminal.print_error("Invalid line number")
                except (ValueError, IndexError):
                    self.terminal.print_error("Usage: INSERT line_number")
                    
            elif command.upper().startswith('DELETE '):
                try:
                    line_num = int(command.split()[1])
                    if 1 <= line_num <= len(lines):
                        deleted_line = lines.pop(line_num - 1)
                        self.terminal.print_success(f"Deleted line {line_num}: {deleted_line}")
                    else:
                        self.terminal.print_error("Invalid line number")
                except (ValueError, IndexError):
                    self.terminal.print_error("Usage: DELETE line_number")
                    
            elif command.upper().startswith('EDIT '):
                try:
                    line_num = int(command.split()[1])
                    if 1 <= line_num <= len(lines):
                        current_line = lines[line_num - 1]
                        self.terminal.print_info(f"Current line {line_num}: {current_line}")
                        new_line = self.terminal.get_input(f"Enter new text for line {line_num}: ")
                        lines[line_num - 1] = new_line
                        self.terminal.print_success(f"Line {line_num} updated")
                    else:
                        self.terminal.print_error("Invalid line number")
                except (ValueError, IndexError):
                    self.terminal.print_error("Usage: EDIT line_number")
                    
            elif command.isdigit():
                line_num = int(command)
                if line_num == 0:
                    # Add to beginning
                    new_line = self.terminal.get_input("Enter text for new line 1: ")
                    lines.insert(0, new_line)
                    self.terminal.print_success("Line added at beginning")
                elif 1 <= line_num <= len(lines):
                    # Edit existing line
                    current_line = lines[line_num - 1]
                    self.terminal.print_info(f"Current line {line_num}: {current_line}")
                    new_line = self.terminal.get_input(f"Enter new text for line {line_num}: ")
                    lines[line_num - 1] = new_line
                    self.terminal.print_success(f"Line {line_num} updated")
                elif line_num == len(lines) + 1:
                    # Add to end
                    new_line = self.terminal.get_input(f"Enter text for new line {line_num}: ")
                    lines.append(new_line)
                    self.terminal.print_success(f"Line {line_num} added")
                else:
                    self.terminal.print_error("Invalid line number")
            else:
                self.terminal.print_error("Unknown command. Type LIST, SAVE, QUIT, INSERT n, DELETE n, EDIT n, or a line number")
    
    # ===== CALCULATOR AND UTILITIES =====
    
    def cmd_calculator(self, args: List[str]):
        """Simple calculator"""
        if args:
            # Direct calculation
            expression = ' '.join(args)
            self.calculate_expression(expression)
        else:
            # Interactive mode
            self.terminal.typewriter_print("=== RETRO CALCULATOR ===", color="yellow")
            self.terminal.typewriter_print("Enter mathematical expressions. Type 'quit' to exit.", color="cyan")
            self.terminal.typewriter_print("Supported: +, -, *, /, (), hex (0x), binary (0b)", color="cyan")
            
            while True:
                expression = self.terminal.get_input("CALC> ")
                if expression.lower() in ['quit', 'exit']:
                    break
                self.calculate_expression(expression)
    
    def calculate_expression(self, expression: str):
        """Calculate mathematical expression safely"""
        try:
            # Simple safety check - only allow certain characters
            allowed_chars = set('0123456789+-*/()., xabcdefABCDEF')
            if not all(c in allowed_chars for c in expression.replace(' ', '')):
                self.terminal.print_error("Invalid characters in expression")
                return
                
            # Handle hex and binary
            if '0x' in expression.lower():
                # Convert hex to decimal for calculation
                import re
                hex_pattern = r'0x[0-9a-fA-F]+'
                for hex_match in re.finditer(hex_pattern, expression, re.IGNORECASE):
                    hex_value = int(hex_match.group(), 16)
                    expression = expression.replace(hex_match.group(), str(hex_value))
                    
            if '0b' in expression.lower():
                # Convert binary to decimal
                import re
                bin_pattern = r'0b[01]+'
                for bin_match in re.finditer(bin_pattern, expression, re.IGNORECASE):
                    bin_value = int(bin_match.group(), 2)
                    expression = expression.replace(bin_match.group(), str(bin_value))
            
            # Evaluate safely
            result = eval(expression, {"__builtins__": {}}, {})
            
            # Display result in multiple formats
            self.terminal.print_success(f"Result: {result}")
            if isinstance(result, (int, float)) and result == int(result):
                result_int = int(result)
                if result_int >= 0:
                    self.terminal.print_info(f"Hex: 0x{result_int:X}")
                    if result_int <= 255:
                        self.terminal.print_info(f"Binary: 0b{result_int:08b}")
                    else:
                        self.terminal.print_info(f"Binary: 0b{result_int:b}")
                        
        except ZeroDivisionError:
            self.terminal.print_error("Division by zero!")
        except Exception as e:
            self.terminal.print_error(f"Calculation error: {e}")
    
    def cmd_time(self, args: List[str]):
        """Show current time"""
        import datetime
        now = datetime.datetime.now()
        self.terminal.typewriter_print(f"Current time: {now.strftime('%H:%M:%S')}", color="green")
    
    def cmd_date(self, args: List[str]):
        """Show current date"""
        import datetime
        now = datetime.datetime.now()
        self.terminal.typewriter_print(f"Current date: {now.strftime('%Y-%m-%d (%A)')}", color="green")
    
    # ===== FUN RETRO COMMANDS =====
    
    def cmd_games(self, args: List[str]):
        """Simple retro games"""
        self.terminal.typewriter_print("=== RETRO GAMES ===", color="yellow")
        self.terminal.typewriter_print("1. Guess the Number", color="green")
        self.terminal.typewriter_print("2. Simple Math Quiz", color="green")
        self.terminal.typewriter_print("3. Word Reverser", color="green")
        
        choice = self.terminal.get_input("Select a game (1-3): ")
        
        if choice == '1':
            self.play_guess_number()
        elif choice == '2':
            self.play_math_quiz()
        elif choice == '3':
            self.play_word_reverser()
        else:
            self.terminal.print_error("Invalid choice")
    
    def play_guess_number(self):
        """Guess the number game"""
        import random
        number = random.randint(1, 100)
        attempts = 0
        
        self.terminal.typewriter_print("I'm thinking of a number between 1 and 100!", color="cyan")
        
        while True:
            try:
                guess = int(self.terminal.get_input("Your guess: "))
                attempts += 1
                
                if guess == number:
                    self.terminal.print_success(f"Congratulations! You got it in {attempts} attempts!")
                    break
                elif guess < number:
                    self.terminal.print_info("Too low! Try higher.")
                else:
                    self.terminal.print_info("Too high! Try lower.")
                    
            except ValueError:
                self.terminal.print_error("Please enter a valid number")
            except KeyboardInterrupt:
                self.terminal.print_warning(f"\nGame cancelled. The number was {number}")
                break
    
    def play_math_quiz(self):
        """Simple math quiz"""
        import random
        score = 0
        questions = 5
        
        self.terminal.typewriter_print(f"Math Quiz - {questions} questions!", color="cyan")
        
        for i in range(questions):
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operation = random.choice(['+', '-', '*'])
            
            if operation == '+':
                answer = a + b
            elif operation == '-':
                answer = a - b
            else:  # multiplication
                answer = a * b
                
            try:
                user_answer = int(self.terminal.get_input(f"Question {i+1}: {a} {operation} {b} = "))
                
                if user_answer == answer:
                    self.terminal.print_success("Correct!")
                    score += 1
                else:
                    self.terminal.print_error(f"Wrong! The answer was {answer}")
                    
            except ValueError:
                self.terminal.print_error(f"Invalid answer! The correct answer was {answer}")
            except KeyboardInterrupt:
                self.terminal.print_warning("\nQuiz cancelled")
                return
                
        self.terminal.typewriter_print(f"\nQuiz complete! Score: {score}/{questions}", color="yellow")
        
        if score == questions:
            self.terminal.print_success("Perfect score! You're a math wizard!")
        elif score >= questions * 0.8:
            self.terminal.print_success("Great job!")
        elif score >= questions * 0.6:
            self.terminal.print_info("Not bad, keep practicing!")
        else:
            self.terminal.print_info("Keep studying those math facts!")
    
    def play_word_reverser(self):
        """Word reverser game"""
        self.terminal.typewriter_print("Word Reverser - I'll reverse whatever you type!", color="cyan")
        self.terminal.typewriter_print("Type 'quit' to exit", color="yellow")
        
        while True:
            text = self.terminal.get_input("Enter text: ")
            if text.lower() == 'quit':
                break
            reversed_text = text[::-1]
            self.terminal.typewriter_print(f"Reversed: {reversed_text}", color="green")
    
    def cmd_hello_world(self, args: List[str]):
        """Classic Hello World"""
        hello_art = """
╔═══════════════════════════════════════╗
║              HELLO, WORLD!            ║
║                                       ║
║  Welcome to your retro computer!      ║
║  May your computing be bug-free       ║
║  and your programs run swiftly!       ║
╚═══════════════════════════════════════╝
        """
        self.terminal.typewriter_print(hello_art, delay=0.01, color="green")
    
    def cmd_banner(self, args: List[str]):
        """Create a banner with text"""
        if args:
            text = ' '.join(args)
        else:
            text = self.terminal.get_input("Enter banner text: ")
            
        if text:
            width = max(len(text) + 4, 20)
            border = "═" * width
            
            banner = f"""
╔{border}╗
║  {text.center(width-4)}  ║
╚{border}╝
            """
            self.terminal.typewriter_print(banner, delay=0.01, color="yellow")

def main():
    """Main entry point"""
    try:
        simulator = VonNeumannSimulator()
        simulator.start()
    except KeyboardInterrupt:
        print("\\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()