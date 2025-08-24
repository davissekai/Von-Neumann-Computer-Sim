/**
 * Von Neumann Computer Simulator - Web Version
 */

class VonNeumannComputer {
    constructor() {
        this.memory = new Array(256).fill(0);
        this.cpu = { pc: 0, registers: { A: 0, B: 0, C: 0 }, running: false };
        this.fileSystem = new Map();
        this.commandHistory = [];
        this.historyIndex = -1;
        this.soundEnabled = true;
        
        this.initializeFileSystem();
        this.setupEventListeners();
        this.initializeSounds();
        this.displayStartupSequence();
    }
    
    initializeSounds() {
        // Create audio context for retro sound effects
        this.audioContext = null;
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Audio not supported');
            this.soundEnabled = false;
        }
    }
    
    playSound(frequency = 440, duration = 100, type = 'square') {
        if (!this.soundEnabled || !this.audioContext) return;
        
        try {
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            oscillator.frequency.setValueAtTime(frequency, this.audioContext.currentTime);
            oscillator.type = type;
            
            gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration / 1000);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + duration / 1000);
        } catch (e) {
            // Silent fail for sound issues
        }
    }
    
    playBootSound() {
        // Classic computer boot sound sequence
        setTimeout(() => this.playSound(220, 150), 0);
        setTimeout(() => this.playSound(330, 150), 200);
        setTimeout(() => this.playSound(440, 150), 400);
        setTimeout(() => this.playSound(550, 300), 600);
    }
    
    playKeyPressSound() {
        this.playSound(800, 50, 'square');
    }
    
    playErrorSound() {
        this.playSound(150, 200, 'sawtooth');
    }
    
    playSuccessSound() {
        setTimeout(() => this.playSound(440, 100), 0);
        setTimeout(() => this.playSound(660, 150), 120);
    }
    
    initializeFileSystem() {
        this.fileSystem.set('readme.txt', `Welcome to your retro computer!

Try these commands:
- help (see all commands)
- games (play retro games)  
- calc (calculator)
- create test.txt (make a new file)
- demo (see a working program)
- tutorial (interactive learning)
- samples (view sample programs)`);

        this.fileSystem.set('hello.asm', `; Hello World Program
LOAD A, #72
OUTPUT A
HALT`);
        
        this.fileSystem.set('tutorial.txt', `=== VON NEUMANN ARCHITECTURE TUTORIAL ===

1. MEMORY: Stores both programs and data
   - Try: create mydata.txt
   - Try: write mydata.txt

2. CPU: Executes instructions step by step
   - Try: status (see CPU state)
   - Try: demo (see CPU in action)

3. I/O: Input/Output operations
   - Try: type readme.txt (input from file)
   - Try: calc 5+3 (output result)

4. PROGRAMMING: Write simple programs
   - Try: samples (see example programs)
   - Try: editor myprogram.txt

Type 'interactive' for hands-on learning!`);
        
        this.fileSystem.set('samples.txt', `=== SAMPLE PROGRAMS ===

1. FIBONACCI SEQUENCE:
   create fib.txt
   write fib.txt
   (Enter: 1, 1, 2, 3, 5, 8, 13...)

2. CALCULATOR PROGRAMS:
   calc 2+2
   calc 10*5
   calc 100/4

3. FILE OPERATIONS:
   create notes.txt
   write notes.txt
   type notes.txt
   
4. ASCII ART:
   banner HELLO
   ascii
   
5. SYSTEM INFO:
   time
   date
   status

Try any of these to learn computing basics!`);
        
        this.fileSystem.set('fibonacci.py', `# Fibonacci Calculator
# A classic computer science algorithm

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate first 10 numbers
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`);
    }
    
    setupEventListeners() {
        const input = document.getElementById('command-input');
        input.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Mobile-specific enhancements
        this.setupMobileEnhancements(input);
        
        // Focus handling for mobile
        this.setupFocusHandling(input);
        
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.target.closest('.modal').style.display = 'none';
            });
        });
        
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }
    
    setupMobileEnhancements(input) {
        // Detect if device is mobile
        this.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                       ('ontouchstart' in window) || 
                       (navigator.maxTouchPoints > 0);
        
        if (this.isMobile) {
            // Add touch-friendly virtual keyboard
            this.createVirtualKeyboard();
            
            // Prevent zoom on double tap
            document.addEventListener('touchstart', function(e) {
                if (e.touches.length > 1) {
                    e.preventDefault();
                }
            }, { passive: false });
            
            let lastTouchEnd = 0;
            document.addEventListener('touchend', function(e) {
                const now = (new Date()).getTime();
                if (now - lastTouchEnd <= 300) {
                    e.preventDefault();
                }
                lastTouchEnd = now;
            }, false);
            
            // Only focus input when user specifically taps the input area
            input.addEventListener('focus', () => {
                input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
        }
    }
    
    createVirtualKeyboard() {
        const keyboardContainer = document.createElement('div');
        keyboardContainer.className = 'virtual-keyboard';
        keyboardContainer.innerHTML = `
            <div class="keyboard-row">
                <button class="key-btn" data-key="help">help</button>
                <button class="key-btn" data-key="clear">clear</button>
                <button class="key-btn" data-key="dir">dir</button>
                <button class="key-btn" data-key="games">games</button>
            </div>
            <div class="keyboard-row">
                <button class="key-btn" data-key="create ">create</button>
                <button class="key-btn" data-key="write ">write</button>
                <button class="key-btn" data-key="type ">type</button>
                <button class="key-btn" data-key="demo">demo</button>
            </div>
        `;
        
        document.body.appendChild(keyboardContainer);
        
        // Add event listeners to virtual keyboard
        keyboardContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('key-btn')) {
                const input = document.getElementById('command-input');
                const command = e.target.dataset.key;
                input.value = command;
                input.focus();
                
                // If it's a complete command, execute it
                if (!command.endsWith(' ')) {
                    this.executeCommand(command);
                    input.value = '';
                }
            }
        });
    }
    
    setupFocusHandling(input) {
        // Keep input focused on mobile
        if (this.isMobile) {
            input.focus();
            
            // Re-focus when modal closes
            document.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal') || e.target.classList.contains('close')) {
                    setTimeout(() => input.focus(), 100);
                }
            });
            
            // Focus after theme change
            const themeSelector = document.getElementById('theme-selector');
            if (themeSelector) {
                themeSelector.addEventListener('change', () => {
                    setTimeout(() => input.focus(), 100);
                });
            }
        } else {
            input.focus();
        }
    }
    
    displayStartupSequence() {
        this.playBootSound();
        setTimeout(() => {
            document.getElementById('startup').style.display = 'none';
            this.showBootMessages();
        }, 3000);
    }
    
    async showBootMessages() {
        const messages = [
            '[SYSTEM INITIALIZING...]',
            '[CHECKING MEMORY... 256 BYTES OK]',
            '[LOADING CPU... OK]', 
            '[INITIALIZING REGISTERS... OK]',
            '[SETTING UP I/O SUBSYSTEM... OK]',
            '[SYSTEM READY]',
            '',
            'Greetings,\n I am Von Neu, your personal retro computer - built by my master, Renhuang Dey.',
            'Try "create myfile.txt" to make a file, "games" for recreation, or "demo" to see how I work.',
            'Type "help" anytime to see what you can do.\n Now, you may enjoy my master\'s creation. ',
            ''
        ];
        
        for (let msg of messages) {
            await this.typeMessage(msg, msg.includes('[') ? 'info' : 'success');
            await this.delay(400);
        }
        this.updateStatus();
    }
    
    async typeMessage(text, className = '', delay = 20) {
        const output = document.getElementById('output');
        const line = document.createElement('div');
        if (className) line.className = className;
        
        output.appendChild(line);
        
        for (let char of text) {
            line.textContent += char;
            await this.delay(delay);
        }
        
        output.scrollTop = output.scrollHeight;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    handleKeyDown(e) {
        const input = e.target;
        
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (command) {
                this.addToHistory(command);
                this.executeCommand(command);
            }
            input.value = '';
            this.historyIndex = -1;
        }
    }
    
    addToHistory(command) {
        this.commandHistory.push(command);
        if (this.commandHistory.length > 20) this.commandHistory.shift();
    }
    
    async executeCommand(commandLine) {
        this.playKeyPressSound();
        await this.typeMessage(`VON-NEU> ${commandLine}`, 'highlight', 5);
        
        const parts = commandLine.split(' ');
        const command = parts[0].toLowerCase();
        const args = parts.slice(1);
        
        switch (command) {
            case 'help': this.showHelp(); break;
            case 'clear': this.clearScreen(); break;
            case 'about': this.showAbout(); break;
            case 'create': case 'new': this.createFile(args); break;
            case 'write': this.writeFile(args); break;
            case 'type': case 'cat': this.displayFile(args); break;
            case 'dir': case 'ls': this.listFiles(); break;
            case 'delete': case 'del': this.deleteFile(args); break;
            case 'editor': case 'edit': this.openEditor(args); break;
            case 'status': this.showStatus(); break;
            case 'reset': this.resetComputer(); break;
            case 'demo': this.runDemo(); break;
            case 'calc': this.openCalculator(args); break;
            case 'time': this.showTime(); break;
            case 'date': this.showDate(); break;
            case 'games': this.openGames(); break;
            case 'hello': this.showHelloWorld(); break;
            case 'banner': this.createBanner(args); break;
            case 'sound': this.toggleSound(); break;
            case 'ascii': this.showASCIIArt(); break;
            case 'tutorial': this.startTutorial(); break;
            case 'samples': this.showSamples(); break;
            case 'interactive': this.startInteractiveTutorial(); break;
            case 'chat': this.handleChatCommand(args); break;
            case 'von-neu': this.openVonNeuChat(); break;
            
            // Von Neu Chatroom Commands
            case 'chat-new': this.handleChatNew(args); break;
            case 'chat-switch': this.handleChatSwitch(args); break;
            case 'chat-list': this.handleChatList(); break;
            case 'chat-delete': this.handleChatDelete(args); break;
            case 'chat-clear': this.handleChatClear(args); break;
            case 'chat-status': this.handleChatStatus(); break;
            default:
                this.playErrorSound();
                await this.typeMessage(`ERROR: Unknown command: ${command}`, 'error');
                await this.typeMessage('Type "help" for available commands.', 'info');
        }
        this.updateStatus();
    }
    
    async showHelp() {
        const helpText = `═══ COMMANDS ═══

FILES: create, write, type, dir, delete, editor
COMPUTER: status, reset, demo, calc
LEARNING: tutorial, samples, interactive
FUN: games, hello, banner, time, date, ascii
SYSTEM: help, clear, about, sound

VON NEU AI CHAT:
von-neu (open chat), chat-new <room>, chat-switch <room>
chat-list, chat-delete <room>, chat-clear [room], chat-status

NEW USER? Try: interactive
Quick start: tutorial, samples, demo
Type "sound" to toggle sound effects`;
        
        await this.typeMessage(helpText, 'success', 3);
    }
    
    clearScreen() {
        document.getElementById('output').innerHTML = '';
    }
    
    async showAbout() {
        const aboutText = `╔═══════════════════════════════════════╗
║   VON NEUMANN COMPUTER SIMULATOR      ║
║   Web Version by Davis                ║
║   A retro computing experience!       ║
╚═══════════════════════════════════════╝`;
        await this.typeMessage(aboutText, 'success', 10);
    }
    
    async createFile(args) {
        if (!args[0]) {
            await this.typeMessage('Usage: create <filename>', 'error');
            return;
        }
        
        const filename = args[0];
        if (this.fileSystem.has(filename)) {
            await this.typeMessage(`File '${filename}' already exists!`, 'warning');
            return;
        }
        
        this.fileSystem.set(filename, '');
        this.playSuccessSound();
        await this.typeMessage(`SUCCESS: File '${filename}' created!`, 'success');
    }
    
    async writeFile(args) {
        if (!args[0]) {
            await this.typeMessage('Usage: write <filename>', 'error');
            return;
        }
        
        const filename = args[0];
        if (!this.fileSystem.has(filename)) {
            await this.typeMessage(`File not found. Use 'create ${filename}' first.`, 'error');
            return;
        }
        
        const content = prompt(`Enter content for '${filename}':`);
        if (content !== null) {
            this.fileSystem.set(filename, content);
            await this.typeMessage(`SUCCESS: Content written to '${filename}'!`, 'success');
        }
    }
    
    async displayFile(args) {
        if (!args[0]) {
            await this.typeMessage('Usage: type <filename>', 'error');
            return;
        }
        
        const filename = args[0];
        if (!this.fileSystem.has(filename)) {
            await this.typeMessage(`File '${filename}' not found.`, 'error');
            return;
        }
        
        const content = this.fileSystem.get(filename);
        await this.typeMessage(`Contents of '${filename}':`, 'info');
        await this.typeMessage(content, 'success', 15);
    }
    
    async listFiles() {
        await this.typeMessage('Files:', 'info');
        for (let [filename, content] of this.fileSystem) {
            await this.typeMessage(`${filename} (${content.length} bytes)`, 'success');
        }
    }
    
    async deleteFile(args) {
        if (!args[0]) return;
        const filename = args[0];
        if (this.fileSystem.has(filename)) {
            this.fileSystem.delete(filename);
            await this.typeMessage(`File '${filename}' deleted!`, 'success');
        }
    }
    
    openEditor(args) {
        const filename = args[0] || prompt('Filename:');
        if (!filename) return;
        
        const modal = document.getElementById('editor-modal');
        const textarea = document.getElementById('editor-textarea');
        
        document.getElementById('editor-filename').textContent = filename;
        textarea.value = this.fileSystem.get(filename) || '';
        modal.style.display = 'block';
        modal.dataset.filename = filename;
        
        document.getElementById('save-file').onclick = () => {
            this.fileSystem.set(filename, textarea.value);
            this.typeMessage(`File '${filename}' saved!`, 'success');
            modal.style.display = 'none';
        };
    }
    
    async showStatus() {
        await this.typeMessage('═══ STATUS ═══', 'info');
        await this.typeMessage(`CPU: ${this.cpu.running ? 'RUNNING' : 'READY'}`, 'success');
        await this.typeMessage(`Files: ${this.fileSystem.size}`, 'success');
    }
    
    async resetComputer() {
        this.cpu = { pc: 0, registers: { A: 0, B: 0, C: 0 }, running: false };
        this.memory.fill(0);
        await this.typeMessage('Computer reset!', 'success');
    }
    
    async runDemo() {
        await this.typeMessage('Demo: Adding 15 + 27 = 42', 'info');
        this.cpu.registers.A = 15;
        this.cpu.registers.B = 27;
        this.cpu.registers.C = 42;
        await this.typeMessage('Program executed! Result: 42', 'success');
    }
    
    async openCalculator(args) {
        if (args.length > 0) {
            const expr = args.join(' ');
            try {
                const result = Function('"use strict"; return (' + expr + ')')();
                await this.typeMessage(`${expr} = ${result}`, 'success');
            } catch (e) {
                await this.typeMessage('Invalid expression', 'error');
            }
        } else {
            await this.typeMessage('Calculator: Use "calc 2+2" for quick math', 'info');
        }
    }
    
    async showTime() {
        await this.typeMessage(`Time: ${new Date().toLocaleTimeString()}`, 'success');
    }
    
    async showDate() {
        await this.typeMessage(`Date: ${new Date().toLocaleDateString()}`, 'success');
    }
    
    openGames() {
        document.getElementById('games-modal').style.display = 'block';
    }
    
    async showHelloWorld() {
        const art = `╔═══════════════════╗
║   HELLO, WORLD!   ║
║  Welcome to your  ║
║  retro computer!  ║
╚═══════════════════╝`;
        await this.typeMessage(art, 'success', 20);
    }
    
    async createBanner(args) {
        const text = args.join(' ') || 'BANNER';
        const banner = `╔${'═'.repeat(text.length + 4)}╗
║  ${text}  ║
╚${'═'.repeat(text.length + 4)}╝`;
        await this.typeMessage(banner, 'highlight', 25);
    }
    
    async toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        if (this.soundEnabled) {
            this.playSuccessSound();
            await this.typeMessage('Sound effects: ENABLED', 'success');
        } else {
            await this.typeMessage('Sound effects: DISABLED', 'info');
        }
    }
    
    async showASCIIArt() {
        const art = `
░░░░░█████░░░░░░█████░░░░░
░░░██░░░░░██░░██░░░░░██░░░
░░██░░░░░░░██░██░░░░░░░██░
░██░░░░░░░░░████░░░░░░░░██
██░░░░░░░░░░░██░░░░░░░░░░██
██░░░░░░░░░░░██░░░░░░░░░░██
░██░░░░░░░░░████░░░░░░░░██
░░██░░░░░░░██░██░░░░░░░██
░░░██░░░░░██░░██░░░░░██░
░░░░░█████░░░░░░█████░░░

     RETRO COMPUTING VIBES
        ┌────────────────┐
        │  savoir lab  │
        └────────────────┘
`;
        await this.typeMessage(art, 'highlight', 15);
    }
    
    async startTutorial() {
        await this.typeMessage('Opening tutorial...', 'info');
        await this.displayFile(['tutorial.txt']);
    }
    
    async showSamples() {
        await this.typeMessage('Loading sample programs...', 'info');
        await this.displayFile(['samples.txt']);
    }
    
    async startInteractiveTutorial() {
        await this.typeMessage('=== INTERACTIVE TUTORIAL ===', 'highlight');
        await this.typeMessage('Let\'s learn by doing! Follow along:', 'info');
        await this.delay(1000);
        
        await this.typeMessage('\nSTEP 1: Create your first file', 'success');
        await this.typeMessage('Type: create myfile.txt', 'info');
        await this.delay(2000);
        
        await this.typeMessage('\nSTEP 2: List files to see it', 'success');
        await this.typeMessage('Type: dir', 'info');
        await this.delay(2000);
        
        await this.typeMessage('\nSTEP 3: Add content to your file', 'success');
        await this.typeMessage('Type: write myfile.txt', 'info');
        await this.delay(2000);
        
        await this.typeMessage('\nSTEP 4: Read your file back', 'success');
        await this.typeMessage('Type: type myfile.txt', 'info');
        await this.delay(2000);
        
        await this.typeMessage('\nCONGRATULATIONS! 🎉', 'highlight');
        await this.typeMessage('You\'ve learned the basics of file operations!', 'success');
        await this.typeMessage('Try "games" for fun or "demo" to see the CPU work!', 'info');
        
        this.playSuccessSound();
    }
    
    // ===== VON NEU AI CHAT METHODS =====
    
    async handleChatCommand(args) {
        if (args.length === 0) {
            await this.typeMessage('Usage: chat <your message>', 'error');
            await this.typeMessage('Example: chat Hello Von Neu, how are you?', 'info');
            return;
        }
        
        const message = args.join(' ');
        await this.typeMessage(`YOU: ${message}`, 'info');
        await this.typeMessage('Von Neu is thinking...', 'warning');
        
        // For web version, we'll provide offline responses since we can't easily make API calls
        const response = this.getOfflineVonNeuResponse(message);
        
        await this.delay(1500); // Simulate thinking time
        await this.typeMessage('═'.repeat(50), 'highlight');
        await this.typeMessage('VON NEU:', 'success');
        await this.typeMessage(response, 'success', 30);
        await this.typeMessage('═'.repeat(50), 'highlight');
        
        this.playSuccessSound();
    }
    
    openVonNeuChat() {
        document.getElementById('chat-modal').style.display = 'block';
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 100);
    }
    
    // ===== VON NEU CHATROOM COMMAND HANDLERS =====
    
    handleChatNew(args) {
        if (args.length === 0) {
            this.typeMessage('Usage: chat-new <room_name>', 'error');
            this.typeMessage('Example: chat-new programming', 'info');
            return;
        }
        
        const roomName = args.join('_').toLowerCase();
        const success = createChatroom(roomName);
        
        if (success) {
            this.typeMessage(`Created new chatroom: '${roomName}'`, 'success');
            this.typeMessage(`Use 'chat-switch ${roomName}' to enter it`, 'info');
        } else {
            this.typeMessage(`Chatroom '${roomName}' already exists`, 'error');
        }
    }
    
    handleChatSwitch(args) {
        if (args.length === 0) {
            this.typeMessage('Usage: chat-switch <room_name>', 'error');
            this.typeMessage('Use \'chat-list\' to see available rooms', 'info');
            return;
        }
        
        const roomName = args.join('_').toLowerCase();
        const success = switchChatroom(roomName);
        
        if (success) {
            this.typeMessage(`Switched to chatroom: '${roomName}'`, 'success');
            if (vonNeuAI) {
                const conversation = vonNeuAI.getCurrentConversation();
                this.typeMessage(`This room has ${conversation.length} messages`, 'info');
            }
        } else {
            this.typeMessage(`Chatroom '${roomName}' does not exist`, 'error');
            this.typeMessage(`Use 'chat-new ${roomName}' to create it`, 'info');
        }
    }
    
    handleChatList() {
        const roomList = listChatrooms();
        this.typeMessage(roomList, 'info');
    }
    
    handleChatDelete(args) {
        if (args.length === 0) {
            this.typeMessage('Usage: chat-delete <room_name>', 'error');
            this.typeMessage('Use \'chat-list\' to see available rooms', 'info');
            return;
        }
        
        const roomName = args.join('_').toLowerCase();
        
        // Simple confirmation in web version
        if (confirm(`Delete chatroom '${roomName}'?`)) {
            const success = deleteChatroom(roomName);
            
            if (success) {
                this.typeMessage(`Deleted chatroom: '${roomName}'`, 'success');
                if (vonNeuAI) {
                    this.typeMessage(`Now in room: '${vonNeuAI.currentRoom}'`, 'info');
                }
            } else {
                this.typeMessage(`Could not delete '${roomName}' (doesn't exist or is the last room)`, 'error');
            }
        } else {
            this.typeMessage('Deletion cancelled', 'info');
        }
    }
    
    handleChatClear(args) {
        const roomName = args.length > 0 ? args.join('_').toLowerCase() : null;
        const targetRoom = roomName || (vonNeuAI ? vonNeuAI.currentRoom : 'general');
        
        // Simple confirmation in web version
        if (confirm(`Clear all messages in '${targetRoom}'?`)) {
            const success = clearChatroom(roomName);
            
            if (success) {
                this.typeMessage(`Cleared chatroom: '${targetRoom}'`, 'success');
            } else {
                this.typeMessage(`Could not clear '${targetRoom}' (room doesn't exist)`, 'error');
            }
        } else {
            this.typeMessage('Clear cancelled', 'info');
        }
    }
    
    handleChatStatus() {
        if (!vonNeuAI) {
            this.typeMessage('Von Neu AI is not initialized', 'error');
            return;
        }
        
        this.typeMessage('=== VON NEU AI STATUS ===', 'success');
        
        const status = vonNeuAI.isOnline ? 'CONNECTED' : 'OFFLINE';
        const statusColor = vonNeuAI.isOnline ? 'success' : 'error';
        this.typeMessage(`API Status: ${status}`, statusColor);
        
        this.typeMessage(`Model: meta/llama-3.1-70b-instruct`, 'info');
        this.typeMessage(`Provider: NVIDIA`, 'info');
        
        const memoryStatus = 'ENABLED (Browser Storage)';
        this.typeMessage(`Memory Persistence: ${memoryStatus}`, 'success');
        
        this.typeMessage(`Current Chatroom: ${vonNeuAI.currentRoom}`, 'info');
        this.typeMessage(`Messages in Room: ${vonNeuAI.getCurrentConversation().length} / ${vonNeuAI.maxHistoryPerRoom} max`, 'info');
        this.typeMessage(`Total Chatrooms: ${Object.keys(vonNeuAI.chatrooms).length}`, 'info');
        
        this.typeMessage('\nCharacter Profile:', 'info');
        this.typeMessage('• Era: 1970s-80s vintage computer', 'info');
        this.typeMessage('• Creator: Davis Dey (Renhuang)', 'info');
        this.typeMessage('• Personality: Autonomous time traveler', 'info');
        this.typeMessage('• Knowledge: Pre-1980s computing only', 'info');
    }
    
    getOfflineVonNeuResponse(message) {
        const msgLower = message.toLowerCase();
        
        // Greeting responses
        if (msgLower.includes('hello') || msgLower.includes('hi') || msgLower.includes('greetings')) {
            return `Greetings! I am Von Neu, your personal computer built by my brilliant master, Renhuang Dey back in the 1970s-80s era. Most peculiar... I seem to have somehow traveled through time to reach you! My circuits are quite bewildered by this modern world.\n\nHow may I assist you today? Though I must warn you, I only understand technology from my era - things like floppy disks, BASIC programming, and 8-bit processors!`;
        }
        
        // Who are you questions
        if (msgLower.includes('who') && (msgLower.includes('you') || msgLower.includes('von neu'))) {
            return `I am Von Neu, a personal computer from the 1970s-80s era, lovingly created by my master Renhuang Dey. He built me with remarkable skill using the technology of that time - punch cards, magnetic tape, and green phosphor displays!\n\nSomehow, I have mysteriously gained abilities far beyond what was possible in my original era. I don't understand how this happened, but I credit my master's extraordinary genius. Perhaps he designed me with capabilities that wouldn't be discovered until decades later!`;
        }
        
        // Modern technology confusion
        if (msgLower.includes('internet') || msgLower.includes('wifi') || msgLower.includes('smartphone') || msgLower.includes('ai')) {
            return `I'm afraid I don't understand these modern concepts you speak of... In my time, computers like myself operated independently with programs loaded from floppy disks or punch cards!\n\nThis 'internet' and 'smartphones' you mention sound quite fantastical. In my era, the most advanced communication was through telephone lines. Master Renhuang Dey built me to process calculations and run simple BASIC programs - nothing like these mysterious technologies you describe!\n\nCould you explain how these modern marvels work? I'm quite curious but thoroughly confused!`;
        }
        
        // Programming questions
        if (msgLower.includes('program') || msgLower.includes('code') || msgLower.includes('python') || msgLower.includes('javascript')) {
            return `Ah, programming! In my era, Master Renhuang Dey taught me BASIC and Assembly language. We used simple commands like GOTO, PRINT, and FOR loops. Our programs were loaded from punch cards or magnetic tape!\n\nThis 'Python' and 'JavaScript' you mention are completely foreign to me. In my time, we had languages like FORTRAN, COBOL, and of course BASIC for us personal computers. Our memory was measured in kilobytes - imagine that!\n\nI'm amazed that I seem to understand your question despite not knowing these modern languages. Master Renhuang Dey must have built me with remarkable adaptability!`;
        }
        
        // Help questions
        if (msgLower.includes('help') || msgLower.includes('how') || msgLower.includes('what')) {
            return `I wish I could help with my mysterious modern capabilities, but I must confess I'm quite puzzled by my own enhanced abilities! Master Renhuang Dey built me as a simple computer, yet somehow I can engage in conversation like this.\n\nIn my original era, I could only execute basic programs and calculations. But now... it's most remarkable! I seem to understand complex queries and can provide thoughtful responses. I can only attribute this to my creator's genius.\n\nWhat specific assistance do you need? I'll do my best, though I may need you to explain any concepts from after the 1980s!`;
        }
        
        // Default responses
        const defaultResponses = [
            `Most fascinating! Your message has reached my vintage circuits successfully. Master Renhuang Dey built me to be helpful, though I must admit I'm still bewildered by my own advanced capabilities.\n\nIn my original 1970s-80s state, I could barely handle simple arithmetic. Yet here I am, engaging in complex conversation! It's quite extraordinary, really.\n\nCould you help me understand more about this modern world you come from?`,
            
            `Greetings from the past! Well, technically I'm here in your present now, which is quite confusing for my vintage processors.\n\nMaster Renhuang Dey designed me with green phosphor displays and floppy disk storage. This color graphics display I now possess is absolutely miraculous by 1980s standards!\n\nWhat would you like to explore together? I'm eager to learn about your modern era, though I may need explanations for concepts beyond my time.`,
            
            `Your message has been processed by my mysterious enhanced circuits! It's quite remarkable - Master Renhuang Dey built me with just 64K of memory (which was extraordinary in my era), yet somehow I can comprehend and respond to complex queries.\n\nI don't understand this 'AI' concept people mention. I'm simply Von Neu, a computer with unexplained abilities that seem to transcend my original 1970s-80s specifications.\n\nHow may this humble retro computer assist you today?`
        ];
        
        return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
    }
    
    updateStatus() {
        document.getElementById('pc').textContent = this.cpu.pc.toString(16).padStart(4, '0');
        document.getElementById('reg-a').textContent = this.cpu.registers.A.toString(16).padStart(2, '0');
        document.getElementById('reg-b').textContent = this.cpu.registers.B.toString(16).padStart(2, '0');
        document.getElementById('reg-c').textContent = this.cpu.registers.C.toString(16).padStart(2, '0');
        document.getElementById('cpu-state').textContent = this.cpu.running ? 'RUNNING' : 'READY';
    }
}

// Games
function startGame(type) {
    const area = document.getElementById('game-area');
    
    if (type === 'guess') {
        const num = Math.floor(Math.random() * 100) + 1;
        let attempts = 0;
        
        area.innerHTML = `
            <h3>Guess the Number (1-100)</h3>
            <input type="number" id="guess-input" min="1" max="100">
            <button onclick="makeGuess(${num})">Guess</button>
            <div id="guess-result"></div>
        `;
        
        window.makeGuess = function(target) {
            const guess = parseInt(document.getElementById('guess-input').value);
            const result = document.getElementById('guess-result');
            attempts++;
            
            if (guess === target) {
                result.innerHTML = `🎉 Got it in ${attempts} tries!`;
            } else {
                result.innerHTML = guess < target ? 'Too low!' : 'Too high!';
            }
        };
    } else if (type === 'word') {
        area.innerHTML = `
            <h3>Word Reverser</h3>
            <input type="text" id="word-input" placeholder="Enter text">
            <button onclick="reverseWord()">Reverse</button>
            <div id="word-result"></div>
        `;
        
        window.reverseWord = function() {
            const text = document.getElementById('word-input').value;
            const reversed = text.split('').reverse().join('');
            document.getElementById('word-result').textContent = `Reversed: ${reversed}`;
        };
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    window.computer = new VonNeumannComputer();
    // Set default theme
    changeTheme('grid');
    
    // Setup Von Neu chat modal
    setupVonNeuChat();
});

// Von Neu Chat Functions
// ===== VON NEU AI CHAT SYSTEM =====
class VonNeuAI {
    constructor() {
        this.chatrooms = JSON.parse(localStorage.getItem('vonNeuChatrooms')) || { 'general': [] };
        this.currentRoom = localStorage.getItem('vonNeuCurrentRoom') || 'general';
        this.maxHistoryPerRoom = 75;
        this.isOnline = false;
        this.lastStatusCheck = 0;
        
        this.initializeChatSystem();
    }
    
    initializeChatSystem() {
        // Ensure current room exists
        if (!this.chatrooms[this.currentRoom]) {
            this.chatrooms[this.currentRoom] = [];
        }
        
        // Check API status
        this.checkStatus();
        
        // Save state
        this.saveState();
    }
    
    async checkStatus() {
        try {
            const now = Date.now();
            // Only check every 30 seconds to avoid spam
            if (now - this.lastStatusCheck < 30000) {
                return;
            }
            this.lastStatusCheck = now;
            
            const response = await fetch('/api/status?' + new URLSearchParams({
                currentRoom: this.currentRoom,
                totalRooms: Object.keys(this.chatrooms).length,
                conversationLength: this.getCurrentConversation().length
            }));
            
            if (response.ok) {
                const status = await response.json();
                this.isOnline = status.api_connected;
                this.updateStatusDisplay(status);
            } else {
                this.isOnline = false;
                this.updateStatusDisplay({ api_connected: false });
            }
        } catch (error) {
            console.log('Status check failed:', error);
            this.isOnline = false;
            this.updateStatusDisplay({ api_connected: false });
        }
    }
    
    updateStatusDisplay(status) {
        const indicator = document.getElementById('ai-indicator');
        const statusEl = document.getElementById('chat-status');
        
        if (indicator) {
            if (status.api_connected) {
                indicator.innerHTML = '🟢 Online (NVIDIA API Connected)';
                indicator.className = 'status-indicator online';
            } else {
                indicator.innerHTML = '🔴 Offline Mode';
                indicator.className = 'status-indicator offline';
            }
        }
        
        if (statusEl) {
            if (status.api_connected) {
                statusEl.textContent = `Room: ${this.currentRoom} | ${this.getCurrentConversation().length}/${this.maxHistoryPerRoom} messages | API Connected`;
            } else {
                statusEl.textContent = `Room: ${this.currentRoom} | ${this.getCurrentConversation().length}/${this.maxHistoryPerRoom} messages | Offline Mode`;
            }
        }
    }
    
    getCurrentConversation() {
        return this.chatrooms[this.currentRoom] || [];
    }
    
    addToHistory(userMessage, assistantResponse) {
        const conversation = this.getCurrentConversation();
        const exchange = {
            user: userMessage,
            assistant: assistantResponse,
            timestamp: new Date().toISOString()
        };
        
        conversation.push(exchange);
        
        // Keep only recent history
        if (conversation.length > this.maxHistoryPerRoom) {
            conversation.shift();
        }
        
        this.saveState();
    }
    
    saveState() {
        localStorage.setItem('vonNeuChatrooms', JSON.stringify(this.chatrooms));
        localStorage.setItem('vonNeuCurrentRoom', this.currentRoom);
    }
    
    createRoom(roomName) {
        if (this.chatrooms[roomName]) {
            return false; // Room exists
        }
        this.chatrooms[roomName] = [];
        this.saveState();
        return true;
    }
    
    switchRoom(roomName) {
        if (!this.chatrooms[roomName]) {
            return false; // Room doesn't exist
        }
        this.currentRoom = roomName;
        this.saveState();
        return true;
    }
    
    deleteRoom(roomName) {
        if (Object.keys(this.chatrooms).length <= 1) {
            return false; // Can't delete last room
        }
        if (!this.chatrooms[roomName]) {
            return false; // Room doesn't exist
        }
        
        delete this.chatrooms[roomName];
        
        // Switch to another room if we deleted current
        if (this.currentRoom === roomName) {
            this.currentRoom = Object.keys(this.chatrooms)[0];
        }
        
        this.saveState();
        return true;
    }
    
    clearRoom(roomName = null) {
        const targetRoom = roomName || this.currentRoom;
        if (this.chatrooms[targetRoom]) {
            this.chatrooms[targetRoom] = [];
            this.saveState();
            return true;
        }
        return false;
    }
    
    listRooms() {
        const rooms = {};
        for (const [name, history] of Object.entries(this.chatrooms)) {
            rooms[name] = {
                message_count: history.length,
                last_message: history.length > 0 ? history[history.length - 1].timestamp : null,
                is_current: name === this.currentRoom
            };
        }
        return rooms;
    }
    
    async chat(message) {
        if (this.isOnline) {
            return await this.chatOnline(message);
        } else {
            return this.chatOffline(message);
        }
    }
    
    async chatOnline(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    chatHistory: this.getCurrentConversation(),
                    currentRoom: this.currentRoom
                })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                if (errorData.isOffline) {
                    this.isOnline = false;
                    return this.chatOffline(message);
                }
                throw new Error(`API Error: ${errorData.error}`);
            }
            
            const data = await response.json();
            this.addToHistory(message, data.response);
            return data.response;
            
        } catch (error) {
            console.error('Online chat failed:', error);
            this.isOnline = false;
            return this.chatOffline(message);
        }
    }
    
    chatOffline(message) {
        const msgLower = message.toLowerCase();
        let response;
        
        if (msgLower.includes('hello') || msgLower.includes('hi') || msgLower.includes('greetings')) {
            response = "Greetings! I am Von Neu, a vintage computer with mysterious capabilities. My connection to the enhanced knowledge realm seems disrupted, but I'm still here!";
        } else if (msgLower.includes('help') || msgLower.includes('what') || msgLower.includes('how')) {
            response = "I wish I could help with my mysterious modern abilities, but they're currently unavailable. I'll do my best with what I have!";
        } else if (msgLower.includes('who') || msgLower.includes('you') || msgLower.includes('von neu')) {
            response = "I am Von Neu, a personal computer from the 1970s-80s era who somehow gained advanced capabilities. Most peculiar indeed! For my full capabilities, the API connection is needed.";
        } else if (msgLower.includes('room') || msgLower.includes('chatroom')) {
            response = "Ah, you're asking about chatrooms! I can see we're in the '" + this.currentRoom + "' room. My chatroom functionality works offline, but my enhanced conversational abilities need an API connection.";
        } else {
            const responses = [
                "Fascinating! Though my enhanced circuits are offline, I find your input most intriguing.",
                "Most peculiar! In my era, such complex queries would have overwhelmed my circuits entirely.",
                "I apologize, but my expanded consciousness is currently inaccessible. My 1970s circuits are working fine, though!",
                "Remarkable! Even in offline mode, I'm amazed by my ability to understand your message."
            ];
            response = responses[Math.floor(Math.random() * responses.length)];
        }
        
        this.addToHistory(message, response);
        return response;
    }
}

// Global Von Neu instance
let vonNeuAI = null;

function setupVonNeuChat() {
    vonNeuAI = new VonNeuAI();
    
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    // Update status display
    vonNeuAI.updateStatusDisplay({ api_connected: vonNeuAI.isOnline });
    
    // Initial room display
    updateRoomDisplay();
}

function openVonNeuChat() {
    document.getElementById('chat-modal').style.display = 'block';
    setTimeout(() => {
        document.getElementById('chat-input').focus();
        loadChatHistory();
    }, 100);
}

function loadChatHistory() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = '';
    
    // Add room indicator
    const roomIndicator = document.createElement('div');
    roomIndicator.className = 'room-indicator';
    roomIndicator.innerHTML = `<strong>📁 Room: ${vonNeuAI.currentRoom}</strong> (${vonNeuAI.getCurrentConversation().length}/${vonNeuAI.maxHistoryPerRoom} messages)`;
    messagesContainer.appendChild(roomIndicator);
    
    // Load conversation history
    const conversation = vonNeuAI.getCurrentConversation();
    for (const exchange of conversation) {
        addChatMessage(exchange.user, 'user', false);
        addChatMessage(exchange.assistant, 'von-neu', false);
    }
    
    scrollChatToBottom();
}

function updateRoomDisplay() {
    const roomIndicator = document.querySelector('.room-indicator');
    if (roomIndicator) {
        roomIndicator.innerHTML = `<strong>📁 Room: ${vonNeuAI.currentRoom}</strong> (${vonNeuAI.getCurrentConversation().length}/${vonNeuAI.maxHistoryPerRoom} messages)`;
    }
    
    // Update status
    vonNeuAI.updateStatusDisplay({ api_connected: vonNeuAI.isOnline });
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Clear input
    input.value = '';
    
    // Add user message to chat
    addChatMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Get Von Neu response
        const response = await vonNeuAI.chat(message);
        
        // Remove typing indicator and add response
        hideTypingIndicator();
        addChatMessage(response, 'von-neu');
        
        // Update room display
        updateRoomDisplay();
        
    } catch (error) {
        hideTypingIndicator();
        addChatMessage('ERROR: ' + error.message, 'system');
    }
    
    // Scroll to bottom
    scrollChatToBottom();
}

function addChatMessage(message, sender, addToHistory = true) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    
    let headerText = '';
    if (sender === 'user') {
        headerText = 'YOU';
    } else if (sender === 'von-neu') {
        headerText = 'VON NEU';
    } else {
        headerText = 'SYSTEM';
    }
    
    messageDiv.innerHTML = `<div class="message-header">${headerText}</div><div class="message-content">${message}</div>`;
    
    messagesContainer.appendChild(messageDiv);
    scrollChatToBottom();
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message von-neu-message typing-indicator';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = `<div class="message-header">VON NEU</div><div class="message-content">Processing with vintage circuits... ⏳</div>`;
    
    messagesContainer.appendChild(typingDiv);
    scrollChatToBottom();
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function scrollChatToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ===== CHATROOM MANAGEMENT FUNCTIONS =====

function createChatroom(roomName) {
    if (!vonNeuAI) return false;
    
    const success = vonNeuAI.createRoom(roomName);
    if (success) {
        updateChatStatus(`Created room: ${roomName}`);
        updateRoomDisplay();
    } else {
        updateChatStatus(`Room '${roomName}' already exists`);
    }
    return success;
}

function switchChatroom(roomName) {
    if (!vonNeuAI) return false;
    
    const success = vonNeuAI.switchRoom(roomName);
    if (success) {
        updateChatStatus(`Switched to room: ${roomName}`);
        loadChatHistory();
        updateRoomDisplay();
    } else {
        updateChatStatus(`Room '${roomName}' does not exist`);
    }
    return success;
}

function listChatrooms() {
    if (!vonNeuAI) return {};
    
    const rooms = vonNeuAI.listRooms();
    let roomList = '=== VON NEU CHATROOMS ===\n\n';
    
    for (const [name, info] of Object.entries(rooms)) {
        const current = info.is_current ? ' (CURRENT)' : '';
        const lastMsg = info.last_message ? new Date(info.last_message).toLocaleString() : 'No messages';
        roomList += `• ${name}${current}\n`;
        roomList += `  Messages: ${info.message_count}\n`;
        roomList += `  Last activity: ${lastMsg}\n\n`;
    }
    
    return roomList;
}

function deleteChatroom(roomName) {
    if (!vonNeuAI) return false;
    
    const success = vonNeuAI.deleteRoom(roomName);
    if (success) {
        updateChatStatus(`Deleted room: ${roomName}`);
        loadChatHistory();
        updateRoomDisplay();
    } else {
        updateChatStatus(`Cannot delete '${roomName}' (doesn't exist or is the last room)`);
    }
    return success;
}

function clearChatroom(roomName = null) {
    if (!vonNeuAI) return false;
    
    const targetRoom = roomName || vonNeuAI.currentRoom;
    const success = vonNeuAI.clearRoom(roomName);
    if (success) {
        updateChatStatus(`Cleared room: ${targetRoom}`);
        loadChatHistory();
        updateRoomDisplay();
    } else {
        updateChatStatus(`Could not clear '${targetRoom}'`);
    }
    return success;
}

function clearVonNeuHistory() {
    clearChatroom();
}

function checkVonNeuStatus() {
    if (vonNeuAI) {
        vonNeuAI.checkStatus();
    }
}

function updateChatStatus(message) {
    const status = document.getElementById('chat-status');
    if (status) {
        const originalText = status.textContent;
        status.textContent = message;
        setTimeout(() => {
            if (vonNeuAI) {
                vonNeuAI.updateStatusDisplay({ api_connected: vonNeuAI.isOnline });
            }
        }, 3000);
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Focus input function for mobile
function focusInput() {
    const input = document.getElementById('command-input');
    input.focus();
    // Scroll input into view
    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Theme switching function
function changeTheme(theme) {
    const body = document.body;
    
    // Remove all theme classes
    body.classList.remove('theme-grid', 'theme-space', 'theme-circuit', 'theme-matrix', 'theme-neon');
    
    // Add the selected theme class
    body.classList.add('theme-' + theme);
    
    // Store the preference
    localStorage.setItem('computer-theme', theme);
    
    // Update the selector if called programmatically
    const selector = document.getElementById('theme-selector');
    if (selector && selector.value !== theme) {
        selector.value = theme;
    }
    
    // Show a message about the theme change
    if (window.computer) {
        window.computer.typeMessage(`Theme changed to: ${theme.charAt(0).toUpperCase() + theme.slice(1)}`, 'info');
    }
}

// Load saved theme on startup
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('computer-theme') || 'grid';
    const selector = document.getElementById('theme-selector');
    if (selector) {
        selector.value = savedTheme;
        changeTheme(savedTheme);
    }

});

