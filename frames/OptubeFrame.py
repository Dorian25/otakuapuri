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
import emoji
import yt_dlp

class OptubeFrame(tk.Frame):
    
    def __init__(self, parent, app, vlc_args=[]):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent

        self.app = app 

        self.current_position = 0
        self.path_video = ""

        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(bg="#1e1e1e")

        self.media_player = vlc.MediaPlayer()
        self.media_player.audio_set_volume(100)
        self.event_manager = self.media_player.event_manager()
        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.next_video)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerPositionChanged, self.pos_callback)

        self.video_length = 0
        self.fullscreen_state = False
        self.mute_state = False

        thread_init = threading.Thread(target=self.__init_playlist, daemon=True)
        thread_init.start()

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

        self.after(3000, self.__set_gui) # not  last for more than 3 seconds

    def __init_playlist(self):
        playlist = Playlist('https://youtube.com/playlist?list=PLRe9ARNnYSY41I4NXMtfHQ2HN2wap_YtX')
        self.videos = list(playlist.videos)
        random.shuffle(self.videos)

        thread_download = threading.Thread(target=self.__download_yt_dlp, daemon=True)
        thread_download.start()

    def __download_yt_dlp(self):
        print("launch donwloading")
        current_video = self.videos[self.current_position]
        res = self.resolution_var.get().replace("p","")

        self.dict_info = {}
        
        ydl_opts = {
            'format': f"b[height={res}][ext=mp4]",
            'quiet': True,
            "nopart": True,
            'outtmpl': DIR_TMP_ANIME + "ost_"+str(self.current_position)+".%(ext)s"
        }

        print(self.videos[self.current_position].watch_url)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.dict_info = ydl.extract_info(self.videos[self.current_position].watch_url)
        except yt_dlp.utils.DownloadError:
            print('interrupt the download')
        finally:
            print('Done downloading, now converting ...')

        self.path_video = DIR_TMP_ANIME + "ost_"+str(self.current_position)+".mp4"

        self.title_var.set(self.dict_info["title"])
        m, s = divmod(self.dict_info["duration"], 60)
        self.duration_var.set('/ %02d:%02d'%(m, s))
        self.views_var.set(emoji.emojize(":eye:") + str(self.dict_info["view_count"])+ " views")
        self.publishdate_var.set("Published on " + current_video.publish_date.strftime("%B %d, %Y"))
        self.description_var.set("\n".join(self.dict_info["description"].split("\n")[:2]))

        self.media_player.set_media(vlc.Media(self.path_video))
        self.start(None)

        # Download thumbnail
        next_video = self.videos[self.current_position+1]
        img_data = requests.get(next_video.thumbnail_url).content

        with open(DIR_TMP_COVERS+'next_op.jpg', 'wb') as handler:
            handler.write(img_data)

        next = ImageTk.PhotoImage(Image.open(DIR_TMP_COVERS+'next_op.jpg').resize((86, 60)))
        self.minia_next.configure(image=next)
        self.minia_next.image = next
        #self.minianext_var.set(next_video.title)

    def __download_pytube(self):
        print("launch donwloading")
        current_video = self.videos[self.current_position]
        
        # res 360p for fast downloading
        path_file = current_video.streams.filter(res="360p", progressive="True", mime_type="video/mp4").first().download(DIR_TMP_ANIME)
     
        print('Done downloading, now converting ...')

        self.title_var.set(current_video.title)
        m, s = divmod(current_video.length, 60)
        self.duration_var.set('/ %02d:%02d'%(m, s))
        self.views_var.set(emoji.emojize(":eye:") + str(current_video.views)+ " views")
        self.publishdate_var.set("Published on " + current_video.publish_date.strftime("%B %d, %Y"))
        self.description_var.set("\n".join(current_video.description.split("\n")[:2]))

        self.path_video = path_file

        self.media_player.set_media(self.vlc_instance.media_new(path_file))
        self.start(None)

        # Download thumbnail
        next_video = self.videos[self.current_position+1]
        img_data = requests.get(next_video.thumbnail_url).content

        with open(DIR_TMP_COVERS+'next_op.jpg', 'wb') as handler:
            handler.write(img_data)

        next = ImageTk.PhotoImage(Image.open(DIR_TMP_COVERS+'next_op.jpg').resize((86, 60)))
        self.minia_next.configure(image=next)
        self.minia_next.image = next
        #self.minianext_var.set(next_video.title)
            
    def start(self, event):
        if self.media_player.is_playing():
            self.play_btn.config(image=self.bg_play_icon)
            self.media_player.pause()
        else:
            self.play_btn.config(image=self.bg_pause_icon)
            self.media_player.play()

    def prev_video(self, event):
        if self.current_position == 0:
            self.media_player.stop()
            self.start(None)
        else :
            self.current_position -= 1

    def next_video(self, event):
        self.current_position += 1

        thread_download = threading.Thread(target=self.__download_yt_dlp, daemon=True)
        thread_download.start()

    def __set_gui(self):
        self.canvas.destroy()

        self.bg_question_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "question_icon.png"))
        self.bg_return_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "icon_left.png"))
        self.bg_play_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_play.png"))
        self.bg_pause_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_pause.png"))
        self.bg_next_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_next.png"))
        self.bg_prev_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_prev.png"))
        self.bg_fullscreen_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_fullscreen.png"))
        self.bg_fullscreen_exit_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_fullscreen_exit.png"))

        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= self.bg_return_icon, 
                                    command=self.return_searching_frame,
                                    borderwidth=0,
                                    cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.button_back.pack(side="left", fill="y", expand=False)

        self.video_frame = tk.Frame(self, background="black")
        self.video_frame.pack(side="top", fill="both", expand="True")

        self.no_signal = tk.Label(self.video_frame, 
                                  text="NO SIGNAL",
                                  fg="white", 
                                  bg="black", 
                                  font=('Courier 25 bold'))
        self.no_signal.pack(fill="both", expand="True")

        self.bottom_video_frame = tk.Frame(self, background="#1e1e1e")
        self.bottom_video_frame.pack(side="top", fill="x", expand=False)

        s = ttk.Style()
        s.theme_use('default')
        s.configure("optube.Horizontal.TProgressbar", 
                    background='#ff0000',
                    troughcolor="#8e8e93")       
        s.configure("optube.Horizontal.TProgressbar", thickness=2)
        self.progressbar = ttk.Progressbar(self.bottom_video_frame,
                                           style="optube.Horizontal.TProgressbar", 
                                           orient="horizontal",
                                           mode="determinate", 
                                           maximum=99,
                                           value=0)
        self.progressbar.pack(fill="x")

        self.fullscreen_btn = tk.Label(self.bottom_video_frame,
                                       image=self.bg_fullscreen_icon,
                                       background="#1e1e1e",
                                       cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.fullscreen_btn.bind("<Button-1>", self.toogle_fullscreen)
        self.fullscreen_btn.pack(side="right", padx=(0,10))

        self.resolution_var = tk.StringVar()
        self.resolution_var.set("360p")
        self.resolution_btn = tk.Label(self.bottom_video_frame,
                                       textvariable=self.resolution_var,
                                       fg="white",
                                       font=("Impact", 10),
                                       background="#1e1e1e",
                                       cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.resolution_btn.bind("<Button-1>", self.change_resolution)
        self.resolution_btn.pack(side="right", padx=(0,10))

        self.prev_btn = tk.Label(self.bottom_video_frame,
                                 background="#1e1e1e", 
                                 image=self.bg_prev_icon,
                                 cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.prev_btn.bind("<Button-1>", self.prev_video)
        self.prev_btn.pack(side="left", padx=10)

        self.play_btn = tk.Label(self.bottom_video_frame,
                                 background="#1e1e1e", 
                                 image=self.bg_pause_icon,
                                 cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.play_btn.bind("<Button-1>", self.start)
        self.play_btn.pack(side="left", padx=10)

        self.next_btn = tk.Label(self.bottom_video_frame, 
                                 image=self.bg_next_icon,
                                 background="#1e1e1e",
                                 cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.next_btn.bind("<Button-1>", self.next_video)
        self.next_btn.pack(side="left", padx=10)

        self.frame_time = tk.Frame(self.bottom_video_frame)
        self.frame_time.pack(side="left",padx=(10,0))
        self.timer_var = tk.StringVar()
        self.timer = tk.Label(self.frame_time,
                              text="99:99",
                              background="#1e1e1e",
                              foreground="white",
                              font=("Roboto", 10),
                              textvariable=self.timer_var)
        self.timer.pack(side="left")
        self.duration_var = tk.StringVar()
        self.duration = tk.Label(self.frame_time,
                                 text="99:99",
                                 background="#1e1e1e",
                                 foreground="white",
                                 font=("Roboto", 10),
                                 textvariable=self.duration_var)
        self.duration.pack(side="left")
        
        self.video_info_frame = tk.Frame(self, bg="black", height=5)
        self.video_info_frame.bind("<Enter>", self.enter_video_frame)
        self.video_info_frame.bind("<Leave>", self.leave_video_frame)
        self.video_info_frame.pack(side="top", fill="x", expand=False)

        self.minianext_var = tk.StringVar()
        self.minia_next = tk.Label(self.video_info_frame, 
                                   compound="bottom",
                                   text="NEXT",
                                   font=("Roboto", 10, "bold"),
                                   background="black",
                                   foreground="white",
                                   wraplength=106)
        self.minia_next.pack(side='right', padx=(0, 20), fill="both")

        self.frame_description = tk.Frame(self.video_info_frame, background="black")
        self.frame_description.pack(side="left")
        self.title_var = tk.StringVar()
        self.title_var.set("Video Title")
        self.title_video = tk.Label(self.frame_description, 
                                    text="video title",
                                    fg="white",
                                    bg="black",
                                    font=("Roboto", 14, "bold"),
                                    textvariable=self.title_var)
        self.title_video.pack(side="top", fill="x", padx=(10,0))

        self.frame_views_date = tk.Frame(self.frame_description, background="black")
        self.frame_views_date.pack(padx=(50, 0), side="top", fill="x")

        self.views_var = tk.StringVar()
        self.views_var.set("999999 views")
        self.views_video = tk.Label(self.frame_views_date,
                                          text="video views",
                                          fg="white",
                                          bg="black",
                                          font=("Roboto", 10, "bold"),
                                          textvariable=self.views_var)
        self.views_video.pack(side="left")
        self.publishdate_var = tk.StringVar()
        self.publishdate_var.set("Published on April 20, 2023")
        self.publishdate_video = tk.Label(self.frame_views_date,
                                          text="video publishdate",
                                          fg="white",
                                          bg="black",
                                          font=("Roboto", 10, "bold"),
                                          textvariable=self.publishdate_var)
        self.publishdate_video.pack(side="left", padx=(20, 0))

        self.description_var = tk.StringVar()
        self.description_var.set("Video Description")
        self.description_video = tk.Label(self.frame_description,
                                          text="video description",
                                          fg="white",
                                          bg="#1e1e1e",
                                          justify="left",
                                          font=("Roboto", 10),
                                          textvariable=self.description_var)
        self.description_video.pack(side="top", fill="x", expand=False)
        
        # define where to display the vlc mediaplayer
        winfo_id = self.video_frame.winfo_id()
        self.media_player.set_hwnd(winfo_id)
        self.update()

        self.__set_bindings()
        self.__on_tick()

    def change_resolution(self, event):
        current_rest = self.resolution_var.get()

        if current_rest == "360p":
            self.resolution_var.set("720p")
        elif current_rest == "720p":
            self.resolution_var.set("360p")

    def __set_bindings(self):
        self.app.bind('<space>', lambda event: self.media_player.pause())
        self.app.bind('<Right>', lambda event: self.media_player.set_time(self.media_player.get_time() + 10_000))
        self.app.bind('<Left>', lambda event: self.media_player.set_time(self.media_player.get_time() - 10_000))
        self.app.bind('<Up>', lambda event: self.media_player.audio_set_volume(self.media_player.audio_get_volume() + 5))
        self.app.bind('<Down>', lambda event: self.media_player.audio_set_volume(self.media_player.audio_get_volume() - 5))
        self.app.bind('f', lambda event: self.toogle_fullscreen(None))
        self.app.bind('m', lambda event: self.toogle_mute())
    
    def unset_bindings(self):
        self.app.unbind('<space>')
        self.app.unbind('<Right>')
        self.app.unbind('<Left>')
        self.app.unbind('<Up>')
        self.app.unbind('<Down>')
        self.app.unbind('f')
        self.app.unbind('m')

    def toogle_fullscreen(self, event):
        self.fullscreen_state = not self.fullscreen_state
        if self.fullscreen_state:
            self.fullscreen_btn.config(image=self.bg_fullscreen_exit_icon)
        else :
            self.fullscreen_btn.config(image=self.bg_fullscreen_icon)
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

    def pos_callback(self, event):
        # source : https://stackoverflow.com/questions/3595649/vlc-python-eventmanager-callback-type
        sec = self.media_player.get_time() / 1000
        m, s = divmod(sec, 60)
        self.progressbar["value"] = int((sec / self.dict_info["duration"]) * 100)
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

    def quit(self):
        if self.media_player.is_playing():
            self.media_player.stop()

    def enter_video_frame(self, event):
        self.bottom_video_frame.pack_forget()

    def leave_video_frame(self, event):
        self.bottom_video_frame.pack(side="top", fill="x", after=self.video_frame)
        