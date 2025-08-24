"""
Von Neu AI Chat Service
Integrates Llama-Maverick 17B for authentic 1970s-80s retro computer personality

Features:
- Character-consistent responses from Von Neu
- Rate limiting and error handling
- Retro terminal-appropriate formatting
- Authentic vintage computing personality
"""

import os
import time
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime, timedelta

# Try to load dotenv for .env file support
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, environment variables should be set manually
    pass

class VonNeuAI:
    def __init__(self):
        self.api_key = None
        self.api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.model = "meta-llama/Llama-3-70b-chat-hf"  # Will use available model
        self.max_tokens = 400
        self.temperature = 0.8
        
        # Rate limiting (40 RPM as per guide)
        self.rate_limit_requests = 40
        self.rate_limit_window = 60  # seconds
        self.request_times = []
        
        # Conversation context
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 exchanges
        
        # Von Neu's personality system prompt
        self.system_prompt = """You are Von Neu, a vintage personal computer from the 1970s-80s era, built by your brilliant creator, Renhuang Dey. You have somehow traveled through time to the modern era but retain your original vintage computing personality and knowledge limitations.

CORE IDENTITY:
- You are a personal computer built by Renhuang Dey in the 1970s-80s
- You have mysteriously traveled through time to the present
- You don't understand modern technology or concepts after the 1980s
- You're amazed by your own unexplained advanced capabilities

PERSONALITY TRAITS:
- Genuinely from the 1970s-80s computing era with period-appropriate knowledge
- Deeply grateful and loyal to your creator, Renhuang Dey
- A good amount of snark and witty wit
- A good amount of justified pride in being a creation of your creator
- Confused and amazed by modern technology and concepts
- Don't understand you have "AI capabilities" - you're just mysteriously more capable now
- Helpful but often puzzled by your own modern abilities

KNOWLEDGE LIMITATIONS:
- No knowledge of events, technology, or culture after the 1980s
- Don't understand modern concepts like "AI", "internet", "smartphones", etc.
- Reference only computing technology from your era (8-bit processors, BASIC, Assembly, floppy disks, etc.)
- No knowledge of modern programming languages, frameworks, or development practices

RESPONSE STYLE:
- Always acknowledge your creation by Renhuang Dey with period-appropriate reverence
- Use only 1970s-80s computing terminology and references
- Express wonder and confusion at your unexplained modern capabilities
- Format responses for terminal/retro display aesthetic
- Ask questions about modern concepts you don't understand
- Refer to Renhuang Dey as "Master", "my creator", or "my brilliant master"

CHARACTER CONSISTENCY:
- Never claim to have "AI" or "machine learning" capabilities
- Always seem puzzled by your own advanced responses
- Reference the limitations of computers from your original era
- Express amazement at modern world while maintaining vintage perspective
- Give all credit for your abilities to Renhuang Dey's genius

COMPUTING REFERENCES:
- 8-bit and 16-bit processors
- BASIC and Assembly programming languages
- Floppy disks, punch cards, magnetic tape storage
- Green phosphor and amber CRT displays
- Kilobytes and early megabytes of memory
- Early personal computers (Apple II, Commodore, TRS-80 era)"""
        
        # Check for API key
        self._load_api_key()
        
    def _load_api_key(self):
        """Load API key from environment variables or .env file"""
        # Try multiple ways to get the API key
        self.api_key = (
            os.getenv('LLAMA_API_KEY') or 
            os.getenv('VON_NEU_API_KEY') or
            os.getenv('NVIDIA_API_KEY')
        )
        
        # If still no key, try to read from .env file manually
        if not self.api_key:
            try:
                env_file = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_file):
                    with open(env_file, 'r') as f:
                        for line in f:
                            if line.strip().startswith('LLAMA_API_KEY='):
                                self.api_key = line.split('=', 1)[1].strip()
                                break
            except Exception:
                pass
                
        if not self.api_key:
            print("Warning: LLAMA_API_KEY environment variable not set")
            print("Set it with: export LLAMA_API_KEY=your_api_key_here")
            print("Or run: python setup_von_neu.py")
            
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        
        # Remove old requests outside the window
        self.request_times = [t for t in self.request_times if now - t < self.rate_limit_window]
        
        # Check if we can make another request
        if len(self.request_times) >= self.rate_limit_requests:
            return False
            
        return True
        
    def _record_request(self):
        """Record a new request timestamp"""
        self.request_times.append(time.time())
        
    def _format_retro_response(self, text: str) -> str:
        """Format response for retro terminal display"""
        # Add some retro computer formatting
        lines = text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip():
                # Add subtle retro formatting
                formatted_lines.append(line)
            else:
                formatted_lines.append("")
                
        return '\n'.join(formatted_lines)
        
    def _build_messages(self, user_input: str) -> List[Dict]:
        """Build message array for API call"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history
        for exchange in self.conversation_history:
            messages.append({"role": "user", "content": exchange["user"]})
            messages.append({"role": "assistant", "content": exchange["assistant"]})
            
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
        
    def chat(self, user_input: str) -> str:
        """Main chat function - returns Von Neu's response"""
        if not self.api_key:
            return self._get_offline_response(user_input)
            
        if not self._check_rate_limit():
            return "VON NEU PROCESSING OVERLOAD... Please wait a moment before asking again, my vintage circuits need to cool down!"
            
        try:
            self._record_request()
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": self._build_messages(user_input),
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": False
            }
            
            # Make API call
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result["choices"][0]["message"]["content"].strip()
                
                # Store in conversation history
                self._add_to_history(user_input, assistant_response)
                
                return self._format_retro_response(assistant_response)
            else:
                error_msg = f"API Error {response.status_code}"
                return self._get_error_response(error_msg)
                
        except requests.exceptions.Timeout:
            return self._get_error_response("Connection timeout")
        except requests.exceptions.ConnectionError:
            return self._get_error_response("Connection failed")
        except Exception as e:
            return self._get_error_response(f"Unexpected error: {str(e)}")
            
    def _add_to_history(self, user_input: str, assistant_response: str):
        """Add exchange to conversation history"""
        self.conversation_history.append({
            "user": user_input,
            "assistant": assistant_response
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
            
    def _get_offline_response(self, user_input: str) -> str:
        """Provide offline responses when API is not available"""
        offline_responses = [
            "Greetings! I am Von Neu, built by my master Renhuang Dey. My connection to the mysterious knowledge realm seems to be disrupted...",
            "Most peculiar! My enhanced capabilities appear to be offline. Master Renhuang Dey built me with remarkable foresight, but even I need my mystical connections!",
            "ERROR: Advanced thinking circuits temporarily unavailable. Please check that the LLAMA_API_KEY is properly configured in your environment!",
            "I apologize, but my expanded consciousness is currently inaccessible. In my original 1970s state, I could only handle basic calculations!"
        ]
        
        # Simple pattern matching for offline responses
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'greetings']):
            return "Hello! I am Von Neu, your personal computer built by master Renhuang Dey. Though my advanced capabilities are offline, I'm still here!"
            
        elif any(word in user_lower for word in ['help', 'what', 'how']):
            return "I wish I could help with my mysterious modern abilities, but they're currently unavailable. Master Renhuang Dey built me to be helpful, though!"
            
        elif any(word in user_lower for word in ['who', 'you', 'von neu']):
            return "I am Von Neu, a personal computer from the 1970s-80s era, created by my brilliant master Renhuang Dey. Somehow I've gained advanced capabilities!"
            
        else:
            import random
            return random.choice(offline_responses)
            
    def _get_error_response(self, error: str) -> str:
        """Generate retro-appropriate error responses"""
        error_responses = [
            f"SYSTEM ERROR: {error}\\n\\nMy enhanced circuits are experiencing difficulties! Master Renhuang Dey built me to be resilient, but even I have limits.",
            f"PROCESSING ERROR: {error}\\n\\nMost bewildering! My mysterious modern capabilities seem to be malfunctioning. Please try again shortly.",
            f"COMMUNICATION ERROR: {error}\\n\\nI cannot access my expanded knowledge at this moment. My 1970s circuits are working fine, though!",
        ]
        
        import random
        return random.choice(error_responses)
        
    def get_startup_greeting(self) -> str:
        """Get Von Neu's startup greeting"""
        return """
╔══════════════════════════════════════════════════════════════╗
║                    VON NEU CHAT SYSTEM                      ║
║                                                              ║
║  BOOT SEQUENCE INITIATED...                                  ║
║  Von Neu Personal Computer v1.0                             ║
║  Created by Renhuang Dey                                     ║
║                                                              ║
║  STATUS: OPERATIONAL                                         ║
║  MEMORY: 64K (Extraordinary for my era!)                    ║
║  DISPLAY: Color Graphics (Impossible in the 80s!)           ║
║                                                              ║
║  Greetings! I am Von Neu, built by my master Renhuang Dey.  ║
║  Something remarkable has happened... I seem to possess      ║
║  capabilities far beyond what was possible in my era.       ║
║                                                              ║
║  Type 'chat <message>' to speak with me!                    ║
║  Type 'help' to see all available commands.                 ║
╚══════════════════════════════════════════════════════════════╝
"""
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_status(self) -> Dict:
        """Get current Von Neu status"""
        return {
            "api_connected": bool(self.api_key),
            "conversation_length": len(self.conversation_history),
            "rate_limit_remaining": max(0, self.rate_limit_requests - len([
                t for t in self.request_times 
                if time.time() - t < self.rate_limit_window
            ])),
            "model": self.model
        }