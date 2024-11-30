import customtkinter as ctk
from typing import Literal

class StatusIndicator(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.status_circle = ctk.CTkCanvas(
            self,
            width=20,
            height=20,
            bg=self._apply_appearance_mode(self._bg_color)
        )
        self.status_circle.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(
            self,
            text="Beklemede"
        )
        self.status_label.pack(side="left", padx=5)
        
        self.draw_circle("inactive")
        
    def draw_circle(self, status: Literal["active", "inactive", "error"]):
        color_map = {
            "active": "green",
            "inactive": "gray",
            "error": "red"
        }
        
        self.status_circle.delete("all")
        self.status_circle.create_oval(
            5, 5, 15, 15,
            fill=color_map[status],
            outline=""
        ) 