# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:00:34 2022

@author: Dorian
"""

import tkinter as tk
from tkinter import ttk
import random

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk
import pygame
import time

from utils.FileManager import FileManager, DIR_IMG_LOAD, DIR_MUSIC_LOAD
from utils.utils import *

class LoadingFrame(tk.Frame):
    DEFAULT_MAX_VAL_PB = 60
    
    def __init__(self, parent, quote_txt):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        # images
        #self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "sea.jpg"))
        self.logo_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "logo_128.png"))
        self.parchemin_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "parchemin_500.png"))
        
        # widgets
        self.canvas = tk.Canvas(self, width=1100, 
                                height=534, 
                                bd=0,
                                background="#1e1e1e",
                                highlightthickness=0,
                                relief='ridge')
    
        #self.canvas.create_image(0,0, image=self.bg_img , anchor="nw") 
        self.canvas.create_image(550,200, image=self.logo_img)
        self.canvas.create_image(550,380, image=self.parchemin_img)
        
        self.canvas.pack(expand=True, fill="both")
        
        s = ttk.Style()
        s.theme_use('default')
        s.configure("red.Horizontal.TProgressbar", 
                    background='#cf2410',
                    troughcolor="#48484a")       
        s.configure("red.Horizontal.TProgressbar", thickness=5)
        
        self.progressbar = ttk.Progressbar(self.canvas,
                                      style="red.Horizontal.TProgressbar", 
                                      orient="horizontal",
                                      length=600, 
                                      mode="determinate", 
                                      maximum=self.DEFAULT_MAX_VAL_PB,
                                      value=0)
        
        self.canvas.create_window(550, 280, window=self.progressbar)
        
        self.quote_txt = self.canvas.create_text(550,
                                                 380,
                                                 fill="black",
                                                 font=("Ink Free",13,"bold"),
                                                 width=400,
                                                 text=quote_txt)

        
    def animate(self):
        pygame.init()
        pygame.mixer.init()
        # Load and play sea sound
        list_musics = os.listdir(DIR_MUSIC_LOAD)
        pygame.mixer.music.load(DIR_MUSIC_LOAD+random.choice(list_musics))
        #pygame.mixer.music.play(-1) #music repeats indefinitely
        pygame.mixer.music.play()
                
        self.animate_progressbar()

        pygame.quit()
                
        self.parent.show_searching_frame()    
        
    
    def animate_progressbar(self):
        # animation de chargement
        for i in range(1,self.DEFAULT_MAX_VAL_PB+1):
            self.progressbar["value"] = i
            #self.canvas.itemconfig(self.progressbar_txt, text="{:.1f}%".format(100 * i/self.DEFAULT_MAX_VAL_PB))
            self.update()
            time.sleep(0.1)         