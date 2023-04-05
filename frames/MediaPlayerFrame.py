# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:56:45 2022

@author: Dorian
"""

import tkinter as tk

from PIL import Image, ImageTk
import vlc

import datetime
from time import strftime
import random

from utils.FileManager import DIR_IMG_ICON


class MusicVLCPlayerFrame(tk.Frame):

    morning_phrases = ['Good morning! How are you feeling today?', 
                   'Rise and shine! How are you doing this morning?', 
                   'Hey there, early bird! How\'s your morning going?', 
                   'Hello, sunshine! How are you feeling on this beautiful morning?', 
                   'Hey, sleepyhead! How are you feeling after your restful night?']

    afternoon_phrases = ['Good afternoon! How\'s your day going so far?', 
                     'Hey there, busy bee! How are you holding up this afternoon?', 
                     'Hello, afternoon delight! How are you feeling today?', 
                     'Hey, go-getter! How\'s your day treating you so far?', 
                     'Hey, dynamo! How\'s your energy holding up this afternoon?']

    evening_phrases = ['Good evening! How was your day?', 
                   'Hey there, night owl! How are you doing this evening?', 
                   'Hello, moonbeam! How are you feeling tonight?', 
                   'Hey, party animal! How\'s your evening going?', 
                   'Hey, nightcap! How are you feeling after a long day?']

    general_phrases = ['How\'s life treating you these days?', 
                   'What\'s new and exciting with you?', 
                   'How are you feeling lately?', 
                   'How\'s everything going in your world?', 
                   'What\'s the latest and greatest with you?']

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def initUI(self):
        # String Variable for Dynamic Labels
        self.var_status_mp = tk.StringVar()
        self.var_track_mp = tk.StringVar()

        # Welcome Message 
        currentTime = datetime.datetime.now()
        if currentTime.hour < 12:
            self.var_track_mp.set("Good Morning ! " + random.choice(self.morning_phrases+self.general_phrases))
        elif 12 <= currentTime.hour < 18:
            self.var_track_mp.set("Good Afternoon ! " + random.choice(self.afternoon_phrases+self.general_phrases))
        else:
            self.var_track_mp.set("Good Evening ! " +  random.choice(self.evening_phrases+self.general_phrases))

        # Images
        self.bg_playbutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_play.png'))
        self.bg_stopbutton = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON+'icon_stop.png'))

        # all widgets
        self.background_image_label = tk.Label(self,
                                           textvariable=self.var_track_mp, 
                                           font="Courier 12 italic bold",
                                           fg="#fff",
                                           background="#1e1e1e",
                                           compound="center",
                                           borderwidth=0)

        self.button_play = tk.Button(self, 
                                     image=self.bg_playbutton, 
                                     command=self.play, 
                                     borderwidth=0,
                                     cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        
        self.background_image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button_play.pack(side=tk.LEFT)


    def play(self):
        
        if self.player.is_playing():
            self.player.stop()
            self.var_track_mp.set("⏹ Music Stopped")
            self.button_play.configure(image=self.bg_playbutton)
            self.update()
            
        else :
            media = self.instance.media_new('https://pool.anison.fm/AniSonFM(320)')
            self.player.set_media(media)
            self.player.play()
            self.var_track_mp.set("♫♪┏(°.°)┛ You're listening to Anison.fm ! ┗(°.°)┓♪♫")
            self.button_play.configure(image=self.bg_stopbutton)
            self.update()

    def stop(self):
        self.player.stop()