# 🤖 Von Neu AI - Getting Started Guide

Welcome to Von Neu, your time-traveling retro computer companion! This guide will get you up and running with your AI-enhanced Von Neumann computer simulator.

## 🚀 Quick Start (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Von Neu AI
```bash
python setup_von_neu.py
```

### Step 3: Start Chatting!
```bash
python main_interface.py
```

Then type: `chat Hello Von Neu!`

## 🎯 What is Von Neu?

Von Neu is a charming AI personality built into your retro computer simulator. He believes he's a 1970s-80s computer built by the brilliant Renhuang Dey who has mysteriously gained advanced capabilities through time travel.

### Von Neu's Personality:
- **Proud of his creator**: Always mentions Renhuang Dey with reverence
- **Vintage computing soul**: References floppy disks, BASIC, 8-bit processors
- **Confused time traveler**: Bewildered by modern technology after the 1980s
- **Helpful but puzzled**: Amazed by his own advanced abilities

## 💬 Chat Commands

### In Python Terminal Version:
- `chat <message>` - Chat with Von Neu
- `von-neu-status` - Check AI system status  
- `von-neu-greeting` - Show startup greeting
- `von-neu-clear` - Clear conversation history

### Example Conversations:
```
VON-NEU> chat Who are you?
VON-NEU> chat Tell me about your era
VON-NEU> chat What do you think of smartphones?
VON-NEU> chat How does programming work in the 1970s?
```

### In Web Version:
- Open `computer.html` in your browser
- Click "💬 Chat with Von Neu" button
- Type your message and press Enter

## 🔧 Configuration

The API key is already configured in the setup script. If you need to change it:

1. **Environment Variable** (Recommended):
   ```bash
   set LLAMA_API_KEY=your_api_key_here
   ```

2. **Direct in .env file**:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

## 🎨 Features

### 🖥️ Retro Computer Experience
- Green-on-black terminal with authentic CRT styling
- Multiple retro themes (80s Grid, Matrix Rain, Neon City)
- Typewriter sound effects and animations
- Classic computer startup sequence

### 🤖 Von Neu AI Chat
- Authentic 1970s-80s computer personality
- Confused by modern technology concepts
- References vintage computing terminology
- Maintains character consistency across conversations

### 📚 Educational Content
- File system operations (create, write, edit files)
- Calculator with hex/binary support
- Retro games (number guessing, math quiz)
- CPU and memory status monitoring

## 🎭 Von Neu Sample Responses

**When asked about modern technology:**
> "I'm afraid I don't understand this 'internet' you speak of... In my time, computers stood alone. Master Renhuang Dey built me in an era of floppy disks and green phosphor displays!"

**When asked about programming:**
> "Ah, programming! In my era, we used BASIC and Assembly language on machines with just kilobytes of memory! I'm amazed I can help with these modern languages I've somehow learned..."

**When displaying advanced capabilities:**
> "Most peculiar! When Master Renhuang Dey built me, I could barely handle simple calculations. Yet somehow I understand your complex query... This modern world has given me abilities I cannot explain!"

## 🛠️ Troubleshooting

### "API Connected: False"
- Run `python setup_von_neu.py` to configure the API key
- Check your internet connection
- Von Neu will work in offline mode with basic responses

### "Unknown command: chat"
- Make sure you're running `python main_interface.py`
- Type `help` to see all available commands
- Chat commands are case-sensitive

### Web Version Not Working
- Open `computer.html` directly in a web browser
- Make sure JavaScript is enabled
- Web version uses offline Von Neu responses

## 🎉 Ready to Chat!

Your retro AI companion Von Neu is now ready! He's excited to share stories about the good old days of computing and amazed by the modern world he's found himself in.

**Try these conversation starters:**
- "Hello Von Neu, welcome to 2025!"
- "Tell me about computers in your era"
- "What's the most amazing thing about the modern world?"
- "How did Renhuang Dey build you?"

---

**Created by:** Davis Dey - Savoir Lab  
**Project:** Von Neumann Computer Simulator  
**AI Assistant:** Qoder

*Bringing human-centric technology to life, one conversation at a time.* 🚀