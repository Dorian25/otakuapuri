# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 18:10:45 2022

@author: Dorian
"""

import tkinter as tk

class ScrollableFrame(tk.Frame):
# source = https://stackoverflow.com/questions/68362391/using-mousewheel-on-scrollable-frame/68363151#68363151

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.canvas = tk.Canvas(self, 
                        bg="#1e1e1e",
                        bd=0, 
                        highlightthickness=0)
        # zone d'affichage // ajouter element ici
        self.viewport = tk.Frame(self.canvas,
                                bg="#1e1e1e", 
                                borderwidth=0)
        self.scrollbar = tk.Scrollbar(self, 
                                orient="vertical", 
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # pack // place widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_window = self.canvas.create_window((0, 0), 
                                                        window=self.viewport, 
                                                        anchor="nw")
        #bind an event whenever the size of the viewport frame changes.
        self.viewport.bind("<Configure>", self.onFrameConfigure)
        #bind an event whenever the size of the viewport frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)

        self.viewport.bind('<Enter>', self._bound_to_mousewheel)
        self.viewport.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        #whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)