import speech_recognition as sr
from typing import Optional
import logging
from src.core.claude_integration import ClaudeAI
from src.core.voice_synthesis import VoiceSynthesis
from src.core.screen_reader import ScreenReader
from src.utils.config import Config
from src.utils.database import Database

class SpeechRecognizer:
    def __init__(self, config: Config):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.claude_ai = ClaudeAI(config)
        self.voice_synthesis = VoiceSynthesis(config)
        self.screen_reader = ScreenReader()
        self.wake_word = config.wake_word
        self.db = Database()
        self._setup_recognizer()
        
    def _setup_recognizer(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def start_listening(self):
        print(f"Dinlemeye başladım! '{self.wake_word}' diyerek beni çağırabilirsin...")
        
        while True:
            text = self._listen()
            if text and self.wake_word in text.lower():
                self.voice_synthesis.speak("Seni duydum! Ne yapmamı istersin?")
                command = self._listen()
                if command:
                    self._handle_command(command)
    
    def _listen(self) -> Optional[str]:
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio, language="tr-TR")
                return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Ses tanıma servisi şu anda çalışmıyor...")
            return None
            
    def _handle_command(self, command: str):
        try:
            command_type = "general"
            success = True
            
            if "ekran görüntüsü al" in command:
                command_type = "screenshot"
                screenshot_path = self.screen_reader.take_screenshot()
                response = f"Ekran görüntüsü kaydedildi: {screenshot_path}"
            
            elif "ekranı oku" in command:
                command_type = "ocr"
                screenshot_path = self.screen_reader.take_screenshot()
                text = self.screen_reader.read_text_from_image(screenshot_path)
                response = f"Ekranda şunlar yazıyor: {text}" if text else "Ekranda okunabilir metin bulamadım."
            
            else:
                response = self.claude_ai.process_command(command)
            
        except Exception as e:
            success = False
            response = f"Bir hata oluştu: {str(e)}"
        
        # Veritabanına kaydet
        self.db.save_conversation(command, response, command_type, success)
        self.db.update_command_stats(command_type, success)
        
        if response:
            print(f"Cevabım: {response}")
            self.voice_synthesis.speak(response)