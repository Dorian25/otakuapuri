# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:56:45 2022

@author: Dorian
"""

import tkinter as tk

import os
import pygame

import random
import threading

from PIL import Image, ImageTk

import datetime
from time import strftime

from utils.FileManager import DIR_MUSIC_PLAYLIST, DIR_IMG_MP3, DIR_IMG_ICON


class MediaPlayerFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        
        # Constant
        self.playlist = os.listdir(DIR_MUSIC_PLAYLIST)
        list_bg_img = os.listdir(DIR_IMG_MP3)
        self.num_piste = 0

        # Images
        self.bg_playbutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_play.png'))
        self.bg_pausebutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_pause.png'))
        self.bg_nextbutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_next.png'))
        self.bg_prevbutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_previous.png'))
        self.bg_mediaplayer = ImageTk.PhotoImage(Image.open(DIR_IMG_MP3+random.choice(list_bg_img)))
        
        # String Variable for Dynamic Labels
        self.var_status_mp = tk.StringVar()
        self.var_track_mp = tk.StringVar()
        
        # Welcome Message 
        currentTime = datetime.datetime.now()
        if currentTime.hour < 12:
            self.var_track_mp.set("Good Morning ! You can listen to " + str(len(self.playlist)) + " songs !")
        elif 12 <= currentTime.hour < 18:
            self.var_track_mp.set("Good Afternoon ! You can listen to " + str(len(self.playlist)) + " songs !")
        else:
            self.var_track_mp.set("Good Evening ! You can listen to " + str(len(self.playlist)) + " songs !")
        
        # all widgets
        self.background_image_label = tk.Label(self, 
                                           image=self.bg_mediaplayer, 
                                           textvariable=self.var_track_mp, 
                                           font="Courier 12 italic bold",
                                           fg="#fff",
                                           compound="center",
                                           borderwidth=0)

        self.button_previous = tk.Button(self, 
                                         image=self.bg_prevbutton, 
                                         command=self.prev_song, 
                                         borderwidth=0,
                                         cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.button_play = tk.Button(self, 
                                     image=self.bg_playbutton, 
                                     command=self.play_song, 
                                     borderwidth=0,
                                     cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.button_next = tk.Button(self, 
                                     image=self.bg_nextbutton, 
                                     command=self.next_song, 
                                     borderwidth=0,
                                     cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        
        self.background_image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button_previous.pack(side=tk.LEFT)
        self.button_play.pack(side=tk.LEFT)
        self.button_next.pack(side=tk.LEFT)
           
    def play_song(self):
        pygame.init()
        pygame.mixer.init()
        if self.var_status_mp.get() == "play" :
            pygame.mixer.music.pause()
            self.var_status_mp.set("pause")
            self.var_track_mp.set("|| Paused")
            self.button_play.configure(image=self.bg_playbutton)
            self.update()
        elif self.var_status_mp.get() == "pause" :
            pygame.mixer.music.unpause()
            self.var_status_mp.set("play")
            self.var_track_mp.set("You're listening to : "+self.playlist[self.num_piste])
            self.button_play.configure(image=self.bg_pausebutton)
            self.update()
        else :
            self.var_status_mp.set("play")
            self.var_track_mp.set("You're listening to : "+self.playlist[self.num_piste])      
            pygame.mixer.music.load(DIR_MUSIC_PLAYLIST+self.playlist[self.num_piste])
            pygame.mixer.music.play()
            self.button_play.configure(image=self.bg_pausebutton)
            self.update()
        
    def next_song(self) :
        if self.var_status_mp.get() == "play" :
            if self.num_piste == (len(self.playlist)-1) :
                self.num_piste = 0
            else :
                self.num_piste += 1
            
            self.var_track_mp.set("You're listening to "+self.playlist[self.num_piste]) 
            pygame.mixer.music.load(DIR_MUSIC_PLAYLIST+self.playlist[self.num_piste])
            pygame.mixer.music.play()
        
        
    def prev_song(self) :
        if self.var_status_mp.get() == "play" :
         
            if self.num_piste == 0 :
                self.num_piste = len(self.playlist)-1
            else :
                self.num_piste -= 1
            
            self.var_track_mp.set("You're listening to "+self.playlist[self.num_piste]) 
            pygame.mixer.music.load(DIR_MUSIC_PLAYLIST+self.playlist[self.num_piste])
            pygame.mixer.music.play()