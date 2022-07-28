# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:09:00 2022

@author: Dorian
"""

import os
import random
import pygame
import webbrowser

import tkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import font

from PIL import Image, ImageTk

import threading

from DbManager import DbManager
from FileManager import FileManager, DIR_TMP_COVERS
from utils import *

class SerieFrame(tk.Frame):
    
    font_label_head_resume = ("Verdana",15,"bold")
    font_label_resume = ("Calibri",10,"italic")
    
    def __init__(self, parent, name, infos):
        
        tk.Frame.__init__(self, parent)
        
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.parent = parent
        
        self.serie_name = name
        self.serie_infos = infos
        
        self.covers_path = []
        self.covers_img = []
        
        self.button_back = tk.Button(self,text="Back", command=self.return_searching_frame)
        
        self.frame_resume = tk.Frame(self, borderwidth=2, relief="sunken")
        self.label_head_resume = tk.Label(self.frame_resume, 
                                          text="Synopsis", 
                                          justify="center",
                                          fg="black",
                                          bg="white",
                                          font=self.font_label_head_resume)
        self.label_resume = tk.Label(self.frame_resume, 
                                     text=self.serie_infos["synopsis"],
                                     justify="center",
                                     fg="black",
                                     bg="white",
                                     font=self.font_label_resume,
                                     wraplength=700)
        
        s = ttk.Style()
        s.theme_use('default')
        s.configure("red.Horizontal.TProgressbar", 
                    background='#cf2410')       
        s.configure("red.Horizontal.TProgressbar", thickness=5)
        
        self.progressbar = ttk.Progressbar(self, 
                                           style="red.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           mode="determinate", 
                                           value=0)
    
        self.frame_info = tk.Frame(self, borderwidth=0, width=30)
        self.label_statut = tk.Label(self.frame_info, text=self.serie_infos["status"])
        self.label_type = tk.Label(self.frame_info, text=self.serie_infos["type"])
        self.label_annee = tk.Label(self.frame_info, text=self.serie_infos["year"])
        #self.label_auteur = tk.Label(self.frame_info, text=self.infos["title"]auteur)
    
        self.canvas_volumes = tk.Canvas(self, bg="#c7c7cc", bd=0, relief='ridge')
        self.canvas_volumes.bind_all("<MouseWheel>", self.on_mousewheel)
        self.scrollbar = ttk.Scrollbar(self.canvas_volumes, 
                                       orient="vertical",
                                       command=self.canvas_volumes.yview)
        self.frame_scrollable = tk.Frame(self.canvas_volumes, bg="#c7c7cc", bd=0)
        self.frame_scrollable.bind(
            "<Configure>",
            lambda e: self.canvas_volumes.configure(
                scrollregion=self.canvas_volumes.bbox("all")
            )
        )
        self.canvas_volumes.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_volumes.create_window((0,0), window=self.frame_scrollable, anchor="nw")
        
        self.button_back.pack(side="left", fill="y")
        
        self.frame_info.pack(side="top", fill="y")
        self.label_statut.pack(side="left", fill="both", expand=True)
        self.label_type.pack(side="left", fill="both", expand=True)
        self.label_annee.pack(side="left", fill="both", expand=True)
        #self.label_auteur.pack()
            
        self.frame_resume.pack(side="top", fill="x")
        self.label_head_resume.pack(side="top", fill="x")
        self.label_resume.pack(side="top", fill="x", ipadx=5, ipady=5)
        self.progressbar.pack(side="top", fill="x", ipady=3)

        self.canvas_volumes.pack(side="bottom", fill="both", expand=True)
        self.scrollbar.pack(side="right",fill="y")
        
        t2 = threading.Thread(target=self.show_covers)
        t2.start()
        
    def return_searching_frame(self):
        # delete all covers in tmp dir
        self.parent.show_searching_frame(None)
        FileManager().delete_tmp_files()
        
    def on_mousewheel(self, event):
        self.canvas_volumes.yview_scroll(int(-1*(event.delta/120)), "units")    
        
    def onClickVolume(self, event):
        if messagebox.askyesno("Download","Download this volume ?") :
            
            self.button_back.config(state="disabled")
            
            pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the volume ?",
                                                    filetypes=[("Pdf files",".pdf")],
                                                    defaultextension='.pdf')
            
            if pdf_path.endswith(".pdf"):
                print(pdf_path)
                
                url= [v for v in self.serie_infos["volumes"] if v[0] == event.widget.cget("text")][0][1]
                
                t1 = threading.Thread(target=self.download_volume, args=(url, pdf_path))
                t1.start()
            else :
                messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
        else :
            self.button_back.config(state="normal")
        
        
    def download_volume(self, url_volume, pdf_path):
        url_pages = get_all_pages_url(url_volume)
        self.progressbar.config(maximum=len(url_pages))
        
        for num_page, url_img_page in enumerate(url_pages) :
            download_page(url_img_page, num_page)
            self.progressbar["value"] = num_page+1
            self.update()
        
        convert_to_pdf(pdf_path)
        messagebox.showinfo("Done", pdf_path + " successfully downloaded !")
        
        webbrowser.open(pdf_path)
        FileManager().delete_tmp_pages()
        
        self.button_back.config(state="normal")
        
        self.progressbar["value"] = 0
        self.update()     

    def onEnter(self, event) :
        event.widget["relief"] = "raised"
        
    def onLeave(self, event) :
        event.widget["relief"] = "groove"
            

    def show_covers(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        total_tome = len(self.serie_infos["volumes"])
        n_col = 6
        n_row = total_tome // n_col
        n_col_rest = total_tome - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    num_volume = self.serie_infos["volumes"][(i*n_col)+j][0]
                    url_volume = self.serie_infos["volumes"][(i*n_col)+j][1]
                    # get_cover_manga(title_manga, n_vol, url_manga, download_dir)
                    cover_path = get_cover_manga(self.serie_infos["title"].lower().replace(" ","_"),
                                                               num_volume, 
                                                               url_volume, 
                                                               DIR_TMP_COVERS)
                    image = Image.open(cover_path)
                    image_resize = image.resize((120, 160))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
                    print("volume",(i*n_col)+j)
                    label_volume = tk.Label(self.frame_scrollable, 
                                             text=num_volume, 
                                             image=tk_image, 
                                             compound='top',
                                             borderwidth=2, 
                                             relief="groove")
                    
                    label_volume.bind("<Button-1>", self.onClickVolume)
                    label_volume.bind("<Enter>", self.onEnter)
                    label_volume.bind("<Leave>", self.onLeave)
                    
                    label_volume.grid(row=i,column=j, padx=15, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                num_volume = self.serie_infos["volumes"][(n_row*n_col)+j][0]
                url_volume = self.serie_infos["volumes"][(n_row*n_col)+j][1]
                cover_path = get_cover_manga(self.serie_infos["title"].lower().replace(" ","_"),
                                                           num_volume, 
                                                           url_volume, 
                                                           DIR_TMP_COVERS)
                image = Image.open(cover_path)
                image_resize = image.resize((120, 160))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)
                print("volume",(n_row*n_col)+j)
                label_volume = tk.Label(self.frame_scrollable, 
                                         text=num_volume, 
                                         image=tk_image, 
                                         compound='top',
                                         borderwidth=2, 
                                         relief="groove")
                
                label_volume.bind("<Button-1>", self.onClickVolume)
                label_volume.bind("<Enter>", self.onEnter)
                label_volume.bind("<Leave>", self.onLeave)
                
                label_volume.grid(row=n_row,column=j, padx=15, pady=20, sticky='ew')
                self.update()            


