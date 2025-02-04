import asyncio
from chat_downloader import ChatDownloader
from utils import log_message

class ChatFetcher:
    """Handles both text and image generation triggers"""
    
    def __init__(self, config):
        self.config = config
        self.chat = ChatDownloader()
        self.running = False
        self.youtube_url = config["chat"]["youtube_url"]
        self.triggers = [prefix.lower() for prefix in config["chat"]["trigger_prefixes"]]

    async def start_listening(self, message_handler, chat_sender):
        self.running = True
        log_message(f"Starting chat listener for {self.youtube_url}")
        
        while self.running:
            try:
                await self._listen_loop(message_handler, chat_sender)
            except Exception as e:
                log_message(f"Connection error: {str(e)}. Reconnecting in 5s...", level="ERROR")
                await asyncio.sleep(5)

    async def _listen_loop(self, message_handler, chat_sender):
        async for message in self._async_chat_generator():
            if not self.running:
                break
                
            await self._process_message(message, message_handler, chat_sender)

    async def _async_chat_generator(self):
        loop = asyncio.get_event_loop()
        for message in await loop.run_in_executor(None, self.chat.get_chat, self.youtube_url):
            yield message

    async def _process_message(self, message, message_handler, chat_sender):
        try:
            text = message['message'].strip()
            user_name = message['author']['name']
            user_id = message['author']['id']
            timestamp = message['timestamp']

            # Check for image command or regular triggers
            if (any(trigger in text.lower() for trigger in self.triggers) or 
                text.lower().startswith('/imagine ')):
                
                log_message(f"Processing message from {user_name}: {text}")
                response = message_handler.process_message(
                    user_name=user_name,
                    user_id=user_id,
                    text=text,
                    timestamp=timestamp
                )
                
                await chat_sender.send_message(response)

        except KeyError as e:
            log_message(f"Invalid message format: {str(e)}", level="WARNING")
        except Exception as e:
            log_message(f"Message processing error: {str(e)}", level="ERROR")