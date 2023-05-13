# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 19:06:58 2022

@author: Dorian
"""
import tkinter as tk
from tkinter import ttk

from tkinter import messagebox

from utils.utils import top_100_mal

from utils.DbManager import MongoDBManager

import threading

class TreeviewMALFrame(tk.Frame):
    
    COLUMNS = ('rank','title','score')
    
    def __init__(self, parent, which, app):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.app = app
        self.which = which

        s = ttk.Style()
        s.configure('Treeview.Heading',
                    background="#4f74c8",
                    foreground="white")

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
        
        self.treeview.heading('rank', text="Rank", anchor=tk.CENTER)
        self.treeview.heading('title', text="Title", anchor=tk.CENTER)
        self.treeview.heading('score', text="Score", anchor=tk.CENTER)

        self.treeview.pack(expand=True, fill="both")
        
        t1 = threading.Thread(target=self.fill_treeview)
        t1.start()
        
    def fill_treeview(self):
        top_100 = top_100_mal(which=self.which, page=0)
        print(top_100) 
        for rank, title, score in top_100:
            self.treeview.insert("", tk.END, values=(rank, title, score))

    def clear_all(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def fill_treeview_next(self, i): 
        self.clear_all()

        top_100 = top_100_mal(which=self.which, page=i) 
        for rank, title, score in top_100:
            self.treeview.insert("", tk.END, values=(rank, title, score))

    def item_selected(self, event):
        item = self.treeview.item(self.treeview.selection())
        record = item['values']

        # show a message
        serie = MongoDBManager.get_serie_infos_from_mal_pymongo(self.app.mongoclient, record[1])
        if serie:
            self.app.show_serie_frame(serie)
        else :
            messagebox.showwarning("Sorry, this series was not found ! Try another one...")
