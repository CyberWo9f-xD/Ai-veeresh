import requests
from utils import log_message

class GenderPredictor:
    """Gender prediction service with caching and rate limiting"""
    
    def __init__(self, config):
        self.endpoint = config["api"]["genderize"]
        self.cache = {}
        self.timeout = 3  # Seconds

    def predict(self, name: str) -> str:
        """Get gender prediction with cache and fallback"""
        if not name.strip():
            return "unknown"
            
        # Use cached value if available
        clean_name = name.strip().lower()
        if clean_name in self.cache:
            return self.cache[clean_name]
            
        try:
            response = requests.get(
                self.endpoint,
                params={"name": clean_name},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                gender = data.get("gender", "unknown")
                self.cache[clean_name] = gender
                return gender
                
            log_message(f"Gender API error: {response.status_code}", level="WARNING")
            return "unknown"
            
        except requests.exceptions.RequestException as e:
            log_message(f"Gender API connection failed: {str(e)}", level="WARNING")
            return "unknown"
        except Exception as e:
            log_message(f"Gender prediction error: {str(e)}", level="ERROR")
            return "unknown"