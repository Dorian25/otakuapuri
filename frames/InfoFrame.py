# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 23:37:00 2023

@author: Dorian
"""



import utils.mtTkinter as tk


class InfoFrame(tk.Frame):
    
    font_label = ("Verdana",12)
    
    def __init__(self, parent, key, value):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(background="#252526")

        self.label_key = tk.Label(self, 
                                    text=key,
                                    justify="left",
                                    fg="#8e8e93",
                                    bg="#252526",
                                    font=self.font_label,
                                    wraplength=700)
        self.label_value = tk.Label(self, 
                                    text=value,
                                    justify="right",
                                    fg="white",
                                    bg="#252526",
                                    font=self.font_label,
                                    wraplength=200)

        self.label_key.pack(side="left", fill="x", padx=5, pady=5)
        self.label_value.pack(side="right", fill="x", padx=5, pady=5)

