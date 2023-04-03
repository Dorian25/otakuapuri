# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 14:31:49 2023

@author: Dorian
"""

import tkinter as tk
from pytube import Playlist
from tkinter import ttk
import vlc
import random
from PIL import Image, ImageTk
from utils.FileManager import FileManager, DIR_IMG_ICON, DIR_TMP_COVERS, DIR_TMP_ANIME
import requests
import threading
import time
from datetime import datetime

class OptubeFrame(tk.Frame):
    
    def __init__(self, parent, app, vlc_args=[]):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent

        self.app = app 

        self.current_position = 0
        self.path_video = ""

        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        events = self.media_player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.next_video)
        events.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.pos_callback, self.media_player)

        self.video_length = 0
        self.fullscreen_state = False
        self.mute_state = False

        self.__set_bindings()
        self.__on_tick()

    def splash_screen(self):
        self.logo_img = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_logo.png"))
        self.canvas = tk.Canvas(self, 
                                width=1100, 
                                height=534, 
                                bd=0,
                                background="white",
                                highlightthickness=0,
                                relief='ridge')
        self.canvas.pack(expand=True, fill="both")
        self.canvas.create_image(550,267, image=self.logo_img)

        thread_init = threading.Thread(target=self.__init_playlist, daemon=True)
        thread_init.start()

        time.sleep(3)

        self.__set_gui()

    def __init_playlist(self):
        playlist = Playlist('https://youtube.com/playlist?list=PLRe9ARNnYSY41I4NXMtfHQ2HN2wap_YtX')
        self.videos = list(playlist.videos)
        random.shuffle(self.videos)

        thread_download = threading.Thread(target=self.__download, daemon=True)
        thread_download.start()

    def __download(self):
        current_video = self.videos[self.current_position]
        
        # res 360p for fast downloading
        try :
            path_file = current_video.streams.filter(res="720p", progressive="True", mime_type="video/mp4").first().download(DIR_TMP_ANIME)

            print('Done downloading, now converting ...')
            self.title_var.set(current_video.title)
            m, s = divmod(current_video.length, 60)
            self.duration_var.set('/ %02d:%02d'%(m, s))
            self.views_var.set(str(current_video.views)+ " views")
            self.publishdate_var.set(current_video.publish_date.strftime("%d %b %Y"))
            self.description_var.set("\n".join(current_video.description.split("\n")[:2]))

            if self.media_player.is_playing():
                self.media_player.stop()

            # remove latest video
            if self.path_video != "":
                print("delete", self.path_video)
                FileManager().delete_file(self.path_video)
                
            self.path_video = path_file

            self.media_player.set_media(self.vlc_instance.media_new(path_file))
            self.start()

            # Download thumbnail
            next_video = self.videos[self.current_position+1]
            img_data = requests.get(next_video.thumbnail_url).content

            with open(DIR_TMP_COVERS+'next_op.jpg', 'wb') as handler:
                handler.write(img_data)

            next = ImageTk.PhotoImage(Image.open(DIR_TMP_COVERS+'next_op.jpg').resize((106, 80)))
            self.minia_next.configure(image=next)
            self.minia_next.image = next
            self.minianext_var.set(next_video.title)
        except :
            print("Erreur")
            self.next_video()
            
    def start(self):
        self.media_player.audio_set_volume(100)
        self.media_player.play()

    def next_video(self, event):
        self.current_position += 1

        thread_download = threading.Thread(target=self.__download, daemon=True)
        thread_download.start()

    def __set_gui(self):
        self.canvas.destroy()

        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(bg="#1e1e1e")

        self.bg_question_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "question_icon.png"))
        self.bg_return_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "icon_left.png"))

        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= self.bg_return_icon, 
                                    command=self.return_searching_frame,
                                    borderwidth=0)
        self.button_back.pack(side="left", fill="y")

        self.video_frame = tk.Frame(self, background="black")
        self.video_frame.pack(fill="both", expand="True", side="top")

        self.no_signal = tk.Label(self.video_frame, 
                                  text="NO SIGNAL",
                                  fg="white", 
                                  bg="black", 
                                  font=('Courier 25 bold'))
        self.no_signal.place(relx=.5, rely=.5, anchor=tk.CENTER)

        self.bottom_video_frame = tk.Frame(self, background="#1e1e1e")
        self.bottom_video_frame.pack(side="top", fill="x")

        s = ttk.Style()
        s.theme_use('default')
        s.configure("red.Horizontal.TProgressbar", 
                    background='#ff3b30',
                    troughcolor="#8e8e93")       
        s.configure("red.Horizontal.TProgressbar", thickness=2)
        self.progressbar = ttk.Progressbar(self.bottom_video_frame,
                                           style="red.Horizontal.TProgressbar", 
                                           orient="horizontal",
                                           mode="determinate", 
                                           maximum=100,
                                           value=0)
        self.progressbar.pack(side="top", fill="x")
        self.command_info = tk.Label(self.bottom_video_frame,
                                    image=self.bg_question_icon,
                                    background="#1e1e1e",
                                    text="Command  ",
                                    compound="right",
                                    foreground="white",
                                    cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.command_info.bind("<Button-1>", self.show_command)
        self.command_info.pack(side="right", padx=(0,10))

        self.frame_time = tk.Frame(self.bottom_video_frame)
        self.frame_time.pack(side="left",padx=(10,0))
        self.timer_var = tk.StringVar()
        self.timer = tk.Label(self.frame_time,
                              text="99:99",
                              background="black",
                              foreground="white",
                              font=("Roboto", 10),
                              textvariable=self.timer_var)
        self.timer.pack(side="left")
        self.duration_var = tk.StringVar()
        self.duration = tk.Label(self.frame_time,
                                 text="99:99",
                                 background="black",
                                 foreground="white",
                                 font=("Roboto", 10),
                                 textvariable=self.duration_var)
        self.duration.pack(side="left")
        
        self.video_info_frame = tk.Frame(self, bg="black", height=5)
        self.video_info_frame.pack(side="top", fill="x")

        self.minianext_var = tk.StringVar()
        self.minia_next = tk.Label(self.video_info_frame, 
                                   height=80, 
                                   width=106,
                                   compound="top",
                                   textvariable=self.minianext_var,
                                   font=("Roboto", 12, "bold"),
                                   background="black",
                                   foreground="white",
                                   wraplength=106)
        self.minia_next.pack(side='right', padx=(0, 20))

        self.frame_description = tk.Frame(self.video_info_frame, background="black")
        self.frame_description.pack(side="left")
        self.title_var = tk.StringVar()
        self.title_video = tk.Label(self.frame_description, 
                                    text="video title",
                                    fg="white",
                                    bg="black",
                                    font=("Roboto", 14, "bold"),
                                    textvariable=self.title_var)
        self.title_video.pack(side="top", fill="x", padx=(10,0))
        self.views_var = tk.StringVar()
        self.views_video = tk.Label(self.frame_description,
                                          text="video views",
                                          fg="white",
                                          bg="black",
                                          font=("Roboto", 10, "bold"),
                                          textvariable=self.views_var)
        self.views_video.pack(side="left", fill="x")
        self.publishdate_var = tk.StringVar()
        self.publishdate_video = tk.Label(self.frame_description,
                                          text="video publishdate",
                                          fg="white",
                                          bg="black",
                                          font=("Roboto", 10, "bold"),
                                          textvariable=self.publishdate_var)
        self.publishdate_video.pack(side="left", fill="x")
        self.description_var = tk.StringVar()
        self.description_video = tk.Label(self.frame_description,
                                          text="video description",
                                          fg="white",
                                          bg="black",
                                          font=("Roboto", 10),
                                          textvariable=self.description_var)
        self.description_video.pack(side="bottom", fill="x")
        
        # define where to display the vlc mediaplayer
        winfo_id = self.video_frame.winfo_id()
        self.media_player.set_hwnd(winfo_id)
        self.update()

    def __set_bindings(self):
        self.app.bind('<space>', lambda event: self.media_player.pause())
        self.app.bind('<Right>', lambda event: self.media_player.set_time(self.media_player.get_time() + 10_000))
        self.app.bind('<Left>', lambda event: self.media_player.set_time(self.media_player.get_time() - 10_000))
        self.app.bind('<Up>', lambda event: self.media_player.audio_set_volume(self.media_player.audio_get_volume() + 5))
        self.app.bind('<Down>', lambda event: self.media_player.audio_set_volume(self.media_player.audio_get_volume() - 5))
        self.app.bind('f', lambda event: self.toogle_fullscreen())
        self.app.bind('m', lambda event: self.toogle_mute())
        self.app.bind('q', lambda event: self.exit())
        self.app.bind('e', lambda event: self.exit())

    def toogle_fullscreen(self):
        self.fullscreen_state = not self.fullscreen_state
        self.app.attributes('-fullscreen', self.fullscreen_state)
    
    def toogle_mute(self):
        self.mute_state = not self.mute_state

    def __on_tick(self):
        seconds = self.media_player.get_time() // 1000

        if self.video_length == 0:
            new_length = self.media_player.get_length() // 1000

            if new_length > 0:
                self.video_length = new_length

        if seconds < 0 or seconds > (2 ** 32):
            seconds = 0
        elif seconds > self.video_length:
            seconds = self.video_length

    def show_command(self, event):
        global pop
        pop = tk.Toplevel(self.app)
        pop.title("Command Videoplayer")
        pop.geometry("250x150")

        pop.config(bg="#1e1e1e")

    def pos_callback(self, event, player):
        # source : https://stackoverflow.com/questions/3595649/vlc-python-eventmanager-callback-type
        sec = player.get_time() / 1000
        m, s = divmod(sec, 60)
        self.progressbar["value"] = int((sec / self.videos[self.current_position].length) * 100)
        self.timer_var.set('%02d:%02d' % (m, s))
        self.update()

    def return_searching_frame(self):
        # delete all covers in tmp dir
        #if self.thread_download_covers.is_alive():
            # kill thread
        #TODO : penser à kill le vlc si l'anime est en cours - appel à la fonction exit()
        if self.media_player.is_playing():
            self.media_player.stop()

        self.parent.show_searching_frame()
        FileManager().delete_tmp_files()