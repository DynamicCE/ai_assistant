import os
from typing import List
import json

def clean_old_screenshots(directory: str, max_files: int = 10) -> None:
    """Eski screenshot'ları temizler"""
    try:
        files = sorted([f for f in os.listdir(directory) if f.startswith("screenshot_")])
        if len(files) > max_files:
            for old_file in files[:-max_files]:
                os.remove(os.path.join(directory, old_file))
    except Exception as e:
        print(f"Dosya temizleme hatası: {str(e)}")

def save_conversation_history(history: List[str], filename: str = "conversation_history.json") -> None:
    """Konuşma geçmişini kaydeder"""
    try:
        with open(f"resources/{filename}", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Konuşma geçmişi kaydetme hatası: {str(e)}") 