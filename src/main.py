import asyncio
from utils import setup_logging, load_config, log_message
from chat_fetcher import ChatFetcher
from message_handler import MessageHandler
from chat_sender import ChatSender

def main():
    """Main entry point for Ai-Veeresh"""
    setup_logging()
    log_message("Starting Ai-Veeresh...")
    
    try:
        # Load main configuration
        config = load_config("settings.json")
        
        # Validate essential configuration
        if "api" not in config:
            raise ValueError("Missing API section in settings.json")
            
        if "chat" not in config:
            raise ValueError("Missing chat configuration in settings.json")

        chat_fetcher = ChatFetcher(config)
        message_handler = MessageHandler(config)
        chat_sender = ChatSender(config)
        asyncio.run(chat_fetcher.start_listening(message_handler, chat_sender))
        
    except Exception as e:
        log_message(f"Critical error: {str(e)}", level="ERROR")
        raise

if __name__ == "__main__":
    main()