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
    
    def __init__(self, parent, app):
        tk.Frame.__init__(self, parent)
        self.config(bg="white")
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.current_page_allmanga = 0
        self.current_page_topmanga = 0
        self.current_page_popularmanga = 0
        
        self.parent = parent
        self.app = app
        self.covers_img = []

        image_leftbutton = ImageTk.PhotoImage(Image.open("images/icons/icon_left.png"))
        image_mallogo = ImageTk.PhotoImage(Image.open("images/icons/myanimelist_logo.png"))

        self.covers_img.append(image_leftbutton)
        self.covers_img.append(image_mallogo)

        self.mal_logo = tk.Label(self,
                                 background="white",
                                 image=image_mallogo, 
                                 borderwidth=0)
        self.mal_logo.pack(side="top")

        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= image_leftbutton, 
                                    command=self.return_searching_frame,
                                    borderwidth=0)
        self.button_back.pack(side="left", fill="y")
        
        self.nav_bar = ttk.Notebook(self)
        self.nav_bar.bind('<<NotebookTabChanged>>',self.onchangetab)
        
        self.tab1 = TreeviewMALFrame(self.nav_bar, which="All Manga", app=self.app)
        self.tab2 = TreeviewMALFrame(self.nav_bar, which="Top Manga", app=self.app)
        self.tab3 = TreeviewMALFrame(self.nav_bar, which="Most Popular", app=self.app)
        
        self.nav_bar.add(self.tab1, text="All Manga")
        self.nav_bar.add(self.tab2, text="Top Manga")
        self.nav_bar.add(self.tab3, text="Most Popular")

        self.nav_bar.pack(side="top", expand=True, fill="both", padx=30, pady=30)

        self.frame_pagination = tk.Frame(self, 
                                         background="white",
                                         borderwidth=0)
        self.frame_pagination.pack(side="bottom")
        
        self.button_next_50 = tk.Button(self.frame_pagination,
                                        background="#4f74c8",
                                        foreground="white",
                                        text= "Next 50 >", 
                                        command=self.next_50,
                                        borderwidth=0)
        self.button_next_50.pack(side="right", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)

        self.button_prev_50 = tk.Button(self.frame_pagination,
                                        background="#4f74c8",
                                        foreground="white",
                                        text= "< Prev 50", 
                                        command=self.prev_50,
                                        borderwidth=0)

    def onchangetab(self, event):
        current_tab = self.nav_bar.tab(self.nav_bar.select(), "text")

        if current_tab == "All Manga":
            if self.current_page_allmanga == 0 and self.button_prev_50.winfo_exists():
                self.button_prev_50.pack_forget()
            else :
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)
        elif current_tab == "Top Manga":
            if self.current_page_topmanga == 0 and self.button_prev_50.winfo_exists():
                self.button_prev_50.pack_forget()
            else :
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)
        else:
            if self.current_page_popularmanga == 0 and self.button_prev_50.winfo_exists():
                self.button_prev_50.pack_forget()
            else :
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)


    def next_50(self):
        current_tab = self.nav_bar.tab(self.nav_bar.select(), "text")

        if current_tab == "All Manga":
            self.current_page_allmanga += 1
            t1 = threading.Thread(target=self.tab1.fill_treeview_next, args=[self.current_page_allmanga])
            t1.start()

            if self.current_page_allmanga == 1:
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)

        elif current_tab == "Top Manga":
            self.current_page_topmanga += 1
            t1 = threading.Thread(target=self.tab2.fill_treeview_next, args=[self.current_page_topmanga])
            t1.start()

            if self.current_page_topmanga == 1:
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)
        else :
            self.current_page_popularmanga += 1
            t1 = threading.Thread(target=self.tab3.fill_treeview_next, args=[self.current_page_popularmanga])
            t1.start()

            if self.current_page_popularmanga == 1:
                self.button_prev_50.pack(side="left", anchor="center", padx=5, pady=10, ipadx=10, ipady=10)

    def prev_50(self):
        current_tab = self.nav_bar.tab(self.nav_bar.select(), "text")
        
        if current_tab == "All Manga":
            self.current_page_allmanga -= 1
            t1 = threading.Thread(target=self.tab1.fill_treeview_next, args=[self.current_page_allmanga])
            t1.start()

            if self.current_page_allmanga == 0:
                self.button_prev_50.pack_forget()

        elif current_tab == "Top Manga":
            self.current_page_topmanga -= 1
            t1 = threading.Thread(target=self.tab2.fill_treeview_next, args=[self.current_page_topmanga])
            t1.start()

            if self.current_page_topmanga == 0:
                self.button_prev_50.pack_forget()
        else :
            self.current_page_popularmanga -= 1
            t1 = threading.Thread(target=self.tab3.fill_treeview_next, args=[self.current_page_popularmanga])
            t1.start()

            if self.current_page_popularmanga == 0:
                self.button_prev_50.pack_forget()


    def return_searching_frame(self):
        self.parent.show_searching_frame()