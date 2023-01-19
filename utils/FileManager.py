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
DIR_TMP_CHARACTERS = "tmp/characters/"
DIR_TMP_PAGES = "tmp/pages/"

class FileManager(object):
    # https://stackoverflow.com/questions/30556857/creating-a-static-class-with-no-instances
    @staticmethod
    def create_tmp_folders():
        try:
            os.makedirs(DIR_TMP_PAGES, exist_ok = True)
            print("Directory '%s' created successfully" % DIR_TMP_PAGES)
        except OSError as error:
            print("Directory '%s' can not be created" % DIR_TMP_PAGES)

        try:
            os.makedirs(DIR_TMP_COVERS, exist_ok = True)
            print("Directory '%s' created successfully" % DIR_TMP_COVERS)
        except OSError as error:
            print("Directory '%s' can not be created" % DIR_TMP_COVERS)

        try:
            os.makedirs(DIR_TMP_CHARACTERS, exist_ok = True)
            print("Directory '%s' created successfully" % DIR_TMP_CHARACTERS)
        except OSError as error:
            print("Directory '%s' can not be created" % DIR_TMP_CHARACTERS)

    @staticmethod
    def delete_tmp_files():
        list_covers = os.listdir(DIR_TMP_COVERS)
        list_pages = os.listdir(DIR_TMP_PAGES)
        list_characters = os.listdir(DIR_TMP_CHARACTERS)
        
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

        if len(list_characters) > 0:
            for file_name in list_characters:
                # construct full file path
                file = DIR_TMP_CHARACTERS + file_name
                if os.path.isfile(file):
                    os.remove(file)
                
        print("Deleted","- delete_tmp_files -", str(len(list_covers)), "files have been deleted successfully")
        print("Deleted","- delete_tmp_files -", str(len(list_pages)), "files have been deleted successfully")
        print("Deleted","- delete_tmp_files -", str(len(list_characters)), "files have been deleted successfully")

    @staticmethod      
    def delete_tmp_pages():
        list_pages = os.listdir(DIR_TMP_PAGES)
        
        if len(list_pages) > 0:
            for file_name in list_pages:
                # construct full file path
                file = DIR_TMP_PAGES + file_name
                if os.path.isfile(file):
                    os.remove(file)
                
        print("Deleted","- delete_tmp_files -", str(len(list_pages)), "files have been deleted successfully")

    @staticmethod    
    def delete_tmp_covers():
        list_covers = os.listdir(DIR_TMP_COVERS)
        
        if len(list_covers) > 0:
            for file_name in list_covers:
                # construct full file path
                file = DIR_TMP_COVERS + file_name
                if os.path.isfile(file):
                    os.remove(file)
        print("Deleted","- delete_tmp_files -", str(len(list_covers)), "files have been deleted successfully")