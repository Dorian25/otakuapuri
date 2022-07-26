# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:30:39 2022

@author: Dorian
"""

import os

DIR_IMG = "images/"
DIR_IMG_ICON = DIR_IMG + "icons/"
DIR_IMG_LOAD = DIR_IMG + "loading/"
DIR_IMG_SEARCH = DIR_IMG + "searching/"
DIR_IMG_MP3 = DIR_IMG + "mediaplayer/"
DIR_MUSIC = "musics/"
DIR_MUSIC_PLAYLIST = DIR_MUSIC + "playlist/"
DIR_MUSIC_LOAD = DIR_MUSIC + "home/"
DIR_DOC = "docs/"
DIR_TMP_COVERS = "tmp/covers/"
DIR_TMP_PAGES = "tmp/pages/"

class FileManager():
    def __init__(self):
        pass
        
        
    def delete_tmp_files(self):
        list_covers = os.listdir(DIR_TMP_COVERS)
        list_pages = os.listdir(DIR_TMP_PAGES)
        
        if len(list_covers) > 0:
            for file_name in list_covers:
                # construct full file path
                file = DIR_TMP_COVERS + file_name
                if os.path.isfile(file):
                    os.remove(file)
        if len(list_pages) > 0:
            for file_name in list_pages:
                # construct full file path
                file = DIR_TMP_PAGES + file_name
                if os.path.isfile(file):
                    os.remove(file)
                
        print("Deleted","- delete_tmp_files -", str(len(list_covers)), "files have been deleted successfully")
        print("Deleted","- delete_tmp_files -", str(len(list_pages)), "files have been deleted successfully")
        
        
    def delete_tmp_pages(self):
        list_pages = os.listdir(DIR_TMP_PAGES)
        
        if len(list_pages) > 0:
            for file_name in list_pages:
                # construct full file path
                file = DIR_TMP_PAGES + file_name
                if os.path.isfile(file):
                    os.remove(file)
                
        print("Deleted","- delete_tmp_files -", str(len(list_pages)), "files have been deleted successfully")
        
    def delete_tmp_covers(self):
        list_covers = os.listdir(DIR_TMP_COVERS)
        
        if len(list_covers) > 0:
            for file_name in list_covers:
                # construct full file path
                file = DIR_TMP_COVERS + file_name
                if os.path.isfile(file):
                    os.remove(file)
        print("Deleted","- delete_tmp_files -", str(len(list_covers)), "files have been deleted successfully")