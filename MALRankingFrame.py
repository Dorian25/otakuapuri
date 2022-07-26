# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 12:44:24 2022

@author: Dorian
"""

import os
import random

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk

from DbManager import DbManager
from FileManager import DIR_IMG_SEARCH, DIR_IMG_ICON
from AllMangaFrame import AllMangaFrame

class MALRankingFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY = ('Verdana',16)
    FONT_SEARCH_RESULT = ('Verdana', 12)
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.config(bg="#2e51a2")
        
        self.parent = parent
        
        
        self.nav_bar = ttk.Notebook(self)
        
        self.tab1 = AllMangaFrame(self.nav_bar)
        self.tab2 = tk.Frame(self.nav_bar)
        self.tab3 = tk.Frame(self.nav_bar)
        
        self.nav_bar.add(self.tab1, text="All Manga")
        self.nav_bar.add(self.tab2, text="Top Manga")
        self.nav_bar.add(self.tab3, text="Most Popular")
        
        
        
        self.back_button = tk.Button(self, 
                                     text="Back", 
                                     bd=0,
                                     highlightthickness=0,
                                     relief='ridge',
                                     command=self.return_searching_frame)
        
        self.back_button.pack(side="top")
        self.nav_bar.pack(side="top", expand=True, fill="both", padx=30, pady=30)
        
        
    def return_searching_frame(self):
        # delete all covers in tmp dir
        self.parent.show_searching_frame(None)
       
        
        """
        self.top100 = self.get_top100()
        
        
        
        
        
        
        self.treeview = ttk.Treeview(root, 
                                     columns=self.COLUMNS,
                                     show='headings')
        
        self.scrollbarx = tk.Scrollbar(TableMargin, orient=tk.HORIZONTAL)
        self.scrollbary = tk.Scrollbar(TableMargin, orient=tk.VERTICAL)
        tree = ttk.Treeview(TableMargin, columns=("rank", "title", "score"), 
                            yscrollcommand=scrollbary.set, 
                            xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarx.config(command=self.treeview.xview)
        scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.treeview.heading('rank', text="Rank", anchor=tk.W)
        self.treeview.heading('title', text="Title", anchor=tk.W)
        self.treeview.heading('score', text="Score", anchor=tk.W)
        
        
        self.treeview.column('#0', stretch=tk.NO, minwidth=0, width=0)
        self.treeview.column('#1', stretch=tk.NO, minwidth=0, width=200)
        self.treeview.column('#2', stretch=tk.NO, minwidth=0, width=200)
        self.treeview.column('#3', stretch=tk.NO, minwidth=0, width=300)
        
        tree.pack()
        
    
            """