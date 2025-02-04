import json
import os
from typing import Dict, List, Any

class MemoryManager:
    """Manages user-specific conversation memories stored in JSON files."""
    
    def __init__(self, memory_dir: str = "user_memories"):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def _get_user_memory_path(self, user_id: str) -> str:
        """Get the path to a user's memory file."""
        return os.path.join(self.memory_dir, f"user_{user_id}.json")

    def load_memories(self, user_id: str) -> Dict[str, List[Dict[str, str]]]:
        """Load a user's conversation memories from their JSON file."""
        memory_path = self._get_user_memory_path(user_id)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, "r") as file:
                    return json.load(file)
            else:
                return {"memories": []}
        except json.JSONDecodeError:
            return {"memories": []}

    def save_memories(self, user_id: str, memories: Dict[str, List[Dict[str, str]]]):
        """Save a user's conversation memories to their JSON file."""
        memory_path = self._get_user_memory_path(user_id)
        with open(memory_path, "w") as file:
            json.dump(memories, file, indent=2)

    def add_memory(self, user_id: str, context: List[Dict[str, str]]):
        """Add a new conversation memory for a user."""
        memories = self.load_memories(user_id)
        memories["memories"].append({"context": context})
        self.save_memories(user_id, memories)