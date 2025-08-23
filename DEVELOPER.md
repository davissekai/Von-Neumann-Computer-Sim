# Developer Documentation
## Von Neumann Computer Simulator

*Created by Savoir Lab - towards the peak human.*

---

## 🏗️ **Architecture Overview**

The Von Neumann Computer Simulator is a web-based educational tool that demonstrates the fundamental principles of computer architecture through an interactive retro-styled interface.

### **Core Components**

1. **Memory System** (`VonNeumannComputer.memory`)
   - 256-byte unified memory array
   - Stores both program instructions and data
   - Simulates the stored-program concept

2. **CPU Simulation** (`VonNeumannComputer.cpu`)
   - Program Counter (PC)
   - Registers (A, B, C)
   - Running state management

3. **File System** (`VonNeumannComputer.fileSystem`)
   - JavaScript Map for file storage
   - In-memory file operations
   - Educational file samples

4. **I/O System**
   - Terminal interface for user interaction
   - Command processing engine
   - Audio feedback system

---

## 📁 **File Structure**

```
von_neumann_computer/
├── landing.html          # Landing page
├── landing.css           # Landing page styles
├── computer.html         # Main simulator interface
├── styles.css           # Simulator styles
├── von-neumann.js       # Core JavaScript logic
├── README.md            # Project documentation
├── TESTING.md           # Test documentation
├── vercel.json          # Deployment configuration
├── .gitignore           # Git ignore rules
└── Python files/        # Original Python implementation
    ├── cpu.py
    ├── memory.py
    ├── main_interface.py
    └── ...
```

---

## 🎯 **JavaScript Architecture**

### **Main Class: VonNeumannComputer**

```javascript
class VonNeumannComputer {
    constructor() {
        this.memory = new Array(256).fill(0);
        this.cpu = { pc: 0, registers: { A: 0, B: 0, C: 0 }, running: false };
        this.fileSystem = new Map();
        this.commandHistory = [];
        this.historyIndex = -1;
        this.soundEnabled = true;
    }
}
```

### **Key Methods**

#### **Command Processing**
```javascript
async executeCommand(commandLine)
```
- Parses user input
- Routes to appropriate command handlers
- Provides error handling and feedback

#### **Audio System**
```javascript
playSound(frequency, duration, type)
playBootSound()
playKeyPressSound()
playErrorSound()
playSuccessSound()
```

#### **File Operations**
```javascript
createFile(args)
writeFile(args)
displayFile(args)
deleteFile(args)
listFiles()
```

#### **Educational Features**
```javascript
startTutorial()
showSamples()
startInteractiveTutorial()
```

---

## 🎨 **CSS Architecture**

### **Theme System**
The simulator supports 5 themes with CSS classes:
- `.theme-grid` - Classic 80s Grid
- `.theme-space` - Space Stars
- `.theme-circuit` - Circuit Board
- `.theme-matrix` - Matrix Rain
- `.theme-neon` - Neon City

### **Responsive Design**
- Mobile-first approach
- Breakpoints: 768px (tablet), 480px (mobile)
- Touch-friendly interface elements
- Virtual keyboard for mobile

### **CSS Variables**
```css
:root {
    --primary-green: #00ff00;
    --dark-bg: #000000;
    --secondary-bg: #333333;
    --text-light: #ffffff;
    --text-gray: #cccccc;
    --text-muted: #888888;
    --border-color: #666666;
}
```

---

## 📱 **Mobile Enhancement Features**

### **Virtual Keyboard**
- Auto-generated for touch devices
- Common commands as buttons
- Touch-friendly 44px minimum size

### **Touch Optimizations**
- Prevents unwanted zooming
- Auto-focus management
- Gesture handling
- Mobile-specific layouts

### **Detection Logic**
```javascript
this.isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
               ('ontouchstart' in window) || 
               (navigator.maxTouchPoints > 0);
```

---

## 🔊 **Audio System**

### **Web Audio API Implementation**
```javascript
initializeSounds() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
}
```

### **Sound Effects**
- **Boot Sound**: Ascending tone sequence
- **Key Press**: Quick 800Hz square wave
- **Success**: Harmonic chord progression
- **Error**: Low-frequency sawtooth wave

---

## 🎮 **Game System**

### **Modular Game Architecture**
Games are implemented as self-contained functions:

```javascript
function startGame(type) {
    const area = document.getElementById('game-area');
    // Game-specific logic
}
```

### **Available Games**
1. **Guess the Number** - Random number generation and comparison
2. **Word Reverser** - String manipulation demonstration
3. **Math Quiz** - Basic arithmetic challenges

---

## 📚 **Educational Content System**

### **File-Based Learning**
Educational content is stored as files in the virtual file system:
- `readme.txt` - Welcome and basic commands
- `tutorial.txt` - Comprehensive learning guide
- `samples.txt` - Example programs and exercises
- `fibonacci.py` - Programming example

### **Interactive Tutorial Flow**
1. Introduction to file creation
2. File listing and navigation
3. Content writing and reading
4. Celebration and next steps

---

## 🔧 **Command System**

### **Command Categories**

#### **File Operations**
- `create <filename>` - Create new file
- `write <filename>` - Add content to file
- `type <filename>` - Display file content
- `dir` / `ls` - List files
- `delete <filename>` - Remove file
- `editor <filename>` - Open text editor

#### **System Commands**
- `help` - Show command list
- `clear` - Clear terminal
- `about` - Show system information
- `status` - Display CPU/system status
- `reset` - Reset computer state

#### **Educational Commands**
- `tutorial` - Open tutorial content
- `samples` - Show sample programs
- `interactive` - Start guided tutorial
- `demo` - Run demonstration program

#### **Entertainment Commands**
- `games` - Open games interface
- `calc <expression>` - Calculator
- `ascii` - Display ASCII art
- `banner <text>` - Create custom banner
- `hello` - Hello World display

#### **Utility Commands**
- `time` - Current time
- `date` - Current date
- `sound` - Toggle audio effects

---

## 🎯 **Deployment Configuration**

### **Vercel Settings** (`vercel.json`)
```json
{
  "version": 2,
  "builds": [
    { "src": "*.html", "use": "@vercel/static" },
    { "src": "*.css", "use": "@vercel/static" },
    { "src": "*.js", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/", "dest": "/landing.html" },
    { "src": "/computer", "dest": "/computer.html" }
  ]
}
```

### **Git Workflow**
1. Initialize repository: `git init`
2. Stage files: `git add .`
3. Commit: `git commit -m "message"`
4. Push to GitHub: `git push origin main`
5. Deploy via Vercel automatic integration

---

## 🔍 **Performance Considerations**

### **Optimization Strategies**
- Lazy loading of audio context
- Efficient DOM manipulation
- CSS hardware acceleration
- Minimal JavaScript bundle size

### **Memory Management**
- Limited file system size
- Command history pruning
- Audio context cleanup
- Event listener management

---

## 🐛 **Debug Features**

### **Console Integration**
```javascript
// Debug mode activation
window.computer.debugMode = true;

// Access internal state
console.log(window.computer.fileSystem);
console.log(window.computer.cpu);
```

### **Development Tools**
- Browser DevTools integration
- Console command testing
- Network monitoring
- Performance profiling

---

## 🔮 **Future Enhancements**

### **Planned Features**
- Assembly language interpreter
- Memory editing interface
- Program execution visualization
- Multi-user collaborative sessions
- Advanced sound synthesis
- VR/AR integration possibilities

### **Technical Debt**
- Unit test implementation
- TypeScript conversion
- Progressive Web App features
- Offline functionality
- Enhanced accessibility

---

## 🤝 **Contributing Guidelines**

### **Code Style**
- Use ES6+ features
- Maintain retro aesthetic
- Follow mobile-first approach
- Preserve educational value

### **Pull Request Process**
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test across devices
5. Submit pull request

### **Issue Reporting**
- Use provided issue templates
- Include browser/device information
- Provide reproduction steps
- Suggest potential solutions

---

## 📄 **License**

MIT License - Educational use encouraged

---

## 📞 **Support**

For technical questions or contributions:
- GitHub Issues
- Savoir Lab Contact
- Community Discussions

---

**Built with ❤️ by Savoir Lab**  
*Advancing human potential through technology*