# Veeresh AI Bot 🤖

Veeresh is an intelligent AI bot designed for YouTube live streams. It can:
- Respond to chat messages in real-time
- Generate creative images using `/imagine` command
- Remember conversations for personalized interactions
- Handle long messages by splitting them into parts

## Features ✨
- **Real-Time Chat Interaction**: Engage with viewers instantly
- **Image Generation**: Create art with `/imagine [prompt]`
- **Memory System**: Remembers past conversations
- **Multi-Language Support**: Works in multiple languages
- **Open Source**: Free for All.

## Installation 🛠️

### Windows
1. Run `setup.bat`
2. Activate virtual environment: `venv\Scripts\activate`
3. Run the bot: `python src\main.py`

### Linux/Mac
1. Make setup script executable: `chmod +x setup.sh`
2. Run setup: `./setup.sh`
3. Activate virtual environment: `source venv/bin/activate`
4. Run the bot: `python3 src/main.py`

## Configuration ⚙️
1. Create `.env` file:
   ```plaintext
   AI_API_KEY="openai_api_key_here"
   YOUTUBE_LIVE_URL="https://www.youtube.com/watch?v=your_live_stream"