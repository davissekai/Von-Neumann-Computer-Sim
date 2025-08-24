# Von Neu AI Setup Instructions

## Quick Start

1. **Get API Access**
   - Obtain a Llama-Maverick 17B API key from DeepInfra or similar provider
   - Note: The guide mentions 40 RPM rate limit

2. **Configure Environment**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API key
   # Replace 'your_api_key_here' with your actual API key
   LLAMA_API_KEY=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
   ```

3. **Install Dependencies**
   ```bash
   pip install requests python-dotenv
   ```

4. **Test Von Neu**
   ```bash
   # Run the Python version
   python main_interface.py
   
   # Try the new chat command
   VON-NEU> chat Hello Von Neu!
   ```

## Environment Variables

Create a `.env` file in the project root with:

```bash
LLAMA_API_KEY="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"
VON_NEU_MAX_TOKENS=400
VON_NEU_TEMPERATURE=0.8
VON_NEU_MAX_HISTORY=10
VON_NEU_RATE_LIMIT=40
VON_NEU_RATE_WINDOW=60
```

## Von Neu Commands

### Python Version
- `chat <message>` - Chat with Von Neu
- `von-neu-status` - Check AI system status
- `von-neu-clear` - Clear conversation history
- `von-neu-greeting` - Show startup greeting

### Web Version
- Click "Chat with Von Neu" button
- Type in chat input field
- Press Enter to send message

## Personality Features

Von Neu will:
- Act as a 1970s-80s computer built by Renhuang Dey
- Be confused by modern technology
- Reference vintage computing concepts
- Express amazement at his own capabilities
- Always credit Renhuang Dey as his creator
- Use retro computing terminology

## Troubleshooting

### No API Key Error
```
Warning: LLAMA_API_KEY environment variable not set
```
**Solution**: Create `.env` file with your API key

### Rate Limit Errors
```
VON NEU PROCESSING OVERLOAD...
```
**Solution**: Wait a minute and try again (40 requests per minute limit)

### Connection Errors
```
COMMUNICATION ERROR: Connection failed
```
**Solution**: Check internet connection and API key validity

## Security Notes

- Never commit `.env` files to version control
- Keep API keys secure and private
- The `.env` file is already in `.gitignore`
- Use environment variables for production deployment

## Development Notes

- Von Neu personality is defined in `von_neu_ai.py`
- System prompt ensures character consistency
- Offline mode provides fallback responses
- Rate limiting respects API constraints
- Conversation history maintains context