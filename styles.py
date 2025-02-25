from tkinter import *
from tkinter import ttk

class MinesweeperStyles:
    def __init__(self):
        self.style = ttk.Style()
        self.configure_styles()
        self.bg_color = "#999999"
        self.bg_color_selected = "#656565"
        self.bg_color_bomb = "red"
        self.color_bomb = "#000000"

    def configure_styles(self):
        self.style.theme_use("clam")
        self.style.configure('MS.TFrame', background="#999999", borderwidth=2, relief='raised')
        self.style.configure('MS.TLabel', background="#999999", font=("Helvetica", 10, "bold"))
        self.style.configure('MS.TButton', background="#999999", relief='raised', width=2, )
        self.style.configure('MS_bomb.TButton', background="red", relief='sunken', width=2,)
        self.style.configure('MS_pressed.TButton', background="#656565", relief='sunken', width=2,)
        self.style.map('MS.TButton', background=[('pressed', "#479d2e"), ('active', "#656565")])
        self.style.map('MS_bomb.TButton', background=[('pressed', "red")])
        self.style.map('MS.TButton', background=[('pressed', "#656565"), ('active', "#656565")])