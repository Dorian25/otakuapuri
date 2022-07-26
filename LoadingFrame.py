# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:00:34 2022

@author: Dorian
"""

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk
import pygame
import time

from DbManager import DbManager
from FileManager import FileManager, DIR_IMG_LOAD, DIR_MUSIC_LOAD
from utils import *

class LoadingFrame(tk.Frame):
    DEFAULT_MAX_VAL_PB = 60
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        # images
        self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_LOAD + "sea.jpg"))
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
        
        self.canvas.create_window(500, 280, window=self.progressbar)
        
        self.progressbar_txt = self.canvas.create_text(500,
                                                       315,
                                                       fill="white",
                                                       font="Verdana 20 bold",
                                                       text="Welcome to the board !")

        
    def animate(self):
        # Init pygame mixer
        pygame.init()
        pygame.mixer.init()
        # Load and play sea sound
        pygame.mixer.music.load(DIR_MUSIC_LOAD+"sea_sound.mp3")
        pygame.mixer.music.play(-1)
        
        db_manager = DbManager("test.db")
        
        key_figures = {}
        
        try :
            if test_internet():
                if db_manager.is_empty_db():
                    self.realtime_animation()
                else :
                    self.default_animation()
                
                key_figures["number_of_series"] = db_manager.count_series()
                key_figures["number_of_volumes"] = db_manager.count_volumes()
                
                db_manager.close()
                pygame.quit()
                
                self.parent.show_searching_frame(key_figures)    
            else:
                messagebox.showerror("No connection", "Please activate your connection !")
        except ConnectionError:
            messagebox.showerror("No connection", "Please activate your connection !")
        
    
    def default_animation(self):
        # animation de chargement
        for i in range(1,self.DEFAULT_MAX_VAL_PB+1):
            self.progressbar["value"] = i
            self.canvas.itemconfig(self.progressbar_txt, text="{:.1f}%".format(100 * i/self.DEFAULT_MAX_VAL_PB))
            self.update()
            time.sleep(0.1)
            
    def realtime_animation(self):
        db_manager = DbManager("test.db")
        #self.progressbar.maximum = 
        pass
        

        
         

    