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
from frames.OptubeFrame import OptubeFrame
from frames.ErrorFrame import ErrorFrame
from frames.SearchingFrame import SearchingFrame
from frames.SerieFrame import SerieFrame
from frames.MALRankingFrame import MALRankingFrame
from frames.SplashScreenFrame import SplashScreenFrame
import utils.mtTkinter as tk
from utils.DbManager import MongoDBManager
from utils.FileManager import FileManager, DIR_IMG_ICON
from utils.utils import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class App(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # source : https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
        # Gets the requested values of the height and width.
        windowWidth = 1100
        windowHeight = 534
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/3 - windowHeight/2)
        # Positions the window in the center of the page.
        self.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
        
        self.resizable(False, False)
        self.iconbitmap(DIR_IMG_ICON + 'icon.ico')
        self.title('Otaku Apuri (v1.2.2)')
        
        self.series_available_sushiscan = []
        self.series_available_manganato = []
        
        self.current_frame = None
        self.mongoclient = MongoClient("mongodb+srv://"+os.getenv('USER_PYMONGO')+":"+os.getenv('PASS_PYMONGO')+"@getmangacluster.zmh5nne.mongodb.net/?retryWrites=true&w=majority", 
                            server_api=ServerApi('1'))
        
        #self.show_loading_frame()
        self.show_splashscreen_frame()
        #self.show_optube_frame()
        #self.show_searching_frame()
        #self.show_serie_frame(MongoDBManager.get_serie_infos_pymongo(self.mongoclient, "Blue Lock", "sushiscan"))

    def set_series_available(self, source="sushiscan"):
        self.series_available_sushiscan = MongoDBManager.get_all_series_pymongo(self.mongoclient, "sushiscan")
        time.sleep(1)
        self.series_available_manganato = MongoDBManager.get_all_series_pymongo(self.mongoclient, "manganato")
        
        print("Manganato", len(self.series_available_manganato))
        print("Sushiscan", len(self.series_available_sushiscan))

    def show_searching_frame(self):
        """Show the SearchingFrame
        """
        if self.current_frame :
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
            self.current_frame.destroy()
        
        self.current_frame = SearchingFrame(parent=self)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title("Otaku Apuri (v1.2.2)")

    def show_splashscreen_frame(self):
        """Show the SplashScreenFrame
        """
        if self.current_frame :
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
            self.current_frame.destroy()

        self.current_frame = SplashScreenFrame(parent=self)
        self.current_frame.pack(expand=True, fill="both")

        self.current_frame.after(0, self.current_frame.update, 0)

    def show_optube_frame(self):
        """Show the OptubeFrame
        """
        if self.current_frame :
            self.current_frame.mediaplayer.stop()
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
            self.current_frame.destroy()

        self.current_frame = OptubeFrame(parent=self, app=self)
        self.current_frame.pack(expand=True, fill="both")

        self.current_frame.splash_screen()

    def show_loading_frame(self):
        """Show the LoadingFrame
        - A quote is chose randomly
        - If while the loading bar is animated
        
        """
        if self.current_frame :
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
            self.current_frame.destroy()

        quote = random.choice(quotes_anime)   
        self.current_frame = LoadingFrame(parent=self, quote_txt=quote)
        self.current_frame.pack(expand=True, fill="both")
        
        if len(self.series_available_sushiscan) == 0:
            thread = threading.Thread(target=self.set_series_available, daemon=True)
            thread.start()

        self.current_frame.animate()
             
    def show_serie_frame(self, serie):
        """_summary_

        Args:
            serie (_type_): _description_
        """
        if self.current_frame :
            self.current_frame.mediaplayer.stop()
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
            self.current_frame.destroy()
            
        self.current_frame = SerieFrame(parent=self, serie_obj=serie)
        self.current_frame.pack(expand=True, fill="both")
        
        self.title(self.current_frame.serie_obj.titre)
        
    def show_malranking_frame(self):
        """_summary_
        """
        if self.current_frame :
            self.current_frame.mediaplayer.stop()
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
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
            # Supprimer tous les widgets enfants de la video_frame
            for child in self.current_frame.winfo_children():
                child.destroy()
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
# TODO : Gérer toutes les exceptions
# TODO : Paginer les chapitres volumes


if __name__ == "__main__":
    extDataDir = os.getcwd()
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):        
    	# sys._MEIPASS = C:\Users\xxxx\AppData\Local\Temp\_MEIxxxxxx
        os.chdir(sys._MEIPASS)
        extDataDir = sys._MEIPASS
    # https://github.com/pyinstaller/pyinstaller/issues/5522#issuecomment-770858489
    load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

    thread_create_folders = threading.Thread(target=FileManager.create_tmp_folders, daemon=True)
    thread_create_folders.start()
    
    app = App()
    app.mainloop()
    
    if isinstance(app.current_frame, SerieFrame):
        app.current_frame.frame_anime.stop(quit=True)

    app.mongoclient.close()
    FileManager.delete_tmp_files()
    pygame.quit()