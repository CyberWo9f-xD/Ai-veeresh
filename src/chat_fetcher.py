import asyncio
import os
from chat_downloader import ChatDownloader
from utils import log_message

class ChatFetcher:
    """YouTube chat fetcher with cookie authentication"""
    
    def __init__(self, config):
        self.config = config
        self.chat = self._initialize_chat_downloader()
        self.running = False
        self.youtube_url = config["chat"]["youtube_url"]
        self.triggers = [prefix.lower() for prefix in config["chat"]["trigger_prefixes"]]

    def _initialize_chat_downloader(self):
        """Initialize with cookies and custom headers"""
        return ChatDownloader(
            cookies=os.path.join(os.path.dirname(__file__), '..', 'cookies.txt'),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
        )

    async def start_listening(self, message_handler, chat_sender):
        """Main listener with enhanced error handling"""
        self.running = True
        log_message(f"Starting authenticated chat listener for {self.youtube_url}")
        
        while self.running:
            try:
                await self._listen_loop(message_handler, chat_sender)
            except Exception as e:
                log_message(f"Connection error: {str(e)}. Reconnecting in 10s...", level="ERROR")
                await asyncio.sleep(10)

    async def _listen_loop(self, message_handler, chat_sender):
        """Processing loop with session management"""
        async for message in self._async_chat_generator():
            if not self.running:
                break
            await self._process_message(message, message_handler, chat_sender)

    async def _async_chat_generator(self):
        """Async generator with cookie-based authentication"""
        loop = asyncio.get_event_loop()
        try:
            chat = await loop.run_in_executor(
                None,
                self.chat.get_chat,
                self.youtube_url
            )
            for message in chat:
                yield message
        except Exception as e:
            log_message(f"Chat generator error: {str(e)}", level="ERROR")
            raise

    async def _process_message(self, message, message_handler, chat_sender):
        """Message processing with validation"""
        try:
            if not all(key in message['author'] for key in ['name', 'id']):
                return

            text = message['message'].strip()
            user_name = message['author']['name']
            user_id = message['author']['id']
            timestamp = message['timestamp']

            if any(trigger in text.lower() for trigger in self.triggers):
                log_message(f"Processing message from {user_name}: {text}")
                response = message_handler.process_message(
                    user_name=user_name,
                    user_id=user_id,
                    text=text,
                    timestamp=timestamp
                )
                await chat_sender.send_message(response)

        except KeyError as e:
            log_message(f"Message format error: {str(e)}", level="WARNING")
        except Exception as e:
            log_message(f"Processing error: {str(e)}", level="ERROR")

    def stop(self):
        """Graceful shutdown"""
        self.running = False
        self.chat.stop()