# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 21:20:08 2022

@author: Dorian
"""

import os 
import sys
import random
import threading
from dotenv import load_dotenv
import pygame
from frames.LoadingFrame import LoadingFrame
from frames.ErrorFrame import ErrorFrame
from frames.SearchingFrame import SearchingFrame
from frames.SerieFrame import SerieFrame
from frames.MALRankingFrame import MALRankingFrame
import utils.mtTkinter as tk
from utils.DbManager import MongoDBManager
from utils.FileManager import FileManager, DIR_IMG_ICON
from utils.utils import *

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
        
        self.series_available = []
        
        self.current_frame = None
        
        self.show_loading_frame(random.choice(quotes_anime))

    def set_series_available(self):
        self.series_available = MongoDBManager.get_all_series()

    def show_searching_frame(self):
        """Show the SearchingFrame
        """

        if self.current_frame :
            self.current_frame.destroy()
        
        self.current_frame = SearchingFrame(parent=self)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title("Get-Mangas ! ["+str(len(self.series_available))+" series available]")
        
    def show_loading_frame(self, quote):
        """Show the LoadingFrame

        Args:
            quote (str): a quote 
        """

        if self.current_frame :
            self.current_frame.destroy()
            
        self.current_frame = LoadingFrame(parent=self, quote_txt=quote)
        self.current_frame.pack(expand=True, fill="both")
        
        if len(self.series_available) == 0:
            thread = threading.Thread(target=self.set_series_available, daemon=True)
            thread.start()

        self.current_frame.animate()
             
    def show_serie_frame(self, serie):
        """_summary_

        Args:
            serie (_type_): _description_
        """

        if self.current_frame :
            self.current_frame.destroy()
            
        self.current_frame = SerieFrame(parent=self, serie_obj=serie)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title(self.current_frame.serie_obj.titre)
        
    def show_malranking_frame(self):
        """_summary_
        """

        if self.current_frame :
            self.current_frame.destroy()
        
        self.current_frame = MALRankingFrame(parent=self)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title("Top Manga - MyAnimeList.net")
        
    def show_error_frame(self, error_msg):
        """_summary_

        Args:
            error_msg (_type_): _description_
        """

        if self.current_frame :
            self.current_frame.destroy()
            
        self.current_frame = ErrorFrame(parent=self, error_txt=error_msg)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title("Error")
        
              
###########

# TODO : revoir la gestion du pygame pour la musique etc...
# TODO : revoir la gestion du message d'erreur internet (position du bouton relancer showloading et showsearching)
# TODO : revoir la recherche via  MAL (score doit être minimum de 10 sinon ce n'est pas le bon résultat)
# TODO : revoir la pipeline ETL pour MAL pour inclure les stats
# TODO : revoir les séries qui n'ont pas VOLUMES ou CHAPITRES 
# TODO : revoir l'aspect graphique de l'application
# TODO : revoir l'onglet Stats 
# TODO : essayer d'avoir des onglets de couleurs différentes


if __name__ == "__main__":
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):        
    	# sys._MEIPASS = C:\Users\xxxx\AppData\Local\Temp\_MEIxxxxxx
        os.chdir(sys._MEIPASS)
        extDataDir = sys._MEIPASS
    # https://github.com/pyinstaller/pyinstaller/issues/5522#issuecomment-770858489
    load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

    FileManager.create_tmp_folders()
    
    app = App()
    app.mainloop()
    
    FileManager.delete_tmp_files()
    pygame.quit()