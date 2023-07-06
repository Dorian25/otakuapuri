import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.FileManager import DIR_IMG_ICON, DIR_IMG_HTML, DIR_TMP_ANIME
from utils.utils import extract_real_url
import threading
import youtube_dl
import logging
import os
from tkwebview2.tkwebview2 import WebView2
from tkinter import filedialog
from tkinter import messagebox

class VideoPlayerFrame(tk.Frame):
    # source = https://gitlab.com/SafwanLjd/PyTkinterVLC/-/blob/master/tkvlc/__init__.py
    def __init__(self, parent, vo, vf, app, serieframe, p_bar):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.app = app
        self.serieframe = serieframe

        self.images = []  # to hold the newly created image

        self.p_bar = p_bar
        
        self.vo = vo
        self.vf = vf
        
        self.fullscreen_state = False
        self.cancelled = False
        self.download_state = False

        self.__set_gui()

    def __set_gui(self):
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(bg="#1e1e1e")

        # webview
        # Opening the html file
        html_file = open(DIR_IMG_HTML + "nosignal.html", "r")
        # Reading the file
        html_content = html_file.read()
        self.webview_frame = WebView2(self, 300, 100, background="black")
        self.webview_frame.load_html(html_content)
        self.webview_frame.pack(side='bottom', fill='both', expand=True)

        self.bg_fr_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "french_flag.png"))
        self.bg_jap_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "japan_flag.png"))
        self.bg_download_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "icon_download.png"))

        self.fullscreen_var = tk.StringVar()
        self.fullscreen_var.set("ON") if self.fullscreen_state else self.fullscreen_var.set("OFF") 
        self.fullscreen_value = tk.Label(self,
                                         background="#1e1e1e",
                                         textvariable=self.fullscreen_var,
                                         foreground="red",
                                         font=("Helvetica", 10, "bold"),
                                         cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.fullscreen_value.bind("<Button-1>", self.toogle_fullscreen)
        self.fullscreen_value.pack(side="right", anchor="e", padx=(0,10))

        self.fullscreen_label = tk.Label(self,
                                         background="#1e1e1e",
                                         text="Fullscreen",
                                         compound="right",
                                         font=("Helvetica", 10, "bold"),
                                         foreground="white")
        self.fullscreen_label.pack(side="right", anchor="e", padx=(0,10))

        self.vf_icon = tk.Label(self,
                                image=self.bg_fr_icon,
                                background="#1e1e1e",
                                text="VF",
                                compound="left",
                                foreground="#1e1e1e",
                                cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.vf_icon.bind("<Button-1>", self.onChangeLanguage)
        if self.vf :
            self.vf_icon.pack(side="left", anchor="n", padx=(10,0))

        self.vostfr_icon = tk.Label(self,
                                    image=self.bg_jap_icon,
                                    background="#1e1e1e",
                                    foreground="#1e1e1e",
                                    text="VO",
                                    compound="left",
                                    cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.vostfr_icon.bind("<Button-1>", self.onChangeLanguage)
        if self.vo:
            self.vostfr_icon.pack(side="left",anchor="n")
        
        self.var_version = tk.StringVar()
        self.var_season = tk.StringVar()
        self.var_episode = tk.StringVar()
        self.var_episode_link = tk.StringVar()

        self.seasons_selector = ttk.Combobox(self, 
                                             height=30, 
                                             width=30, 
                                             textvariable=self.var_season)
        self.seasons_selector.bind('<<ComboboxSelected>>', self.onChangeSeason)
        self.seasons_selector.set("Choose a season")
        if self.vo and not self.vf:
            self.var_version.set("VO")
            self.seasons_selector['state'] = 'readonly'
            self.seasons_selector['values'] = list(self.vo.keys())
        elif self.vf and not self.vo:
            self.var_version.set("VF")
            self.seasons_selector['state'] = 'readonly'
            self.seasons_selector['values'] = list(self.vf.keys())
        else :
            self.seasons_selector['state'] = 'disable'
            
        self.seasons_selector.pack(side="left",anchor="n", padx=(0,20), pady=(10,0))

        self.episodes_selector = ttk.Combobox(self, 
                                             height=30, 
                                             width=30, 
                                             textvariable=self.var_episode)
        self.episodes_selector.bind('<<ComboboxSelected>>', self.onChangeEpisode)
        self.episodes_selector['state'] = 'disable'
        self.episodes_selector.set("Choose an episode")
        self.episodes_selector.pack(side="left",anchor="n", padx=(0,20), pady=(10,0))

        self.download_icon = tk.Label(self,
                                      image=self.bg_download_icon,
                                      background="#1e1e1e",
                                      text=" Download",
                                      compound="left",
                                      font=("Helvetica", 10, "bold"),
                                      foreground="white",
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.download_icon.bind("<Button-1>", self.onClickDownload)
        self.download_icon.pack(side="left", anchor="n", padx=(10,0))

    def onChangeEpisode(self, event):
        if self.var_version.get() == "VF":
            self.var_episode_link.set(self.vf[self.var_season.get()][self.var_episode.get()])
        else :
            self.var_episode_link.set(self.vo[self.var_season.get()][self.var_episode.get()])
        
        self.load_video_webview(self.var_episode_link.get())
    
    def onChangeSeason(self, event):
        if self.var_version.get() == "VF":
            self.episodes_selector['state'] = 'readonly'
            self.episodes_selector['values'] = list(self.vf[self.var_season.get()].keys())
        else :
            self.episodes_selector['state'] = 'readonly'
            self.episodes_selector['values'] = list(self.vo[self.var_season.get()].keys())

    def onChangeLanguage(self, event):
        version = event.widget.cget("text")

        if version == self.var_version.get():
            return 

        self.var_version.set(version)

        self.seasons_selector['state'] = 'readonly'

        if version == "VF":
            self.seasons_selector['values'] = list(self.vf.keys())  
        else :
            self.seasons_selector['values'] = list(self.vo.keys())
           
        self.seasons_selector.set("Choose a season")

        self.episodes_selector['state'] = 'disable'
        self.episodes_selector.set("Choose an episode")

    def toogle_fullscreen(self, event):
        self.fullscreen_state = not self.fullscreen_state
        self.fullscreen_value.config(foreground="green") if self.fullscreen_state else self.fullscreen_value.config(foreground="red")
        self.fullscreen_var.set("ON") if self.fullscreen_state else self.fullscreen_var.set("OFF")
        self.app.attributes('-fullscreen', self.fullscreen_state)

    def load_video_webview(self, video_url):
        self.webview_frame.load_url(video_url)

    def load_video(self, video_url):
        """ loads the video """
        
        self.p_bar.config(maximum=100)

        self.download_state = True

        # Download Video
        thread_download_video = threading.Thread(target=self.__download, args=[video_url], daemon=True)
        thread_download_video.start()

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
            self.download_state = False
            self.serieframe.hide_progressbar()
        elif d['status'] == 'downloading' :
            if self.cancelled:
                raise youtube_dl.utils.DownloadError('Download cancelled by user')
            else : 
                percentage = float(d['_percent_str'].strip().replace("%",""))
                self.p_bar["value"] = percentage
                self.serieframe.s.configure("red.Horizontal.TProgressbar", 
                                            foreground='white', 
                                            text="Downloading:      {0}/{1}/{2}      ({3}%)      ".format(self.var_version.get(), self.var_season.get(), self.var_episode.get(), percentage))
                 
                self.parent.update()


    def __download(self, video_url):
        self.serieframe.show_progressbar()

        # créer un objet logger pour les sorties
        logger = logging.getLogger('youtube_dl')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(DIR_TMP_ANIME + 'youtube-dl.log', 'w', 'utf-8')
        logger.addHandler(handler)

        ydl_opts = {
            'progress_hooks': [self.my_hook],
            'quiet': True,
            'logger': logger,
            "nopart": True,
            'outtmpl': self.mp4_path
        }
        
        # tweaks 
        if "myvi" in video_url:
            video_url = extract_real_url(video_url)

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except youtube_dl.utils.DownloadError:
            print('interrupt the download')
        finally:
            print('end of download')
            self.download_state = False
            self.cancelled = False
            # remove handler
            logger.removeHandler(handler)
            # Fermer le handler du logger
            handler.close()

            #logging.shutdown()
            
            #self.serieframe.hide_progressbar()
            os.remove(DIR_TMP_ANIME + 'youtube-dl.log')

    def stop(self, quit=False):
        print("QUIT", quit)

        if self.download_state: 
            print("Downloading ok")
            self.cancelled = True
            
        if not quit:
            print("no quit")
            self.reset_video_frame()
            self.serieframe.hide_progressbar()

    def reset_video_frame(self):
        self.webview_frame.load_html('<div style="width:100%"><div style="height:0;padding-bottom:56.25%;position:relative;width:100%"><iframe allowfullscreen="" frameBorder="0" height="100%" src="https://giphy.com/embed/vboZVH1oDiLdctj4V3/video" style="left:0;position:absolute;top:0" width="100%"></iframe></div></div>')

    def onClickDownload(self, event):
        print("var_episode", self.var_episode.get())
        if not self.download_state :
            if self.var_episode.get() != "Choose an episode":
                if messagebox.askyesno("Download","Download this episode ?") :
                    self.download_state = True
                    
                    self.mp4_path = filedialog.asksaveasfilename(title="Where do you want to save the episode ?",
                                                            filetypes=[("Mp4 files",".mp4")],
                                                            initialfile="anime_" + self.var_version.get().lower().replace(" ", "_") + "_" + self.var_season.get().lower().replace(" ", "_") + "_" + self.var_episode.get().lower().replace(" ", "_"),
                                                            defaultextension='.mp4')
                    
                    if self.mp4_path.endswith(".mp4"):
                        print("var_episode_link", self.var_episode_link.get())
                        t1 = threading.Thread(target=self.load_video, args=(self.var_episode_link.get(),), daemon=True)
                        t1.start()
                    else :
                        messagebox.showerror("Error","Please specify a filename that ends with '.mp4'")
                        self.download_state = False
                else :
                    self.download_state = False
            else:
                messagebox.showerror("Error", "Please choose an episode to download")
        else:
            messagebox.showerror("Error", "Wait until your download finish")