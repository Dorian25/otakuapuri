# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 09:47:12 2022

@author: Dorian
"""

import os
import img2pdf
import webbrowser
import time
import random
import urllib.request
import threading
from PIL import Image, ImageTk
import pygame
import datetime
currentTime = datetime.datetime.now()

#Import the Tkinter library
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from utils import *

# source useful
#threading - https://pythonassets.com/posts/background-tasks-with-tk-tkinter/
#yt playlist - https://youtube.com/playlist?list=PLcCQJuPwyya3uxri7ZCiDDjMwaaVXz7DK
#music player - https://www.studytonight.com/tkinter/music-player-application-using-tkinter


# App Parameters
app = tk.Tk()
app.geometry("1000x500")
app.resizable(False, False)
app.iconbitmap('./icon/icon.ico')
app.title('Download Manga')
app.grid()

# Init pygame mixer
pygame.init()
pygame.mixer.init()


# Constant
columns = ("Titre", "Statut", "Type", "Année de Sortie","Auteur","Posté le","Mis à jour le")
playlist = os.listdir("music")
background_home = os.listdir("image/home")
background_mediaplayer = os.listdir("image/mediaplayer")
num_piste = 0

# Images
image = Image.open('image/home/'+random.choice(background_home))
image_playbutton = Image.open('icon/icon_play.png')
image_prevbutton = Image.open('icon/icon_previous.png')
image_nextbutton = Image.open('icon/icon_next.png')
image_sakura = Image.open('image/mediaplayer/background_mediaplayer_sunnight.jpg')

# 
bg = ImageTk.PhotoImage(image)
bg_playbutton = ImageTk.PhotoImage(image_playbutton)
bg_nextbutton = ImageTk.PhotoImage(image_nextbutton)
bg_prevbutton = ImageTk.PhotoImage(image_prevbutton)
bg_mediaplayer = ImageTk.PhotoImage(image_sakura)

# String Variable for Dynamic Labels
var_status_mp = tk.StringVar()
var_track_mp = tk.StringVar()
if currentTime.hour < 12:
    var_track_mp.set("Good Morning ! You can listen to " + str(len(playlist)) + " songs !")
elif 12 <= currentTime.hour < 18:
    var_track_mp.set("Good Afternoon ! You can listen to " + str(len(playlist)) + " songs !")
else:
    var_track_mp.set("Good Evening ! You can listen to " + str(len(playlist)) + " songs !")



def play_song() :  
    if var_status_mp.get() == "play" :
        pygame.mixer.music.pause()
        var_status_mp.set("pause")
        var_track_mp.set("|| Paused")
    elif var_status_mp.get() == "pause" :
        pygame.mixer.music.unpause()
        var_status_mp.set("play")
        var_track_mp.set("You're listening to : "+playlist[num_piste]) 
    else :
        var_track_mp.set("You're listening to : "+playlist[num_piste])      
        pygame.mixer.music.load("music/"+playlist[num_piste])
        pygame.mixer.music.play()
        var_status_mp.set("play")
    
def next_song() :
    if var_status_mp.get() == "play" :
        global num_piste
        if num_piste == (len(playlist)-1) :
            num_piste = 0
        else :
            num_piste += 1
        
        var_track_mp.set("You're listening to "+playlist[num_piste]) 
        pygame.mixer.music.load("music/"+playlist[num_piste])
        pygame.mixer.music.play()
    
    
def prev_song() :
    if var_status_mp.get() == "play" :
        global num_piste 
        if num_piste == 0 :
            num_piste = len(playlist)-1
        else :
            num_piste -= 1
        
        var_track_mp.set("You're listening to "+playlist[num_piste]) 
        pygame.mixer.music.load("music/"+playlist[num_piste])
        pygame.mixer.music.play()

def welcome() :
    messagebox.showinfo("Welcome Otaku", "Welcome to the jungle !")
    var_status_mp.set("MP3 Player is ready !")

def get_all_elements_downloading() :
    checkbox = []

    total_tome = 17
    n_col = 5
    n_row = total_tome // n_col
    n_col_rest = total_tome - (n_row*n_col)
    print(n_col)
    print(n_row)
    print(n_col_rest)

    for i in range(n_row) :
        for j in range(n_col) :
            checkbox.append(tk.Checkbutton(labelFrameCheckbox, text='tome'+str(i+1)).grid(row=i,column=j))

    for j in range(n_col_rest):
        checkbox.append(tk.Checkbutton(labelFrameCheckbox, text='tome'+str(i+1)).grid(row=n_row,column=j))

def onDoubleclick(event):
    item = treeview.selection()[0]
    showinfo("you clicked on", treeview.item(item,"text"))


def update_treeview_worker():
    all_mangas = get_all_mangas()
    for row in get_all_mangas_infos(all_mangas):
        treeview.insert('', tk.END, values=row)


def schedule_check(t):
    """
    Schedule the execution of the `check_if_done()` function after
    one second.
    """
    app.after(1000, check_if_done, t)


def check_if_done(t):
    # If the thread has finished, re-enable the button and show a message.
    if not t.is_alive():
        info_label["text"] = "File successfully downloaded!"
        refresh_button["state"] = "normal"
    else:
        # Otherwise check again after one second.
        schedule_check(t)


def refresh_treeview():
    info_label["text"] = "Loading elements..."
    # Disable the button while downloading the file.
    refresh_button["state"] = "disabled"
    # Start the download in a new thread.
    t = threading.Thread(target=refresh_worker)
    t.start()
    # Start checking periodically if the thread has finished.
    schedule_check(t)

    
    
# Define all widgets
label = tk.Label(app, image=bg, borderwidth=0)


treeview = ttk.Treeview(app, columns=columns, show="headings")
treeview.bind("<Double-1>", onDoubleclick)
treeview.heading('Titre',text="Titre")
treeview.heading('Statut',text="Statut")
treeview.heading('Type',text="Type")
treeview.heading('Année de Sortie',text="Année")
treeview.heading('Auteur',text="Auteur")

#info_label = tk.Label(text="Click the button to download the file.")
#refresh_button = tk.Button(text="Get Mangas", command=refresh_treeview)


labelFrameCheckbox = tk.LabelFrame(app, text="What you can download :", borderwidth=0)



## BOTTOM FRAME
bottom_frame = tk.Frame(app, borderwidth=0)

background_image_label = tk.Label(bottom_frame, 
                                   image=bg_mediaplayer, 
                                   textvariable=var_track_mp, 
                                   font="Courier 12 italic bold",
                                   fg="#fff",
                                   compound="center",
                                   borderwidth=0)

button_previous = tk.Button(bottom_frame, image=bg_prevbutton, command=prev_song, borderwidth=0)
button_play = tk.Button(bottom_frame, image=bg_playbutton, command=play_song, borderwidth=0)
button_next = tk.Button(bottom_frame, image=bg_nextbutton, command=next_song, borderwidth=0)


# Place all widgets

#treeview.pack(padx=50, pady=40, side=tk.TOP)
#refresh_button.pack()
#info_label.pack()
#labelFrameCheckbox.pack(fill="both", expand="yes", padx = 50, pady=5)
label.place(x=0, y=0, relwidth=1, relheight=1)

bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
background_image_label.place(x=0, y=0, relwidth=1, relheight=1)
button_previous.pack(side=tk.LEFT)
button_play.pack(side=tk.LEFT)
button_next.pack(side=tk.LEFT)




#app.after(10000, is_connected)
welcome()
app.mainloop()
pygame.quit()