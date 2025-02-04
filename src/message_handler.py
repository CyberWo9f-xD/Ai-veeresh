from gender_predictor import GenderPredictor
from ai_responder import AIResponder
from memory_manager import MemoryManager
from utils import log_message

class MessageHandler:
    """Handles both text and image generation requests"""
    
    def __init__(self, config):
        self.config = config
        self.gender_predictor = GenderPredictor(config)
        self.ai_responder = AIResponder(config)
        self.memory_manager = MemoryManager()

    def process_message(self, user_name: str, user_id: str, text: str, timestamp: str):
        """Process message and route to appropriate handler"""
        try:
            # Check for image generation command
            if text.strip().lower().startswith('/imagine '):
                prompt = text[len('/imagine '):].strip()
                if not prompt:
                    return "Please provide a description after /imagine"
                return self.ai_responder.generate_image(prompt)
            
            # Normal message processing
            gender = self.gender_predictor.predict(user_name) or "unknown"
            memories = self.memory_manager.load_memories(user_id)
            
            response = self.ai_responder.generate_response(
                user_name=user_name,
                message=text,
                gender=gender,
                memories=memories
            )
            
            # Save conversation context
            current_context = [
                {"role": "user", "content": text},
                {"role": "assistant", "content": response}
            ]
            self.memory_manager.add_memory(user_id, current_context)
            
            return response
            
        except Exception as e:
            log_message(f"Message handling error: {str(e)}", level="ERROR")
            return self.ai_responder.get_error_response()