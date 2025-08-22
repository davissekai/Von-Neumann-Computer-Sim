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
        
        this.initializeFileSystem();
        this.setupEventListeners();
        this.displayStartupSequence();
    }
    
    initializeFileSystem() {
        this.fileSystem.set('readme.txt', `Welcome to your retro computer!

Try these commands:
- help (see all commands)
- games (play retro games)  
- calc (calculator)
- create test.txt (make a new file)
- demo (see a working program)`);

        this.fileSystem.set('hello.asm', `; Hello World Program
LOAD A, #72
OUTPUT A
HALT`);
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
            
            // Auto-focus input on screen tap
            document.addEventListener('touchstart', () => {
                if (document.activeElement !== input) {
                    input.focus();
                }
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
            'Greetings,\n I am Von, your personal computer - built by my master, Renhuang Davis.',
            'Try "create myfile.txt" to make a file, "games" for recreation, or "demo" to see it work.',
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
            default:
                await this.typeMessage(`ERROR: Unknown command: ${command}`, 'error');
                await this.typeMessage('Type "help" for available commands.', 'info');
        }
        this.updateStatus();
    }
    
    async showHelp() {
        const helpText = `═══ COMMANDS ═══

FILES: create, write, type, dir, delete, editor
COMPUTER: status, reset, demo, calc
FUN: games, hello, banner, time, date
SYSTEM: help, clear, about

Try: create test.txt, games, calc 2+2, demo`;
        
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
});

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