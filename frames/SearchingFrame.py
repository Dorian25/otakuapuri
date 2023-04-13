# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:55:49 2022

@author: Dorian
"""

import os
import re
import random
import pygame
import webbrowser

import tkinter as tk


from PIL import Image, ImageTk

from utils.DbManager import MongoDBManager
from frames.MediaPlayerFrame import MusicVLCPlayerFrame
from utils.InfoBulle import InfoBulle
from utils.FileManager import DIR_IMG_SEARCH, DIR_IMG_ICON
from utils.CustomListBox import CustomListBox

class SearchingFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY=('Verdana',16)
    FONT_SEARCH_ENTRY_PLACEHOLDER =('Verdana',16,'italic')
    FONT_SEARCH_RESULT=('Verdana', 16)
    
    COLOR_SEARCH_ENTRY_PLACEHOLDER="#c7c7cc"
    COLOR_SEARCH_ENTRY="#000"
    
    CHARTS_URL="https://charts.mongodb.com/charts-getmanga-rhtkb/public/dashboards/632df18e-f274-4d69-899d-21740a3f593f"
    
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        # Images
        list_bg_img = os.listdir(DIR_IMG_SEARCH)
        self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_SEARCH + 
                                                    random.choice(list_bg_img)))
        self.bg_button_top100 = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "icon_top100_64.png"))
        self.bg_button_random = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "mystery_box_64.png"))
        self.bg_button_charts = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "mongodb_charts_64.png"))
        self.bg_button_optube = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "optube_64.png"))
        self.bg_button_downloader = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "downloader_64.png"))
        self.bg_logo = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "otakuapuri.png"))
        self.bg_search_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "search_icon.png"))
        self.bg_fr_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "french_flag.png"))
        self.bg_en_icon = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "english_flag.png"))
        
        # String Variable for Dynamic Labels
        self.var_search = tk.StringVar()
        self.var_results = tk.StringVar()
        self.var_source = tk.StringVar()
        self.var_source.set("FR")
        
        # Define all widgets
        self.scrollable_app = tk.Frame(self, background="#1e1e1e")
        self.scrollable_app.pack(side=tk.LEFT, fill="both", expand=True)
        self.top100_button = tk.Label(self.scrollable_app, 
                                      image=self.bg_button_top100, 
                                      background="#1e1e1e",
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        #self.infobulle_top100 = InfoBulle(self.top100_button, "Show the MAL rank")
        self.top100_button.pack(side="top", pady=(15,5))
        self.top100_button.bind("<Button-1>", self.redirect_malranking_frame)

        self.random_button = tk.Label(self.scrollable_app, 
                                      image=self.bg_button_random, 
                                      background="#1e1e1e", 
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        #self.infobulle_random = InfoBulle(self.random_button, "Show a random manga")
        self.random_button.pack(side="top", pady=5)
        self.random_button.bind("<Button-1>", self.redirect_random_serie)

        self.charts_button = tk.Label(self.scrollable_app, 
                                      image=self.bg_button_charts, 
                                      background="#1e1e1e", 
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.charts_button.pack(side="top", pady=5)
        self.charts_button.bind("<Button-1>", self.redirect_charts)
        #self.infobulle_charts = InfoBulle(self.charts_button, "Show more infos on website source")

        self.optube_button = tk.Label(self.scrollable_app, 
                                      image=self.bg_button_optube, 
                                      background="#1e1e1e", 
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.optube_button.pack(side="top", pady=5)
        self.optube_button.bind("<Button-1>", self.redirect_optube_frame)
        #self.infobulle_optube = InfoBulle(self.optube_button, "Watch the best Opening Anime")

        self.downloader_button = tk.Label(self.scrollable_app, 
                                          image=self.bg_button_downloader, 
                                          background="#1e1e1e", 
                                          cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.downloader_button.pack(side="top", pady=5)
        self.downloader_button.bind("<Button-1>", self.redirect_downloader_frame)

        self.canvas = tk.Canvas(self, 
                                width=1000, 
                                height=500, 
                                bd=0, 
                                highlightthickness=0,
                                relief='ridge')
        self.canvas.create_image(0,0, image=self.bg_img , anchor="nw") 
        self.canvas.pack(side=tk.TOP, expand=True, fill="both")

        
        self.frame_entry = tk.Frame(self.canvas, 
                                    borderwidth=5,
                                    background="white", 
                                    relief=tk.RAISED)
        self.search_icon = tk.Label(self.frame_entry, 
                                    image=self.bg_search_icon, 
                                    background="#fff")
        self.search_icon.pack(side=tk.LEFT)
        self.language_icon = tk.Label(self.frame_entry,
                                      image=self.bg_fr_icon,
                                      background="#fff",
                                      cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.language_icon.bind("<Button-1>", self.choose_language)
        self.language_icon.pack(side=tk.RIGHT, padx=(0,10))

        self.search_entry = tk.Entry(self.frame_entry, 
                                     width=40,
                                     relief=tk.FLAT,
                                     borderwidth=10,
                                     textvariable=self.var_search)
        self.search_entry.bind('<KeyRelease>', self.check_search)
        self.search_entry.bind('<KeyPress>', self.onKeyPress)
        self.search_entry.bind("<FocusIn>", self.focus_in_entry)
        self.search_entry.bind("<FocusOut>", self.focus_out_entry)
        self.search_entry.pack()
        self.canvas.create_window(500, 250, window=self.frame_entry, anchor="center")
        self.set_placeholder()

        self.search_result = CustomListBox(self.canvas,
                                           listvariable=self.var_results,
                                           width=48,
                                           height=7,
                                           selectmode=tk.BROWSE,
                                           font=self.FONT_SEARCH_RESULT,
                                           borderwidth=0,
                                           selectforeground="white",
                                           selectbackground="black")
        self.search_result.bind("<<ListboxSelect>>", self.redirect_serie_frame)
        self.canvas_result = self.canvas.create_window(500, 370, 
                                                       window=self.search_result, 
                                                       anchor="center",
                                                       state="hidden")
        
        self.logo = self.canvas.create_image(500,150, image=self.bg_logo) 

        # mediaplayer
        self.mediaplayer = MusicVLCPlayerFrame(self)
        self.mediaplayer.pack(side=tk.BOTTOM, fill=tk.X)

    def select_source(self):
        self.search_entry.delete(0, tk.END)
        self.set_placeholder()

    def focus_in_entry(self, event):
        if self.var_search.get() == "Search a manga":
            self.search_entry.delete('0', 'end')
            self.search_entry.config(font=self.FONT_SEARCH_ENTRY)
            self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY)
        
    def focus_out_entry(self, event):
        self.search_entry.config(highlightthickness=0)
        if self.search_entry.get() == "":
            self.set_placeholder()
            
    def redirect_malranking_frame(self, event):
        pygame.quit()
        self.parent.show_malranking_frame()

    def redirect_optube_frame(self, event):
        pygame.quit()
        self.parent.show_optube_frame()

    def redirect_downloader_frame(self, event):
        pygame.quit()
        #self.parent.show_downloader_frame()

    def choose_language(self, event):
        if self.var_source.get() == 'EN':
            self.var_source.set('FR')
            self.language_icon.config(image=self.bg_fr_icon)
        else :
            self.var_source.set('EN')
            self.language_icon.config(image=self.bg_en_icon)
        print("change language")
    
    def redirect_random_serie(self, event):
        pygame.quit()
        random_serie = None
        serie_obj = None
        if self.var_source.get() == "FR":
            random_serie = random.choice(self.parent.series_available_sushiscan)
            serie_obj = MongoDBManager.get_serie_infos_pymongo(self.parent.mongoclient, 
                                                               random_serie, 
                                                               "sushiscan")
        else :
            random_serie = random.choice(self.parent.series_available_manganato)
            serie_obj = MongoDBManager.get_serie_infos_pymongo(self.parent.mongoclient, 
                                                               random_serie, 
                                                               "manganato")
        
        self.parent.show_serie_frame(serie_obj)
        
    def set_placeholder(self):
        self.search_entry.insert(0, "Search a manga")
        self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY_PLACEHOLDER)
        self.search_entry.config(font=self.FONT_SEARCH_ENTRY_PLACEHOLDER)
        self.search_entry.icursor(0)
        
    def set_default_style(self):
        self.search_entry.config(font=self.FONT_SEARCH_ENTRY)
        self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY)

    def redirect_charts(self, event):
        webbrowser.open(self.CHARTS_URL)

    def redirect_serie_frame(self, event):
        pygame.quit()
        selection = event.widget.curselection()
        serie_obj = None
        if selection:
            index = selection[0]
            titre_serie = event.widget.get(index)
            if self.var_source.get() == "FR":
                serie_obj = MongoDBManager.get_serie_infos_pymongo(self.parent.mongoclient, 
                                                                   titre_serie, 
                                                                   "sushiscan")
            else :
                serie_obj = MongoDBManager.get_serie_infos_pymongo(self.parent.mongoclient, 
                                                                   titre_serie, 
                                                                   "manganato")
         
            self.parent.show_serie_frame(serie_obj)
        else:
            pass
 
    def update_search_result(self, results) :
        # clear listbox
        self.search_result.delete(0, tk.END)
        # add result
        self.var_results.set(results)
        
    def onKeyPress(self, event):
        typed = self.search_entry.get()
        
        if "Search a manga" in typed :
            typed = typed.replace("Search a manga","")
            self.var_search.set(typed)
            self.set_default_style()
        
    def check_search(self, event):
        typed = self.search_entry.get()
        res = []

        if typed == '' :
            # hide search results
            self.canvas.itemconfigure(self.canvas_result, state='hidden')
            self.set_placeholder()
        elif typed == "Search a manga":
            pass
        else :
            pattern = "^"+typed
            if self.var_source.get() == "FR":
                res = [s for s in self.parent.series_available_sushiscan if re.match(pattern, s, re.IGNORECASE)]
            else :
                res = [s for s in self.parent.series_available_manganato if re.match(pattern, s, re.IGNORECASE)]
            
            if len(res)>0 :
                self.update_search_result(res)
                self.canvas.itemconfigure(self.canvas_result, state='normal')
            else :
                self.canvas.itemconfigure(self.canvas_result, state='hidden')