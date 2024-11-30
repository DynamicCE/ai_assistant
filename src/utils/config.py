from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class Config:
    def __init__(self):
        load_dotenv()
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.wake_word = os.getenv('WAKE_WORD', 'hey asistan')
        
        self._validate_config()
    
    def _validate_config(self):
        if not self.claude_api_key:
            raise ValueError("Claude API anahtarı bulunamadı!")
        if not self.elevenlabs_api_key:
            raise ValueError("ElevenLabs API anahtarı bulunamadı!") 