import os
import random
from openai import OpenAI
from utils import log_message, load_config

class AIResponder:
    """Handles both text and image generation"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            api_key=os.getenv("AI_API_KEY") or "Free-For-YT-Subscribers-@DevsDoCode-WatchFullVideo",
            base_url=config["api"]["ai_endpoint"]
        )
        self.text_model = config["ai"]["model"]
        self.temperature = config["ai"]["temperature"]
        self.max_tokens = config["ai"]["max_tokens"]
        self.prompts = load_config("prompts.json")

    def generate_response(self, user_name: str, message: str, gender: str, memories: dict):
        """Generate text response"""
        try:
            messages = self._build_message_chain(memories, user_name, gender, message)
            
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
            
        except Exception as e:
            log_message(f"Text generation error: {str(e)}", level="ERROR")
            return self.get_error_response()

    def generate_image(self, prompt: str) -> str:
        """Generate image response"""
        try:
            response = self.client.images.generate(
                model="flux-dev",
                prompt=prompt,
                size="1024x1024"
            )
            return response.data[0].url
            
        except Exception as e:
            log_message(f"Image generation error: {str(e)}", level="ERROR")
            return random.choice([
                "Couldn't generate that image, try something else?",
                "My art skills failed me on that one!"
            ])

    def _build_message_chain(self, memories, user_name, gender, message):
        """Construct message chain for text generation"""
        messages = [
            {"role": "system", "content": self.prompts["system_prompt"]}
        ]
        
        for memory in memories.get("memories", []):
            messages.extend(memory["context"])
            
        messages.append({
            "role": "user",
            "content": f"{user_name} ({gender}): {message}"
        })
        
        return messages

    def get_error_response(self) -> str:
        return random.choice(self.prompts["error_responses"])