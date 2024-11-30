from anthropic import Anthropic
from typing import Optional
from src.utils.config import Config

class ClaudeAI:
    def __init__(self, config: Config):
        self.client = Anthropic(api_key=config.claude_api_key)
        self.context = "Sen bir sesli asistansın. Kısa ve öz cevaplar vermelisin."
        self.conversation_history = []
    
    def process_command(self, command: str) -> Optional[str]:
        try:
            self.conversation_history.append(f"User: {command}")
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.7,
                system=self.context,
                messages=[
                    {"role": "user", "content": f"{self.context}\n\nKullanıcı: {command}"}
                ]
            )
            
            response = message.content[0].text
            self.conversation_history.append(f"Assistant: {response}")
            return response
            
        except Exception as e:
            print(f"Claude AI hatası: {str(e)}")
            return "Üzgünüm, şu anda cevap veremiyorum."
    
    def clear_context(self):
        self.conversation_history.clear() 