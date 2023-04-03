import tkinter as tk
from tkinter import ttk
import vlc
from PIL import Image, ImageTk
from utils.FileManager import DIR_IMG_ICON, DIR_TMP_ANIME
from utils.utils import extract_real_url
import threading
import yt_dlp
import youtube_dl
import io
import time

class VideoPlayerFrame(tk.Frame):
    # source = https://gitlab.com/SafwanLjd/PyTkinterVLC/-/blob/master/tkvlc/__init__.py
    def __init__(self, parent, vo, vf, app, serieframe, p_bar, vlc_args=[]):
        # vlc_args=['--file-caching=10000','--network-caching=10000','--live-caching=10000']
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.app = app
        self.serieframe = serieframe
        
        self.images = []  # to hold the newly created image

        self.p_bar = p_bar
        self.buffer = io.BytesIO()
        
        self.vo = vo
        self.vf = vf
        
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        self.video_length = 0
        self.fullscreen_state = False
        self.mute_state = False

        self.__set_gui()
        self.__set_bindings()
        self.__on_tick()


    def __set_gui(self):
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(bg="#1e1e1e")

        self.video_frame = tk.Frame(self, background="black")
        self.video_frame.pack(fill="both", expand="True", side="bottom")

        #self.overlay = tk.Canvas(self, background="black")
        #self.overlay.pack()
        #self.create_overlay(50, 50, 250, 150, fill='grey', alpha=.5)
        #self.create_overlay(80, 80, 150, 120, fill='#800000', alpha=.8)

        self.no_signal = tk.Label(self.video_frame, text="NO SIGNAL", fg="white", bg="black", font=('Courier 25 bold'))
        self.no_signal.place(relx=.5, rely=.5, anchor=tk.CENTER)

        self.bg_fr_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "french_flag.png"))
        self.bg_jap_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "japan_flag.png"))
        self.bg_question_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "question_icon.png"))


        self.command_info = tk.Label(self,
                                     image=self.bg_question_icon,
                                     background="#1e1e1e",
                                     text="Command  ",
                                     compound="right",
                                     foreground="white",
                                     cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.command_info.bind("<Button-1>", self.show_command)
        self.command_info.pack(side="right", anchor="e", padx=(0,10))

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
        self.episodes_selector.pack(side="left",anchor="n", pady=(10,0))

        winfo_id = self.video_frame.winfo_id()

        self.media_player.set_hwnd(winfo_id)
        self.update()

    def onChangeEpisode(self, event):
        # EPISODE 1
        numero_episode = int(self.var_episode.get().split(" ")[1]) - 1

        if self.var_version.get() == "VF":
            self.var_episode_link.set(self.vf[self.var_season.get()][numero_episode][self.var_episode.get()])
        else :
            self.var_episode_link.set(self.vo[self.var_season.get()][numero_episode][self.var_episode.get()])

        self.load_video(self.var_episode_link.get())
    
    def onChangeSeason(self, event):
        if self.var_version.get() == "VF":
            self.episodes_selector['state'] = 'readonly'
            self.episodes_selector['values'] = [list(episode.keys())[0] for episode in self.vf[self.var_season.get()]]
        else :
            self.episodes_selector['state'] = 'readonly'
            self.episodes_selector['values'] = [list(episode.keys())[0] for episode in self.vo[self.var_season.get()]]

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

    def toogle_fullscreen(self):
        self.fullscreen_state = not self.fullscreen_state
        self.app.attributes('-fullscreen', self.fullscreen_state)
    
    def toogle_mute(self):
        self.mute_state = not self.mute_state
        self.media_player.audio_set_mute(self.mute_state)

    def load_video(self, video_url):
        """ loads the video """
        
        self.p_bar.config(maximum=100)

        # Download Video
        thread_download_video = threading.Thread(target=self.__download, args=[video_url], daemon=True)
        thread_download_video.start()

        # Stream Video
        #thread_download_video = threading.Thread(target=self.__stream, args=[video_url], daemon=True)
        #thread_download_video.start()

        #self.start_streaming()

    def my_hook(self, d):
        
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
            self.media_player.set_media(self.vlc_instance.media_new(d["filename"]))
            self.start()
            
            self.serieframe.hide_progressbar()
        elif d['status'] == 'downloading' :
            percentage = int((d['downloaded_bytes'] / d['total_bytes']) * 100)
            # on lance la lecture de la vidéo à partir de 10%
            if percentage == 5 and not self.media_player.is_playing():
                self.media_player.set_media(self.vlc_instance.media_new(d["filename"]+".part"))
                self.start()
            self.p_bar["value"] = percentage
            self.serieframe.s.configure("red.Horizontal.TProgressbar", foreground='white', text="Téléchargement: {0} %      ".format(percentage))
            self.parent.update()


    def __download(self, video_url):
        self.serieframe.show_progressbar()

        ydl_opts = {
            'progress_hooks': [self.my_hook],
            'quiet': False, 
            'outtmpl': DIR_TMP_ANIME + "%(title)s.%(ext)s"
        }
        
        # tweaks 
        if "myvi" in video_url:
            video_url = extract_real_url(video_url)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    def __stream(self, video_url):
        ydl_opts = {
            'outtmpl': '-',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with ydl.download([video_url]) as f:
                while True:
                    # Lire les données depuis le fichier téléchargé
                    data = f.read(1024)
                    if not data:
                        break
                    # Écrire les données dans le tampon
                    self.buffer.write(data)
                    # Attendre un peu pour permettre au lecteur VLC de lire les données
                    time.sleep(0.1)


    def start(self):
        self.media_player.audio_set_volume(100)
        self.media_player.play()

    def exit(self):
        self.media_player.stop()
        self.destroy()

    def is_playing(self):
        return self.media_player.is_playing()
    
    def pause(self):
        return self.media_player.pause()

    def create_overlay(self, x1, y1, x2, y2, **kwargs):

        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.overlay.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.overlay.create_rectangle(x1, y1, x2, y2, **kwargs)

    def show_command(self, event):
        global pop
        pop = tk.Toplevel(self.app)
        pop.title("Command Videoplayer")
        pop.geometry("250x250")

        pop.config(bg="#1e1e1e")

        command_f = tk.Label(pop, text="< F > ---> Enter/Exit Fullscreen Mode", fg="white", bg="#1e1e1e", anchor="w")
        command_f.pack(side="top")
        command_m = tk.Label(pop, text="< M > ---> Mute/Unmute", fg="white", bg="#1e1e1e", anchor="w")
        command_m.pack(side="top")
        command_q = tk.Label(pop, text="< Q > ---> Exit", fg="white", bg="#1e1e1e", anchor="w")
        command_q.pack(side="top")
        command_e = tk.Label(pop, text="< E > ---> Exit", fg="white", bg="#1e1e1e", anchor="w")
        command_e.pack(side="top")
        command_space = tk.Label(pop, text="< SPACE > ---> Play/Pause", fg="white", bg="#1e1e1e", anchor="w")
        command_space.pack(side="top")
        command_right = tk.Label(pop, text="< -> > ---> Skip forward", fg="white", bg="#1e1e1e", anchor="w")
        command_right.pack(side="top")
        command_left = tk.Label(pop, text="< <- > --> Skip backward", fg="white", bg="#1e1e1e", anchor="w")
        command_left.pack(side="top")
        command_up = tk.Label(pop, text="< ^ > ---> Turn Volume Up", fg="white", bg="#1e1e1e", anchor="w")
        command_up.pack(side="top")
        command_down = tk.Label(pop, text="< v > ---> Turn Down Volume", fg="white", bg="#1e1e1e", anchor="w")
        command_down.pack(side="top")
        