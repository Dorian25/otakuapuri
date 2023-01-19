# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:00:34 2022

@author: Dorian
"""

import tkinter as tk

class DetailsTabFrame(tk.Frame):
    
    def __init__(self, parent, serie_info):
        tk.Frame.__init__(self, parent)
        
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.label_score = tk.Label(self, text="score", font='Helvetica 18')
        self.label_ranked = tk.Label(self, text="Ranked", font='Helvetica 14')
        self.label_popularity = tk.Label(self, text="Popularity", font='Helvetica 14')
        self.label_members = tk.Label(self, text="Members", font='Helvetica 14')
        self.label_favorites = tk.Label(self, text="Favorites", font='Helvetica 14')

        if serie_info :
            self.label_score_val = tk.Label(self, 
                                            text=serie_info["Score"],
                                            font='Helvetica 18 bold')
            self.label_ranked_val = tk.Label(self, 
                                            text="#" + str(serie_info["Ranked"]),
                                            font='Helvetica 14 bold')
            self.label_popularity_val = tk.Label(self, 
                                            text="#" + str(serie_info["Popularity"]),
                                            font='Helvetica 14 bold')
            self.label_members_val = tk.Label(self, 
                                            text=serie_info["Members"],
                                            font='Helvetica 14 bold')
            self.label_favorites_val = tk.Label(self, 
                                            text=serie_info["Favorites"],
                                            font='Helvetica 14 bold')
        else :
            self.label_score_val = tk.Label(self, text="?", font='Helvetica 14 bold')
            self.label_ranked_val = tk.Label(self, text="?", font='Helvetica 14 bold')
            self.label_popularity_val = tk.Label(self, text="?", font='Helvetica 14 bold')
            self.label_members_val = tk.Label(self, text="?", font='Helvetica 14 bold')
            self.label_favorites_val = tk.Label(self, text="?", font='Helvetica 14 bold')
        

        self.label_score.pack(side="left")
        self.label_score_val.pack(side="left")
        self.label_ranked.pack(side="left", padx=10)
        self.label_ranked_val.pack(side="left")
        self.label_popularity.pack(side="left", padx=10)
        self.label_popularity_val.pack(side="left")
        self.label_members.pack(side="left", padx=10)
        self.label_members_val.pack(side="left")
        self.label_favorites.pack(side="left", padx=10)
        self.label_favorites_val.pack(side="left")