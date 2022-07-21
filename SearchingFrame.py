# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:55:49 2022

@author: Dorian
"""

import os
import random
import pygame

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk


from DbManager import DbManager
from MediaPlayerFrame import MediaPlayerFrame
from FileManager import DIR_IMG_SEARCH

class SearchingFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY = ('Verdana',16)
    FONT_SEARCH_RESULT = ('Verdana', 12)
    
    def __init__(self, parent, data):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.data = data
        
        # Constant
        list_bg_img = os.listdir(DIR_IMG_SEARCH)
        
        # Images
        self.bg_img = ImageTk.PhotoImage(Image.open(DIR_IMG_SEARCH + 
                                                    random.choice(list_bg_img)))
        
        
        # String Variable for Dynamic Labels
        self.var_search = tk.StringVar()
        self.var_search.set("Search a manga")
        self.var_results = tk.StringVar()
        
        # Define all widgets
        self.canvas = tk.Canvas(self, width=1000, height=450, bd=0, relief='ridge')
    
        self.canvas.create_image(0,0, image=self.bg_img , anchor="nw") 
        self.canvas.pack(expand=True, fill="both")
             
        self.search_entry = tk.Entry(self.canvas, 
                                width=40,
                                textvariable=self.var_search,
                                font=self.FONT_SEARCH_ENTRY,
                                highlightthickness=2)
        self.search_entry.bind('<KeyRelease>', self.check_search)
        self.canvas.create_window(500, 200, window=self.search_entry, anchor="center")

        self.search_result = tk.Listbox(self.canvas,
                                   listvariable=self.var_results,
                                   width=40,
                                   font=self.FONT_SEARCH_RESULT,
                                   borderwidth=0,
                                   selectforeground="white",
                                   selectbackground="black" )
        self.search_result.bind("<<ListboxSelect>>", self.redirect)
        
        
        self.canvas_result = self.canvas.create_window(500, 310, 
                                                       window=self.search_result, 
                                                       anchor="center",
                                                       state="hidden")
        
        self.mediaplayer = MediaPlayerFrame(self)
        
        # pack all widgets
        self.mediaplayer.pack(side=tk.BOTTOM, fill=tk.X)
        
    
    def redirect(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            serie = event.widget.get(index)

            db_manager = DbManager("test.db")
            infos = db_manager.get_serie_infos(serie)
         
            self.parent.show_serie_frame(serie, infos)
        else:
            pass
 
    def update_search_result(self, results) :
        # clear listbox
        self.search_result.delete(0, tk.END)
        
        # add result
        self.var_results.set(results)
        
    def check_search(self, event):
        typed = self.search_entry.get()
        
        if typed == '' :
            # hide search results
            self.canvas.itemconfigure(self.canvas_result, state='hidden')
        else :
            db_manager = DbManager("test.db")
            res = db_manager.search_serie(typed)
      
            if len(res)>0 :
                self.update_search_result(res)
                self.canvas.itemconfigure(self.canvas_result, state='normal')
            else :
                self.canvas.itemconfigure(self.canvas_result, state='hidden')
                
            
            db_manager.close()
                
            