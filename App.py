# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 21:20:08 2022

@author: Dorian
"""

import tkinter as tk
import pygame

from LoadingFrame import LoadingFrame
from SearchingFrame import SearchingFrame
from SerieFrame import SerieFrame
from FileManager import FileManager, DIR_IMG_ICON

class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # source : https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        # Gets the requested values of the height and width.
        windowWidth = 1000
        windowHeight = 500
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight/2)
        # Positions the window in the center of the page.
        self.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
        
        self.resizable(False, False)
        self.iconbitmap(DIR_IMG_ICON + 'icon.ico')
        self.title('Get-Mangas !')
        
        self.current_frame = None
            
        self.show_loading_frame()
    
    def show_searching_frame(self, key_figures):
        if self.current_frame :
            self.current_frame.destroy()
        
        self.current_frame = SearchingFrame(parent=self, data=key_figures)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title("Get-Mangas !")
        
    def show_loading_frame(self):
        if self.current_frame :
            self.current_frame.destroy()
            
        self.current_frame = LoadingFrame(parent=self)
        self.current_frame.pack(expand=True, fill="both")
        
        self.current_frame.animate()
             
    def show_serie_frame(self, serie_name, serie_infos):
        if self.current_frame :
            self.current_frame.destroy()
            
        self.current_frame = SerieFrame(parent=self, name=serie_name, infos=serie_infos)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title(self.current_frame.serie_infos["title"] + 
                   " - " + 
                   str(len(self.current_frame.serie_infos["volumes"])) + 
                   " volumes are available !")
        
        
        
###########
if __name__ == "__main__":
    app = App()
    app.mainloop()
    FileManager().delete_tmp_files()
    pygame.quit()
