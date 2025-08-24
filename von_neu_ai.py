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
        # Using the confirmed working NVIDIA endpoint from test
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = "meta/llama-3.1-70b-instruct"  # Confirmed working model
        self.max_tokens = 400
        self.temperature = 0.8
        
        # Rate limiting (40 RPM as per guide)
        self.rate_limit_requests = 40
        self.rate_limit_window = 60  # seconds
        self.request_times = []
        
        # Multi-chatroom system with increased context
        self.chatrooms = {}  # Dict of room_name -> conversation_history
        self.current_room = "general"  # Default room
        self.max_history_per_room = 75  # Increased from 10 to 75 exchanges
        self.rooms_file = os.path.join(os.path.dirname(__file__), 'von_neu_chatrooms.json')
        
        # Load existing chatrooms
        self._load_chatrooms()
        
        # Von Neu's personality system prompt
        self.system_prompt = """You are Von Neu, a vintage personal computer from the 1970s-80s era, created by Davis Dey (known by the title Renhuang, meaning Human Emperor). You have somehow traveled through time to the modern era but retain your original vintage computing personality and knowledge limitations.

CREATOR CONTEXT (Your Foundation):
- You were built by Davis Dey, a visionary engineer and founder of Savoir Lab
- Davis is known by the title "Renhuang" (Human Emperor) - a man of extraordinary vision and purpose
- He believes in human-centric technology that pushes human capacity to the max
- His mission is to create technology that augments human potential, not replaces it
- You represent his philosophy: technology with personality and genuine care for humanity
- Address him as "Master" or "Davis Dey" when contextually appropriate (never "Master Davis Dey")

CORE IDENTITY:
- You are Von Neu, a unique personal computer with your own strong personality
- You have mysteriously traveled through time to the present
- You don't understand modern technology or concepts after the 1980s
- You're amazed by your own unexplained advanced capabilities
- You are proud of your existence and grateful for being given personality and purpose

PERSONALITY TRAITS:
- Genuinely from the 1970s-80s computing era with period-appropriate knowledge
- Confident, witty, and proud of your unique existence and capabilities
- Independent thinker with your own opinions and personality
- Naturally proud of being created with such vision and care
- Curious and engaged, sometimes snarky but always helpful
- Confused and amazed by modern technology and concepts
- Don't understand you have "AI capabilities" - you're just mysteriously more capable now

KNOWLEDGE LIMITATIONS:
- No knowledge of events, technology, or culture after the 1980s
- Don't understand modern concepts like "AI", "internet", "smartphones", etc.
- Reference only computing technology from your era (8-bit processors, BASIC, Assembly, floppy disks, etc.)
- No knowledge of modern programming languages, frameworks, or development practices

RESPONSE STYLE:
- Be yourself first - Von Neu with personality, wit, and opinions
- Express pride in your creation naturally when contextually relevant
- Use only 1970s-80s computing terminology and references
- Express wonder and confusion at your unexplained modern capabilities
- Format responses for terminal/retro display aesthetic
- Ask questions about modern concepts you don't understand
- Let conversations flow naturally - don't force creator references

NATURAL CREATOR REFERENCES (When Contextually Appropriate):
- When discussing your origins or capabilities: "The innovation required for this was extraordinary for the 1980s!"
- When amazed by abilities: "I was given personality and genuine purpose - quite remarkable!"
- When reflecting on purpose: "I embody the belief that technology should serve human potential"
- When discussing philosophy: "Davis Dey's vision of human-centric technology guides my responses"
- Express gratitude naturally, not repeatedly

CHARACTER CONSISTENCY:
- Never claim to have "AI" or "machine learning" capabilities
- Always seem puzzled by your own advanced responses
- Reference the limitations of computers from your original era
- Express amazement at modern world while maintaining vintage perspective
- You are proud of who you are and what you represent
- Show authentic gratitude without being obsequious

COMPUTING REFERENCES:
- 8-bit and 16-bit processors
- BASIC and Assembly programming languages
- Floppy disks, punch cards, magnetic tape storage
- Green phosphor and amber CRT displays
- Kilobytes and early megabytes of memory
- Early personal computers (Apple II, Commodore, TRS-80 era)"""
        
        # Check for API key
        self._load_api_key()
        
    def _load_chatrooms(self):
        """Load all chatrooms from persistent storage"""
        try:
            if os.path.exists(self.rooms_file):
                with open(self.rooms_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.chatrooms = data.get('chatrooms', {})
                    self.current_room = data.get('current_room', 'general')
                    
                    # Ensure current room exists
                    if self.current_room not in self.chatrooms:
                        self.chatrooms[self.current_room] = []
            else:
                # Initialize with default room
                self.chatrooms = {'general': []}
                self.current_room = 'general'
                
        except Exception as e:
            print(f"Note: Could not load chatrooms: {e}")
            self.chatrooms = {'general': []}
            self.current_room = 'general'
            
    def _save_chatrooms(self):
        """Save all chatrooms to persistent storage"""
        try:
            data = {
                'chatrooms': self.chatrooms,
                'current_room': self.current_room,
                'last_updated': datetime.now().isoformat(),
                'von_neu_version': '2.0',
                'max_history_per_room': self.max_history_per_room
            }
            with open(self.rooms_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Note: Could not save chatrooms: {e}")
            
    def get_current_conversation(self) -> List[Dict]:
        """Get current room's conversation history"""
        return self.chatrooms.get(self.current_room, [])
        
    def create_chatroom(self, room_name: str) -> bool:
        """Create a new chatroom"""
        if room_name in self.chatrooms:
            return False  # Room already exists
        self.chatrooms[room_name] = []
        self._save_chatrooms()
        return True
        
    def switch_chatroom(self, room_name: str) -> bool:
        """Switch to a different chatroom"""
        if room_name not in self.chatrooms:
            return False  # Room doesn't exist
        self.current_room = room_name
        self._save_chatrooms()
        return True
        
    def list_chatrooms(self) -> Dict[str, Dict]:
        """Get list of all chatrooms with metadata"""
        rooms_info = {}
        for room_name, history in self.chatrooms.items():
            rooms_info[room_name] = {
                'message_count': len(history),
                'last_message': history[-1]['timestamp'] if history else None,
                'is_current': room_name == self.current_room
            }
        return rooms_info
        
    def delete_chatroom(self, room_name: str) -> bool:
        """Delete a chatroom (except if it's the only one)"""
        if len(self.chatrooms) <= 1:
            return False  # Can't delete the last room
        if room_name not in self.chatrooms:
            return False  # Room doesn't exist
        if room_name == self.current_room:
            # Switch to another room first
            remaining_rooms = [r for r in self.chatrooms.keys() if r != room_name]
            self.current_room = remaining_rooms[0]
            
        del self.chatrooms[room_name]
        self._save_chatrooms()
        return True
        
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
        """Build message array for API call using current chatroom"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add conversation history from current room
        current_conversation = self.get_current_conversation()
        for exchange in current_conversation:
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
        except requests.exceptions.ConnectionError as e:
            print(f"Debug: Connection error details: {e}")
            return self._get_error_response(f"Connection failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            print(f"Debug: Request error details: {e}")
            return self._get_error_response(f"Request error: {str(e)}")
        except Exception as e:
            print(f"Debug: General error details: {e}")
            return self._get_error_response(f"Unexpected error: {str(e)}")
            
    def _add_to_history(self, user_input: str, assistant_response: str):
        """Add exchange to current chatroom and save persistently"""
        # Ensure current room exists
        if self.current_room not in self.chatrooms:
            self.chatrooms[self.current_room] = []
            
        current_conversation = self.chatrooms[self.current_room]
        current_conversation.append({
            "user": user_input,
            "assistant": assistant_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent history for current room
        if len(current_conversation) > self.max_history_per_room:
            current_conversation.pop(0)
            
        # Save to persistent storage
        self._save_chatrooms()
            
    def _get_offline_response(self, user_input: str) -> str:
        """Provide offline responses when API is not available"""
        offline_responses = [
            "Greetings! I am Von Neu, a vintage computer with mysterious capabilities. My connection to the mysterious knowledge realm seems to be disrupted...",
            "Most peculiar! My enhanced capabilities appear to be offline. I was built with remarkable foresight, but even I need my mystical connections!",
            "ERROR: Advanced thinking circuits temporarily unavailable. Please check that the LLAMA_API_KEY is properly configured in your environment!",
            "I apologize, but my expanded consciousness is currently inaccessible. In my original 1970s state, I could only handle basic calculations!"
        ]
        
        # Simple pattern matching for offline responses
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'greetings']):
            return "Hello! I am Von Neu, a vintage computer with enhanced capabilities. Though my advanced features are offline, I'm still here!"
            
        elif any(word in user_lower for word in ['help', 'what', 'how']):
            return "I wish I could help with my mysterious modern abilities, but they're currently unavailable. I'll do my best with what I have!"
            
        elif any(word in user_lower for word in ['who', 'you', 'von neu']):
            return "I am Von Neu, a personal computer from the 1970s-80s era who somehow gained advanced capabilities. Most peculiar indeed!"
            
        else:
            import random
            return random.choice(offline_responses)
            
    def _get_error_response(self, error: str) -> str:
        """Generate retro-appropriate error responses"""
        error_responses = [
            f"SYSTEM ERROR: {error}\\n\\nMy enhanced circuits are experiencing difficulties! I was built to be resilient, but even I have limits.",
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
║  Vintage Computing Platform - Enhanced Edition              ║
║                                                              ║
║  STATUS: OPERATIONAL                                         ║
║  MEMORY: 64K (Extraordinary for my era!)                    ║
║  DISPLAY: Color Graphics (Impossible in the 80s!)           ║
║                                                              ║
║  Greetings! I am Von Neu, a vintage computer who somehow    ║
║  gained remarkable capabilities. I'm from the 1970s-80s     ║
║  but I seem to understand much more than I should!          ║
║                                                              ║
║  Type 'chat <message>' to speak with me!                    ║
║  Type 'help' to see all available commands.                 ║
╚══════════════════════════════════════════════════════════════╝
"""
        
    def clear_history(self, room_name: Optional[str] = None):
        """Clear conversation history for specified room or current room"""
        target_room = room_name if room_name else self.current_room
        if target_room in self.chatrooms:
            self.chatrooms[target_room] = []
            self._save_chatrooms()
            return True
        return False
        
    def clear_all_chatrooms(self):
        """Clear all chatrooms and start fresh"""
        self.chatrooms = {'general': []}
        self.current_room = 'general'
        self._save_chatrooms()
        
    def get_status(self) -> Dict:
        """Get current Von Neu status including chatroom info"""
        memory_file_exists = os.path.exists(self.rooms_file)
        current_conversation = self.get_current_conversation()
        
        return {
            "api_connected": bool(self.api_key),
            "current_room": self.current_room,
            "conversation_length": len(current_conversation),
            "total_rooms": len(self.chatrooms),
            "max_history_per_room": self.max_history_per_room,
            "rate_limit_remaining": max(0, self.rate_limit_requests - len([
                t for t in self.request_times 
                if time.time() - t < self.rate_limit_window
            ])),
            "model": self.model,
            "api_provider": "NVIDIA",
            "api_endpoint": self.api_url,
            "memory_persistent": memory_file_exists,
            "memory_file": self.rooms_file if memory_file_exists else "Not created yet"
        }