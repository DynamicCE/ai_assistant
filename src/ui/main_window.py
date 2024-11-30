import customtkinter as ctk
from PIL import Image, ImageTk
import threading
from src.core.speech_recognition import SpeechRecognizer
from src.utils.config import Config
from typing import Optional
import os

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Asistan")
        self.geometry("800x600")
        
        # Tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.config = Config()
        self.speech_recognizer = SpeechRecognizer(self.config)
        self.is_listening = False
        self.setup_ui()
        
    def setup_ui(self):
        # Ana container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sol panel
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Durum göstergesi
        self.status_label = ctk.CTkLabel(
            self.left_panel,
            text="Dinleme Beklemede...",
            font=("Arial", 16)
        )
        self.status_label.pack(pady=10)
        
        # Mikrofon butonu
        self.mic_button = ctk.CTkButton(
            self.left_panel,
            text="Dinlemeyi Başlat",
            command=self.toggle_listening,
            width=200,
            height=40
        )
        self.mic_button.pack(pady=10)
        
        # Konuşma geçmişi
        self.history_frame = ctk.CTkFrame(self.left_panel)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.history_label = ctk.CTkLabel(
            self.history_frame,
            text="Konuşma Geçmişi",
            font=("Arial", 14)
        )
        self.history_label.pack(pady=5)
        
        self.history_text = ctk.CTkTextbox(
            self.history_frame,
            width=400,
            height=300
        )
        self.history_text.pack(fill="both", expand=True)
        
        # Sağ panel
        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Screenshot önizleme
        self.preview_label = ctk.CTkLabel(
            self.right_panel,
            text="Screenshot Önizleme",
            font=("Arial", 14)
        )
        self.preview_label.pack(pady=5)
        
        self.preview_frame = ctk.CTkFrame(
            self.right_panel,
            width=300,
            height=200
        )
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.mic_button.configure(text="Dinlemeyi Durdur")
            self.status_label.configure(text="Dinleniyor...")
            
            # Dinleme işlemini ayrı thread'de başlat
            self.listen_thread = threading.Thread(target=self.start_listening)
            self.listen_thread.daemon = True
            self.listen_thread.start()
        else:
            self.is_listening = False
            self.mic_button.configure(text="Dinlemeyi Başlat")
            self.status_label.configure(text="Dinleme Beklemede...")
    
    def start_listening(self):
        try:
            while self.is_listening:
                self.speech_recognizer.start_listening()
        except Exception as e:
            self.add_to_history(f"Hata: {str(e)}")
    
    def add_to_history(self, text: str):
        self.history_text.insert("end", f"{text}\n")
        self.history_text.see("end")
    
    def update_preview(self, image_path: Optional[str]):
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((280, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            preview_label = ctk.CTkLabel(
                self.preview_frame,
                image=photo,
                text=""
            )
            preview_label.image = photo
            preview_label.pack(fill="both", expand=True) 