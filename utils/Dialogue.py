# Import the required libraries
from PIL import Image, ImageTk
import time
from utils.FileManager import DIR_MUSIC, DIR_IMG_ICON
from utils.Sound import Sound
from utils.utils import talk_to
from threading import Thread
import emoji

import tkinter as tk

class Dialogue(tk.Toplevel):
    def __init__(self, app, charactername, characterimg, title_series):
        tk.Toplevel.__init__(self)

        #self.configure("backgroud")
        #self.title("Calling "  + charactername + " ...")
        #self.iconbitmap(DIR_IMG_ICON + 'icon.ico')
        #self.wm_transient(app)
        self.overrideredirect(True)
        self.configure(bg="#81b7a7")
        #self.resizable(False, False)
        #self.wm_attributes('-alpha', 1)
        #self.update_idletasks()

        self.app = app
        self.charactername = charactername
        self.characterimg_path = characterimg
        self.characterimg = ""
        self.title_series = title_series

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

        self.gif = Image.open(r'images/loading/codec_mgs.gif')
        self.frame_count = self.gif.n_frames
        self.play_back_delay = 50
        self.frames_gif = [None] * self.frame_count
        self.stop_gif = False
        self._job_gif = None

        #self.__set_gui()
        #self.__set_gui_call()
        self.__set_gui_selector()
        #thread_download_dialogue = Thread(target=self.download_dialogue, daemon=True)
        #thread_download_dialogue.start()
        
        # Call the function to start updating the Toplevel window position
        self.update_position()

    def __set_gui_selector(self):
        n_row = 2
        n_col = 5

        values = {0: {0: emoji.emojize(":disappointed_face: Regrets"), 
                      1: emoji.emojize(":dart: Goals"), 
                      2: emoji.emojize(":shuffle_tracks_button: Choices"), 
                      3: emoji.emojize(":gem_stone: Values"), 
                      4: emoji.emojize(":world_map: Adventure")},
                  1: {0: emoji.emojize(":seedling: Evolution"), 
                      1: emoji.emojize(":pensive_face: Remorse"), 
                      2: emoji.emojize(":family_man_woman_girl_boy: Relationships"), 
                      3: emoji.emojize(":artist_palette: Hobbies"), 
                      4: emoji.emojize(":light_bulb: Advice")}}

        frame_global = tk.Frame(self, background="#1b463e")
        frame_global.pack(padx=1, pady=1, ipadx=5, ipady=10, expand=True, fill="both")

        for i in range(n_row):
            for j in range(n_col):
                frame_conv_type = tk.Frame(frame_global, background="#81b7a7")
                label_conv_type = tk.Label(frame_conv_type, text=values[i][j], bg="#1b463e", fg="#81b7a7", bd=0, font=("Courier", 14))
                frame_conv_type.grid(row=i, column=j, padx=5, pady=5)
                label_conv_type.pack(padx=1, pady=1, ipadx=3, ipady=3)


    def __set_gui_call(self):
        self.sound.loop_sound('call')
        # widgets
        self.label_gif = tk.Label(self, background="#1b463e")
        self.label_gif.pack(expand=True, fill="both")

        self.load_gif()
        self.update_gif(0)
        
        
    def load_gif(self):
        for x in range(self.frame_count):
            frame = ImageTk.PhotoImage(self.gif.copy())
            self.frames_gif[x] = frame
            self.gif.seek(x)


    def update_gif(self, ind):
        if not self.stop_gif:
            # source : https://stackoverflow.com/questions/67704455/tkinter-gif-animation-falters-and-is-pixelated
            frame = self.frames_gif[ind]
            self.label_gif.configure(image=frame)
            
            ind += 1
            if ind == self.frame_count:
                ind = 0

            self._job_gif = self.after(self.play_back_delay, self.update_gif, ind)

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

    def download_dialogue(self):
        msg, dialogue = talk_to(self.charactername, self.title_series)

        self.cancel_gif()
        self.sound.stop_sound('call')

        self.reset()
        
        self.sentences = iter(dialogue.split("\n\n"))
        self.next_sentence(None)
   

    def __set_gui_dialogue(self):
        # Create a Label in the toplevel widget
        image = Image.open(self.characterimg_path)
        image_resize = image.resize((100, 140))
        self.characterimg = ImageTk.PhotoImage(image_resize)
        image = tk.Label(self, text="image", image=self.characterimg, background="#81b7a7") 
        image.pack(side="left")

        self.canvas = tk.Canvas(self, background="#1b463e")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_text = self.canvas.create_text(10, 
                                                   10, 
                                                   text='', 
                                                   anchor=tk.NW, 
                                                   fill="#81b7a7", 
                                                   font=("Courier", 13, "bold"), 
                                                   width=500)
        self.__set_bindings()

    def __set_bindings(self):
        self.bind("<Button-1>", self.next_sentence)
        self.bind("<Enter>", lambda event: self.check_hand_enter())
        self.bind("<Leave>", lambda event: self.check_hand_leave())


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
            self.canvas.itemconfig(self.canvas_text, text="")
            for i in range(1, len(self.current_sentence.strip()) + 1):
                s = self.current_sentence[:i]

                self.canvas.after(delay, self.update_text, s)

                delay += delta
        else :
            self.destroy()

    def update_text(self, s): 
        #source = https://golen.nu/portal/phoenix/ 
        odd = False

        fast = 0.06
        slow = 0.09
        speed = fast

        letter = s[-1]
        self.canvas.itemconfigure(self.canvas_text, text=s)
        
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

    # Function to update the Toplevel window position
    def update_position(self):
        x = int(self.app.winfo_x() + self.app.winfo_width() * 0.26)
        y = int(self.app.winfo_y() + self.app.winfo_height() + 35)
        self.geometry(f'740x150+{x}+{y}')

        # Update the Toplevel window position every 100 milliseconds
        self.after(5, self.update_position)

    def close(self):
        pass

    def reset(self):
        # Supprimer tous les widgets enfants de la video_frame
        for child in self.winfo_children():
            child.destroy()

        self.__set_gui_dialogue()

    def cancel_gif(self):
        self.stop_gif = True
        print(self._job_gif)
        if self._job_gif is not None:
            self.after_cancel(self._job_gif)
            self._job_gif = None









  








