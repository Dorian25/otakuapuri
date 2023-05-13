# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:00:34 2022

@author: Dorian
"""

import tkinter as tk
import pygame
from PIL import Image, ImageTk

from utils.FileManager import DIR_IMG_LOAD, DIR_MUSIC
from utils.utils import *

class SplashScreenFrame(tk.Frame):
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.gb_gif = Image.open(r'images/loading/OtakuApuri.gif')
      
        self.frames_gb_gif = [None] * self.gb_gif.n_frames

        # widgets
        self.label = tk.Label(self, background="black")
        self.label.pack(expand=True, fill="both")

        self.load_gif()
        self.update_gif(0, self.frames_gb_gif, self.label, 50)
        
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(DIR_MUSIC+"gameboy_start_up.mp3")
        pygame.mixer.music.play(loops=0)

    def load_gif(self):
        for x in range(self.gb_gif.n_frames):
            frame = ImageTk.PhotoImage(self.gb_gif.copy())
            self.frames_gb_gif[x] = frame
            self.gb_gif.seek(x)

    def update_gif(self, ind, frames_gif, label_gif, play_back_delay):
        # source : https://stackoverflow.com/questions/67704455/tkinter-gif-animation-falters-and-is-pixelated
        
        if ind == len(frames_gif):
            self.parent.show_loading_frame()    
        else:
            if ind == (len(frames_gif)//4):
                print(ind)
                self.play_sound()

            frame = frames_gif[ind]
            label_gif.configure(image=frame)
            
            ind += 1

            if type(play_back_delay) is dict:
                self._job_gif = self.after(play_back_delay[ind], self.update_gif, ind, frames_gif, label_gif, play_back_delay)
            else:
                self._job_gif = self.after(play_back_delay, self.update_gif, ind, frames_gif, label_gif, play_back_delay)
         