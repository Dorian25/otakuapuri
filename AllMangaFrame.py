# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 19:06:58 2022

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

from DbManager import SQLiteManager
from FileManager import DIR_DOC
from utils import *

import threading

class AllMangaFrame(tk.Frame):
    
    FONT_SEARCH_ENTRY = ('Verdana',16)
    FONT_SEARCH_RESULT = ('Verdana', 12)
    COLUMNS = ('rank','title','score')
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        
        self.scrollbarx = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbary = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.treeview = ttk.Treeview(self, 
                            columns=self.COLUMNS,
                            selectmode='browse',
                            show='headings', 
                            yscrollcommand=self.scrollbary.set, 
                            xscrollcommand=self.scrollbarx.set)
        self.treeview.bind("<<TreeviewSelect>>", self.item_selected)
        
        self.scrollbary.config(command=self.treeview.yview)
        self.scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbarx.config(command=self.treeview.xview)
        self.scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.treeview.heading('rank', text="Rank", anchor=tk.W)
        self.treeview.heading('title', text="Title", anchor=tk.W)
        self.treeview.heading('score', text="Score", anchor=tk.W)

        self.treeview.pack(expand=True, fill="both")
        
        t1 = threading.Thread(target=self.fill_treeview)
        t1.start()
        
    def fill_treeview(self):
        list_docs = os.listdir(DIR_DOC)
        
        if len(list_docs) == 0 :
            top_100 = extract_top100_allmanga() 
            for rank, title, score in top_100:
                self.treeview.insert("", tk.END, values=(rank, title, score))
        else :
            top100_filename = ""
            for doc in list_docs:
                if doc.startswith("top100_all") :
                    top100_filename = doc
                    
            df_top100 = pd.read_csv(DIR_DOC+top100_filename)  
            
            for index, row in df_top100.iterrows():
                self.treeview.insert("", tk.END, values=(row['Rank'],row['Title'],row['Score']))
        
    def item_selected(self, event):
        item = self.treeview.item(self.treeview.selection())
        record = item['values']

        # show a message
        messagebox.showinfo(title='Information', message=record[1])