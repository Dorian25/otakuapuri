# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:00:34 2022

@author: Dorian
"""

import tkinter as tk
import pygame
from PIL import Image

from utils.FileManager import DIR_IMG_LOAD, DIR_MUSIC
from utils.utils import *

class SplashScreenFrame(tk.Frame):
    FRAME_COUNT = Image.open(DIR_IMG_LOAD +'OtakuApuri.gif').n_frames
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        # images
        self.frames = [None] * self.FRAME_COUNT

        # widgets
        self.label = tk.Label(self, background="black")
        self.label.pack(expand=True, fill="both")
        
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(DIR_MUSIC+"gameboy_start_up.mp3")
        pygame.mixer.music.play(loops=0)
        
    def update(self, ind):
        # source : https://stackoverflow.com/questions/28518072/play-animations-in-gif-with-tkinter
        ind += 1

        if ind == self.FRAME_COUNT:
            self.parent.show_loading_frame()    
        else:
            if ind == (self.FRAME_COUNT//4):
                print(ind)
                self.play_sound()

            frame = tk.PhotoImage(file=DIR_IMG_LOAD +'OtakuApuri.gif', format='gif -index %i' % (ind))
            self.frames[ind] = frame
            self.label.configure(image=frame)
            self.after(17, self.update, ind) 