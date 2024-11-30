from elevenlabs import generate, set_api_key
from src.utils.config import Config
import tempfile
import pygame
from typing import Optional

class VoiceSynthesis:
    def __init__(self, config: Config):
        set_api_key(config.elevenlabs_api_key)
        pygame.mixer.init()
        
    def speak(self, text: str) -> Optional[str]:
        try:
            audio = generate(
                text=text,
                voice="Bella",
                model="eleven_multilingual_v2"
            )
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio)
                temp_path = temp_file.name
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            return None
            
        except Exception as e:
            print(f"Ses sentezi hatası: {str(e)}")
            return str(e) 