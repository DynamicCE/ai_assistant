import pyautogui
import pytesseract
from PIL import Image
import numpy as np
import cv2
from datetime import datetime
import os
from typing import Optional, Tuple

class ScreenReader:
    def __init__(self):
        self.screenshot_dir = "resources/screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
    def take_screenshot(self, area: Optional[Tuple[int, int, int, int]] = None) -> str:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.screenshot_dir}/screenshot_{timestamp}.png"
            
            if area:
                screenshot = pyautogui.screenshot(region=area)
            else:
                screenshot = pyautogui.screenshot()
                
            screenshot.save(filename)
            return filename
        except Exception as e:
            print(f"Screenshot hatası: {str(e)}")
            return ""
    
    def read_text_from_image(self, image_path: str, lang: str = 'tur') -> str:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            return text.strip()
        except Exception as e:
            print(f"OCR hatası: {str(e)}")
            return ""
    
    def analyze_screen_area(self, x1: int, y1: int, x2: int, y2: int) -> dict:
        try:
            area = (x1, y1, x2 - x1, y2 - y1)
            screenshot_path = self.take_screenshot(area)
            
            if not screenshot_path:
                return {"error": "Screenshot alınamadı"}
            
            text = self.read_text_from_image(screenshot_path)
            
            # Görüntü analizi için OpenCV kullanımı
            img = cv2.imread(screenshot_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            return {
                "text": text,
                "has_text": bool(text.strip()),
                "screenshot_path": screenshot_path,
                "dimensions": area,
                "has_edges": np.any(edges)
            }
            
        except Exception as e:
            return {"error": str(e)} 