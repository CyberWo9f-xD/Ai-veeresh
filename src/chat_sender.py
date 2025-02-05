# Update chat_sender.py
import asyncio
import requests
from tenacity import retry, wait_exponential, stop_after_attempt
from utils import log_message

class ChatSender:
    """Handles message splitting and delayed sending for YouTube chat"""
    
    def __init__(self, config):
        self.endpoint = config["api"]["chat_sender"]
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "<origin-url>"
        }
        self.max_length = 200  # YouTube chat character limit
        self.delay = 1  # Seconds between messages

    def _split_message(self, text: str) -> list:
        """Split long messages into chunks under max_length without breaking words"""
        chunks = []
        while len(text) > 0:
            if len(text) <= self.max_length:
                chunks.append(text)
                break
            
            # Find last space within limit
            split_at = text.rfind(' ', 0, self.max_length)
            if split_at == -1:
                split_at = self.max_length
                
            chunks.append(text[:split_at].strip())
            text = text[split_at:].strip()
            
        return chunks

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), 
           stop=stop_after_attempt(3),
           reraise=True)
    async def _send_single_message(self, message: str):
        """Send individual message part"""
        try:
            response = requests.post(
                self.endpoint,
                json={"message": message},
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            log_message(f"Message part sent: {message}")
            return True
        except requests.exceptions.RequestException as e:
            log_message(f"Failed to send message part: {str(e)}", level="WARNING")
            raise

    async def send_message(self, full_response: str):
        """Handle message splitting and delayed sending"""
        try:
            chunks = self._split_message(full_response)
            
            for index, chunk in enumerate(chunks):
                # Add delay between chunks (except first message)
                if index > 0:
                    await asyncio.sleep(self.delay)
                    
                await self._send_single_message(chunk)
                
            log_message(f"Successfully sent {len(chunks)} message parts")
            return True
            
        except Exception as e:
            log_message(f"Message sending failed: {str(e)}", level="ERROR")
            return False