# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 15:33:42 2022

@author: Dorian
"""

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk

from utils.FileManager import FileManager, DIR_IMG_LOAD, DIR_MUSIC_LOAD
from utils.utils import *


class ErrorFrame(tk.Frame):
    # mettre son orage + vague
    FONT_SEARCH_ENTRY = ('Verdana',16)
    FONT_SEARCH_RESULT = ('Verdana', 12)
    COLUMNS = ('rank','title','score')
    
    def __init__(self, parent, error_txt):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        # images
        self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "sea_error.png"))
        self.logo_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "logo_128.png"))
        
        # widgets
        self.canvas = tk.Canvas(self, width=1000, 
                                height=500, 
                                bd=0,
                                highlightthickness=0,
                                relief='ridge')
    
        self.canvas.create_image(0,0, image=self.bg_img , anchor="nw") 
        self.canvas.create_image(500,200, image=self.logo_img)
        
        self.canvas.pack(expand=True, fill="both")
        
        self.error_txt = self.canvas.create_text(500,
                                                 380,
                                                 fill="white",
                                                 font=("Ink Free",13,"bold"),
                                                 width=400,
                                                 text="Pas de connexion internet !\n"+
                                                      "Veuillez vérifier votre connexion internet et réessayer.")
        
        self.retry_button = ttk.Button(self, text = "Retry", command = self.retry)
        self.canvas.create_window(520, 300, window=self.retry_button)
        
    def retry(self):
        self.parent.show_loading_frame(random.choice(quotes_anime))