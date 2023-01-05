# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 18:47:42 2022

@author: Dorian
"""
import tkinter as tk
# source : https://stackoverflow.com/a/31497750
class CustomListBox(tk.Listbox):

    def __init__(self, master=None, *args, **kwargs):
        tk.Listbox.__init__(self, master, *args, **kwargs)

        self.bg = "white"
        self.fg = "black"
        self.h_bg = "#c7c7cc"

        self.current = -1  # current highlighted item

        self.bind("<Motion>", self.on_motion)
        self.bind("<Leave>", self.on_leave)

    def reset_colors(self):
        """Resets the colors of the items"""
        list_of_items = self.get(0, tk.END)
        for item in list_of_items:
            self.itemconfig(list_of_items.index(item), {"bg": self.bg})
            self.itemconfig(list_of_items.index(item), {"fg": self.fg})

    def set_highlighted_item(self, index):
        """Set the item at index with the highlighted colors"""
        self.itemconfig(index, {"bg": self.h_bg})    

    def on_motion(self, event):
        """Calls everytime there's a motion of the mouse"""
        index = self.index("@%s,%s" % (event.x, event.y)) #int type
      
        if self.current != -1 and self.current != index:
            self.reset_colors()
            self.set_highlighted_item(index)
        elif self.current == -1:
            self.set_highlighted_item(index)
        self.current = index

    def on_leave(self, event):
        self.reset_colors()
        self.current = -1