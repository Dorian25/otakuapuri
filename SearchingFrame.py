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

from DbManager import MongoDBManager
from MediaPlayerFrame import MediaPlayerFrame
from FileManager import DIR_IMG_SEARCH, DIR_IMG_ICON
from CustomListBox import CustomListBox

class SearchingFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY=('Verdana',16)
    FONT_SEARCH_ENTRY_PLACEHOLDER =('Verdana',16,'italic')
    FONT_SEARCH_RESULT=('Verdana', 12)
    
    COLOR_SEARCH_ENTRY_PLACEHOLDER="#c7c7cc"
    COLOR_SEARCH_ENTRY="#000"
    
    CHARTS_URL="https://charts.mongodb.com/charts-getmanga-rhtkb/public/dashboards/632df18e-f274-4d69-899d-21740a3f593f"
    
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.mongodb_manager = MongoDBManager()
        
        # Images
        list_bg_img = os.listdir(DIR_IMG_SEARCH)
        self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_SEARCH + 
                                                    random.choice(list_bg_img)))
        self.bg_button_top100 = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON +
                                                              "icon_top100_64.png"))
        self.bg_button_random = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON +
                                                              "mystery_box_64.png"))
        self.bg_button_charts = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON +
                                                              "mongodb_charts_64.png"))
        
        # String Variable for Dynamic Labels
        self.var_search = tk.StringVar()
        self.var_results = tk.StringVar()
        
        # Define all widgets
        self.canvas = tk.Canvas(self, 
                                width=1000, 
                                height=450, 
                                bd=0, 
                                highlightthickness=0,
                                relief='ridge')
        self.canvas.create_image(0,0, image=self.bg_img , anchor="nw") 
        self.canvas.pack(expand=True, fill="both")
             
        self.search_entry = tk.Entry(self.canvas, 
                                     width=40,
                                     textvariable=self.var_search)
        self.search_entry.bind('<KeyRelease>', self.check_search)
        self.search_entry.bind('<KeyPress>', self.onKeyPress)
        self.search_entry.bind("<FocusIn>", self.focus_in_entry)
        self.search_entry.bind("<FocusOut>", self.focus_out_entry)
        self.canvas.create_window(500, 200, window=self.search_entry, anchor="center")
        self.set_placeholder()

        self.search_result = CustomListBox(self.canvas,
                                   listvariable=self.var_results,
                                   width=52,
                                   font=self.FONT_SEARCH_RESULT,
                                   borderwidth=0,
                                   selectforeground="white",
                                   selectbackground="black")
        self.search_result.bind("<<ListboxSelect>>", self.redirect_serie_frame)
        self.canvas_result = self.canvas.create_window(500, 313, 
                                                       window=self.search_result, 
                                                       anchor="center",
                                                       state="hidden")
        
        self.top100_button = self.canvas.create_image(940, 70, image=self.bg_button_top100)
        self.canvas.tag_bind(self.top100_button, "<Button-1>", self.redirect_malranking_frame)
        self.random_button = self.canvas.create_image(940, 150, image=self.bg_button_random)
        self.canvas.tag_bind(self.random_button, "<Button-1>", self.redirect_random_serie)
        self.charts_button = self.canvas.create_image(940, 230, image=self.bg_button_charts)
        self.canvas.tag_bind(self.charts_button, "<Button-1>", self.redirect_charts)
        
        # mediaplayer
        self.mediaplayer = MediaPlayerFrame(self)
        self.mediaplayer.pack(side=tk.BOTTOM, fill=tk.X)
        
    def focus_in_entry(self, event):
        self.search_entry.configure(highlightbackground="#007aff", 
                                    highlightcolor="#007aff",
                                    highlightthickness=2)
        
        if self.var_search.get() == "Search a manga":
            self.search_entry.delete('0', 'end')
            self.search_entry.config(font=self.FONT_SEARCH_ENTRY)
            self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY)
        
    def focus_out_entry(self, event):
        print("out")
        self.search_entry.config(highlightthickness=0)
        if self.search_entry.get() == "":
            self.set_placeholder()
            
    def redirect_malranking_frame(self, event):
        self.parent.show_malranking_frame()
        
    def redirect_random_serie(self, event):
        random_serie = random.choice(self.parent.series_available)
        serie_obj = self.mongodb_manager.get_serie_infos(random_serie)
        
        self.parent.show_serie_frame(serie_obj)
        
    def set_placeholder(self):
        self.search_entry.insert(0, "Search a manga")
        self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY_PLACEHOLDER)
        self.search_entry.config(font=self.FONT_SEARCH_ENTRY_PLACEHOLDER)
        
    def set_default_style(self):
        self.search_entry.config(font=self.FONT_SEARCH_ENTRY)
        self.search_entry.config(fg=self.COLOR_SEARCH_ENTRY)

    def redirect_charts(self, event):
        webbrowser.open(self.CHARTS_URL)

        
    def redirect_serie_frame(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            titre_serie = event.widget.get(index)
            serie_obj = self.mongodb_manager.get_serie_infos(titre_serie)
         
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

        if typed == '' :
            # hide search results
            self.canvas.itemconfigure(self.canvas_result, state='hidden')
            self.set_placeholder()
            self.search_entry.icursor(0)
        elif typed == 'Search a manga':
            pass
        else :
            pattern = "^"+typed
            res = [s for s in self.parent.series_available if re.match(pattern, s, re.IGNORECASE)]
      
            if len(res)>0 :
                self.update_search_result(res)
                self.canvas.itemconfigure(self.canvas_result, state='normal')
            else :
                self.canvas.itemconfigure(self.canvas_result, state='hidden')