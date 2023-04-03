# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 12:44:24 2022

@author: Dorian
"""


import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from utils.FileManager import DIR_IMG_SEARCH, DIR_IMG_ICON
from frames.TreeviewMALFrame import TreeviewMALFrame
import threading

class MALRankingFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY = ('Verdana',16)
    FONT_SEARCH_RESULT = ('Verdana', 12)
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.config(bg="white")
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.parent = parent
        self.covers_img = []

        image = Image.open("images\icons\icon_left.png")
        tk_image_button = ImageTk.PhotoImage(image)
        self.covers_img.append(tk_image_button)
        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= tk_image_button, 
                                    command=self.return_searching_frame,
                                    borderwidth=0)
        self.button_back.pack(side="left", fill="y")
        
        self.nav_bar = ttk.Notebook(self)
        
        self.tab1 = TreeviewMALFrame(self.nav_bar, which="All Manga")
        self.tab2 = TreeviewMALFrame(self.nav_bar, which="Top Manga")
        self.tab3 = TreeviewMALFrame(self.nav_bar, which="Most Popular")
        
        self.nav_bar.add(self.tab1, text="All Manga")
        self.nav_bar.add(self.tab2, text="Top Manga")
        self.nav_bar.add(self.tab3, text="Most Popular")

        self.nav_bar.pack(side="top", expand=True, fill="both", padx=30, pady=30)
        
        self.button_next_50 = tk.Button(self,
                                        background="#4f74c8",
                                        foreground="white",
                                        text= "Next 50 >", 
                                        command=self.next_50,
                                        borderwidth=0)
        self.button_next_50.pack(side="bottom", pady=10, ipadx=10, ipady=10)
        


    def next_50(self):
        current_tab = self.nav_bar.tab(self.nav_bar.select(), "text")
        
        if current_tab == "All Manga":
            t1 = threading.Thread(target=self.tab1.fill_treeview_next)
            t1.start()
        elif current_tab == "Top Manga":
            t1 = threading.Thread(target=self.tab2.fill_treeview_next)
            t1.start()
        else :
            t1 = threading.Thread(target=self.tab3.fill_treeview_next)
            t1.start()



    def return_searching_frame(self):
        # delete all covers in tmp dir
        self.parent.show_searching_frame()