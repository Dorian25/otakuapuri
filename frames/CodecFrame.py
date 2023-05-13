# Import the required libraries
from PIL import Image, ImageTk
import time
from utils.FileManager import DIR_MUSIC, DIR_IMG_ICON, DIR_IMG_LOAD
from utils.Sound import Sound
from utils.utils import talk_to
from threading import Thread
import emoji

import tkinter as tk

class CodecFrame(tk.Frame):
    # color
    # #1b463e : foncé
    # #81b7a7 : clair
    def __init__(self, parent, characters, title_series):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#1b463e")

        self.parent = parent

        self.characters = characters
        self.title_series = title_series

        self.cursor = 0
        self.is_talking = False
        self.is_running = False

        self.sound = Sound()
        #self.sound.load_sound('song', DIR_MUSIC + 'music_dialogue.ogg')
        #self.sound.set_volume('song', 0.8)
        #self.sound.loop_sound('song')
        self.sound.load_sound('call', DIR_MUSIC + 'call_sound.mp3')
        self.sound.set_volume('call', 0.8)
        
        self.sound.load_sound('blip', DIR_MUSIC + 'sfx-blipmale.wav')
        self.sound.set_volume('blip', 0.5)

        self.sentences = None
        self.current_sentence = ""

        self.codec_gif = Image.open(r'images/loading/codec_199x329.gif')
        self.snake_gif = Image.open(r'images/loading/snake_199x116.gif')
      
        self.frames_codec_gif = [None] * self.codec_gif.n_frames
        self.frames_snake_gif = [None] * self.snake_gif.n_frames

        self.play_back_delay_codec = 50
        self.play_back_delay_snake = {0: 80, 1: 5000, 2: 80, 3: 100 }

        self.width_img = 0


    def set_gui(self):
        self.is_running = True
        
        self.frame_global = tk.Frame(self, background="#1b463e")
        #self.frame_global.pack(padx=20, pady=20, expand=True)
        self.frame_global.place(relx=0.14, y=20)

        self.border_top = tk.Frame(self.frame_global, background="#81b7a7")
        self.border_top.pack(side="top", expand=True)
        # top
        self.frame_top = tk.Frame(self.border_top, background="#1b463e")
        self.frame_top.pack(padx=1, pady=1, fill="both", expand=True)

        self.frame_img_left = tk.Frame(self.frame_top, background="#1b463e")
        self.frame_img_left.pack(side="left", padx=10)
        self.label_img_left = tk.Label(self.frame_img_left, width=0, background="#1b463e")
        self.label_img_left.pack()
        image_l = Image.open(DIR_IMG_ICON + "icon_left_arrow.png")
        self.tk_image_button_l = ImageTk.PhotoImage(image_l)
        self.button_arrow_left = tk.Button(self.frame_top, 
                                           background="#1b463e",
                                           image=self.tk_image_button_l, 
                                           command=self.prev_character,
                                           borderwidth=0)
        self.button_arrow_left.pack(side="left")

        self.label_codec_gif = tk.Label(self.frame_top, background="#1b463e")
        self.label_codec_gif.pack(side="left", expand=True, fill="both")
        self.load_gif() # both gif are loaded
        # update_gif(self, ind, frames_gif, label_gif, play_back_delay)
        self.update_gif(0, self.frames_codec_gif, self.label_codec_gif, self.play_back_delay_codec)

        image_r = Image.open(DIR_IMG_ICON + "icon_right_arrow.png")
        self.tk_image_button_r = ImageTk.PhotoImage(image_r)
        self.button_arrow_right = tk.Button(self.frame_top,
                                            background="#1b463e",
                                            image=self.tk_image_button_r, 
                                            command=self.next_character,
                                            borderwidth=0)
        self.button_arrow_right.pack(side="left")
        
        self.frame_img_right = tk.Frame(self.frame_top, background="#1b463e")
        self.frame_img_right.pack(side="left", padx=10)
        self.label_img_right = tk.Label(self.frame_img_right, width=0, background="#1b463e")
        self.label_img_right.pack() 
        
        self.expand_size_img()
        self.sound.play_sound("call")

        self.update_image_left()
        self.update_gif(0, self.frames_snake_gif, self.label_img_right, self.play_back_delay_snake)

        # bottom
        self.frame_bottom = tk.Frame(self.frame_global, background="#81b7a7", height=204)
        self.frame_bottom.pack(side="bottom", fill="x", pady=(30,0))

        self.__set_gui_selector()

    def __set_gui_selector(self):
        n_row = 3
        n_col = 4

        values = {0: {0: emoji.emojize(":disappointed_face: Regrets"), 
                      1: emoji.emojize(":bullseye: Goals"),  
                      2: emoji.emojize(":gem_stone: Values"), 
                      3: emoji.emojize(":world_map: Adventure")},
                  1: {0: emoji.emojize(":seedling: Evolution"), 
                      1: emoji.emojize(":pensive_face: Remorse"),  
                      2: emoji.emojize(":artist_palette: Hobbies"), 
                      3: emoji.emojize(":light_bulb: Advice")},
                  2: {0: emoji.emojize(":shuffle_tracks_button: Choices"), 
                      1: emoji.emojize(":family_man_woman_girl_boy: Relationships"),
                      2: "",
                      3: ""}}

        frame_global = tk.Frame(self.frame_bottom, background="#163832")
        frame_global.pack(padx=1, pady=1, expand=True, fill="both")

        for i in range(n_row):
            for j in range(n_col):
                if values[i][j]:
                    frame_conv_type = tk.Frame(frame_global, background="#81b7a7")
                    label_conv_type = tk.Label(frame_conv_type, 
                                               text=values[i][j], 
                                               bg="#1b463e", 
                                               fg="#81b7a7", 
                                               bd=0, 
                                               font=("Courier", 13),
                                               cursor="@"+DIR_IMG_ICON+"aero_link.cur")
                    label_conv_type.bind("<Button-1>", self.onClickTopic)
                    frame_conv_type.grid(row=i, column=j, padx=5, pady=5)
                    label_conv_type.pack(padx=1, pady=1, ipadx=3, ipady=3)


    def __set_gui_call(self):
        self.sound.loop_sound('call')
        # widgets
        self.label_gif = tk.Label(self, background="#1b463e")
        self.label_gif.pack(expand=True, fill="both")

        self.load_gif()
        self.update_gif(0)

    def onClickTopic(self, event):
        self.is_talking = True

        theme = event.widget.cget("text").split(" ")[1]

        print(theme)

        name = self.characters[self.cursor]["name"]

        thread_download_dialogue = Thread(target=self.download_dialogue, args=(name, theme), daemon=True)
        thread_download_dialogue.start()

    def load_gif(self):
        for x in range(self.codec_gif.n_frames):
            frame = ImageTk.PhotoImage(self.codec_gif.copy())
            self.frames_codec_gif[x] = frame
            self.codec_gif.seek(x)

        for x in range(self.snake_gif.n_frames):
            frame = ImageTk.PhotoImage(self.snake_gif.copy())
            self.frames_snake_gif[x] = frame
            self.snake_gif.seek(x)


    def update_gif(self, ind, frames_gif, label_gif, play_back_delay):
        # source : https://stackoverflow.com/questions/67704455/tkinter-gif-animation-falters-and-is-pixelated
        frame = frames_gif[ind]
        label_gif.configure(image=frame)
        
        ind += 1
        if ind == len(frames_gif):
            ind = 0

        if type(play_back_delay) is dict:
            self._job_gif = self.after(play_back_delay[ind], self.update_gif, ind, frames_gif, label_gif, play_back_delay)
        else:
            self._job_gif = self.after(play_back_delay, self.update_gif, ind, frames_gif, label_gif, play_back_delay)

    """
    def update_gif(self, ind):
        # source : https://stackoverflow.com/questions/28518072/play-animations-in-gif-with-tkinter
        ind += 1

        if ind == self.frame_count:
            ind = 0   
        else:
            frame = tk.PhotoImage(file=DIR_IMG_LOAD +'codec_mgs.gif', format='gif -index %i' % (ind))
            self.frames_gif[ind] = frame
            self.label_gif.configure(image=frame)

            self.after(50, self.update_gif, ind) 
    """

    def download_dialogue(self, charactername, theme):
        msg, dialogue = talk_to(charactername, self.title_series, theme)

        #self.cancel_gif()
        self.sound.stop_sound('call')

        self.reset()
        self.__set_gui_dialogue()
        
        self.sentences = iter(dialogue.split("\n\n"))
        self.next_sentence(None)
   

    def __set_gui_dialogue(self):
        self.frame_dialogue = tk.Frame(self.frame_bottom, background="#163832")
        self.frame_dialogue.pack(padx=1, pady=1, expand=True, fill="both")

        self.label_dialogue = tk.Label(self.frame_dialogue, 
                                       background="#163832", 
                                       fg="white", 
                                       font=('Helvetica',13), 
                                       text="",
                                       wraplength=600,
                                       cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.label_dialogue.pack(fill="both")

        self.__set_bindings()

    def __set_bindings(self):
        self.label_dialogue.bind("<Button-1>", self.next_sentence)


    def next_sentence(self, event):
        # I_t_? s_o_u_n_d_s_? l_i_k_e_ h_e_ w_a_n_t_s_? t_o_? d_i_e_._._._
        # ..._  ..._..._..._  ..._..._..._  ..._..._  ..._  ..._..._..._
        # 1 3 3 2 1 3
        
        #Time delay between chars, in milliseconds
        delta = 50 
        delay = 0

        # https://stackoverflow.com/questions/1966591/has-next-in-python-iterators
        self.current_sentence = next(self.sentences, None)

        if self.current_sentence:
            self.label_dialogue.config(text="")
            for i in range(1, len(self.current_sentence.strip()) + 1):
                s = self.current_sentence[:i]

                self.label_dialogue.after(delay, self.update_text, s)

                delay += delta
        else :
            self.reset()
            self.is_talking = False
            self.__set_gui_selector()

    def update_text(self, s): 
        #source = https://golen.nu/portal/phoenix/ 
        odd = False

        fast = 0.06
        slow = 0.09
        speed = fast

        letter = s[-1]
        self.label_dialogue.config(text=s)
        
        odd = not odd
        if letter not in ' |#$%':
            if odd:
                self.sound.play_sound('blip')
        else:
            if not odd:
                time.sleep(speed/2)
            odd = False
        time.sleep(speed/2)

    def check_hand_enter(self):
        self.config(cursor="hand1")

    def check_hand_leave(self):
        self.config(cursor="")

    def reset(self):
        # Supprimer tous les widgets enfants de la video_frame
        for child in self.frame_bottom.winfo_children():
            child.destroy()

    def next_character(self):
        if not self.is_talking:
            self.cursor += 1

            if self.cursor == len(self.characters):
                self.cursor = 0

            self.update_image_left()

            #thread_download_dialogue = Thread(target=self.download_dialogue, daemon=True)
            #thread_download_dialogue.start()
        

    def prev_character(self):
        if not self.is_talking:
            self.cursor -= 1
            
            if self.cursor == -1:
                self.cursor = len(self.characters) - 1

            self.update_image_left()

            #thread_download_dialogue = Thread(target=self.download_dialogue, daemon=True)
            #thread_download_dialogue.start()

    def update_image_left(self):
        image_character = Image.open(self.characters[self.cursor]["path_image"])
        image_resize = image_character.resize((116, 199))
        #self.label_img_left.config(width=image_resize.width)
        self.tk_image_character = ImageTk.PhotoImage(image_resize)
        self.label_img_left.config(image=self.tk_image_character)

    def update_image_right(self):
        image_snake = Image.open(DIR_IMG_LOAD+"snake.gif")
        print(image_snake.width, image_snake.height)
        image_resize = image_snake.resize((116, 199))
        self.label_img_right.config(width=image_resize.width)
        self.tk_image_snake = ImageTk.PhotoImage(image_resize)
        self.label_img_right.config(image=self.tk_image_snake)

    def expand_size_img(self):
        if self.width_img < 100:
            self.label_img_left.config(width=self.width_img)
            self.label_img_right.config(width=self.width_img)
            self.width_img += 1
            self.after(15, self.expand_size_img)
            