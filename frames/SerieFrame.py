# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:09:00 2022

@author: Dorian
"""

import webbrowser

import utils.mtTkinter as tk
from tkinter import ttk

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

import threading

from utils.FileManager import FileManager, DIR_TMP_COVERS, DIR_IMG_ICON
from utils.utils import *

class SerieFrame(tk.Frame):
    
    font_label_resume = ("Helvetica",11,"italic")
    
    def __init__(self, parent, serie_obj):
        tk.Frame.__init__(self, parent)
        
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        
        self.parent = parent
        
        self.serie_obj = serie_obj
        self.covers_path = []
        self.covers_img = []
        
        
        self.frame_info = tk.Frame(self, borderwidth=0, width=30)
        self.label_statut = tk.Label(self.frame_info, text=serie_obj.statut)
        if serie_obj.statut == "Terminé":
            self.label_statut.config(bg="green2")
        elif serie_obj.statut == "En Cours":
            self.label_statut.config(bg="gold")
        self.label_type = tk.Label(self.frame_info, text=serie_obj.type_serie)
        self.label_annee = tk.Label(self.frame_info, text=serie_obj.annee_sortie)
        self.label_auteur = tk.Label(self.frame_info, text=serie_obj.auteur)
        
        
        self.button_back = tk.Button(self,text="Back", command=self.return_searching_frame)
        
        #self.frame_resume = tk.Frame(self, borderwidth=2, relief="sunken")
        self.frame_resume = tk.PanedWindow(self, orient="vertical", borderwidth=2, relief="sunken")
        """
        self.label_head_resume = tk.Label(self.frame_resume, 
                                          text="Synopsis", 
                                          justify="center",
                                          fg="black",
                                          bg="white",
                                          font=self.font_label_head_resume)"""
  
        self.label_resume = tk.Label(self.frame_resume, 
                                     text=self.serie_obj.synopsis,
                                     justify="center",
                                     fg="black",
                                     bg="old lace",
                                     font=self.font_label_resume,
                                     wraplength=700)
        self.frame_resume.add(self.label_resume)
        
        
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
        
        s.configure("TNotebook",tabmargins=0, tabposition='n')
        s.layout("TNotebook", [])
        s.configure('TNotebook.Tab', font=('URW Gothic L','13','bold') )
        
        self.nav_bar = ttk.Notebook(self)
        
        # VOLUMES
        self.canvas_volumes = tk.Canvas(self, bg="#c7c7cc", bd=0, relief='ridge')
        self.canvas_volumes.bind_all("<MouseWheel>", self.on_mousewheel_v)
        self.scrollbar_v = ttk.Scrollbar(self.canvas_volumes, 
                                       orient="vertical",
                                       command=self.canvas_volumes.yview)
        self.frame_scrollable_v = tk.Frame(self.canvas_volumes, bg="#c7c7cc", bd=0)
        self.frame_scrollable_v.bind(
            "<Configure>",
            lambda e: self.canvas_volumes.configure(
                scrollregion=self.canvas_volumes.bbox("all")
            )
        )
        self.canvas_volumes.configure(yscrollcommand=self.scrollbar_v.set)
        self.canvas_volumes.create_window((0,0), window=self.frame_scrollable_v, anchor="nw")
        
        ### CHAPITRE
        self.canvas_chapitres = tk.Canvas(self, bg="#c7c7cc", bd=0, relief='ridge')
        self.canvas_chapitres.bind_all("<MouseWheel>", self.on_mousewheel_c)
        self.scrollbar_c = ttk.Scrollbar(self.canvas_chapitres, 
                                       orient="vertical",
                                       command=self.canvas_chapitres.yview)
        self.frame_scrollable_c = tk.Frame(self.canvas_chapitres, bg="#c7c7cc", bd=0)
        self.frame_scrollable_c.bind(
            "<Configure>",
            lambda e: self.canvas_chapitres.configure(
                scrollregion=self.canvas_chapitres.bbox("all")
            )
        )
        self.canvas_chapitres.configure(yscrollcommand=self.scrollbar_c.set)
        self.canvas_chapitres.create_window((0,0), window=self.frame_scrollable_c, anchor="nw")
            
        self.button_back.pack(side="left", fill="y")
            
        self.frame_info.pack(side="top", fill="y")
        self.label_statut.pack(side="left", fill="x", padx=5, pady=5)
        self.label_type.pack(side="left", fill="x", padx=5, pady=5 )
        self.label_annee.pack(side="left", fill="x", padx=5, pady=5)
        self.label_auteur.pack(side="left", fill="x", padx=5, pady=5)
                
        self.frame_resume.pack(side="top", fill="x")
        #self.label_head_resume.pack(side="top", fill="x")
        #self.label_resume.pack(side="top", fill="x", ipadx=5, ipady=5)
            
        self.progressbar.pack(side="top", fill="x", ipady=3)
        
        #self.canvas_volumes.pack(side="bottom", fill="both", expand=True)
        self.nav_bar.pack(side="bottom", fill="both", expand=True)
            
        
        
        if len(self.serie_obj.volumes) > 0:
            self.nav_bar.add(self.canvas_volumes, text="Volumes ("+ str(self.serie_obj.get_number_volumes()) +")")
            self.scrollbar_v.pack(side="right",fill="y")
            
            self.thread_download_covers = threading.Thread(target=self.show_covers)
            self.thread_download_covers.start()
            
        if len(self.serie_obj.chapitres) > 0:
            self.nav_bar.add(self.canvas_chapitres, text="Chapitres ("+ str(self.serie_obj.get_number_chapitres()) +")")
            self.scrollbar_c.pack(side="right",fill="y")
            
            self.thread_show_chapters = threading.Thread(target=self.show_chapters)
            self.thread_show_chapters.start()
        
    def return_searching_frame(self):
        # delete all covers in tmp dir
        #if self.thread_download_covers.is_alive():
            # kill thread
            
        self.parent.show_searching_frame()
        FileManager().delete_tmp_files()
        
    def on_mousewheel_v(self, event):
        self.canvas_volumes.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_mousewheel_c(self, event):
        self.canvas_chapitres.yview_scroll(int(-1*(event.delta/120)), "units") 
        
    def onClickVolume(self, event):
        if messagebox.askyesno("Download","Download this volume ?") :
            
            self.button_back.config(state="disabled")
            
            pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the volume ?",
                                                    filetypes=[("Pdf files",".pdf")],
                                                    defaultextension='.pdf')
            
            if pdf_path.endswith(".pdf"):
                print(pdf_path)
                
                url_pages = self.serie_obj.volumes[event.widget.cget("text")]
                
                t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path))
                t1.start()
            else :
                messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
        else :
            self.button_back.config(state="normal")
    
    def onClickChapter(self, event):
        if messagebox.askyesno("Download","Download this chapter ?") :
            
            self.button_back.config(state="disabled")
            
            pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the chapter ?",
                                                    filetypes=[("Pdf files",".pdf")],
                                                    defaultextension='.pdf')
            
            if pdf_path.endswith(".pdf"):
                print(pdf_path)
                
                # optimiser cette recherche ?
                url_pages = self.serie_obj.chapitres[event.widget.cget("text")]
                
                t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path))
                t1.start()
            else :
                messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
        else :
            self.button_back.config(state="normal")
        
    def download_volume(self, url_pages, pdf_path):
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
        
    def show_chapters(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        total_tome = len(self.serie_obj.chapitres)
        n_col = 6
        n_row = total_tome // n_col
        n_col_rest = total_tome - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    num_volume = self.serie_obj.get_list_numeros_chapitres()[(i*n_col)+j]

                    image = Image.open(DIR_IMG_ICON+'chapter_1.png')
                    image_resize = image.resize((120, 160))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
                    
                    label_volume = tk.Label(self.frame_scrollable_c, 
                                             text=num_volume, 
                                             image=tk_image,
                                             font=("Impact",13),
                                             compound='top',
                                             borderwidth=2, 
                                             relief="groove")
                    
                    label_volume.bind("<Button-1>", self.onClickChapter)
                    label_volume.bind("<Enter>", self.onEnter)
                    label_volume.bind("<Leave>", self.onLeave)
                    
                    label_volume.grid(row=i,column=j, padx=15, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                num_volume = self.serie_obj.get_list_numeros_chapitres()[(n_row*n_col)+j]
                
                image = Image.open(DIR_IMG_ICON+'chapter_1.png')
                image_resize = image.resize((120, 160))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)
                
                label_volume = tk.Label(self.frame_scrollable_c, 
                                         text=num_volume, 
                                         image=tk_image,
                                         font=("Impact",13),
                                         compound='top',
                                         borderwidth=2, 
                                         relief="groove")
                
                label_volume.bind("<Button-1>", self.onClickChapter)
                label_volume.bind("<Enter>", self.onEnter)
                label_volume.bind("<Leave>", self.onLeave)
                
                label_volume.grid(row=n_row,column=j, padx=15, pady=20, sticky='ew')
                self.update() 
            

    def show_covers(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        total_tome = len(self.serie_obj.volumes)
        n_col = 6
        n_row = total_tome // n_col
        n_col_rest = total_tome - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    num_volume = self.serie_obj.get_list_numeros_volumes()[(i*n_col)+j]
                    url_cover = self.serie_obj.volumes[num_volume][0]
                    # get_cover_manga(title_manga, n_vol, url_cover, download_dir)
                    cover_path = get_cover_manga(self.serie_obj.titre.lower().replace(" ","_"),
                                                num_volume,
                                                url_cover, 
                                                DIR_TMP_COVERS)
                    image = Image.open(cover_path)
                    image_resize = image.resize((120, 160))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
                    print("volume",(i*n_col)+j)
                    label_volume = tk.Label(self.frame_scrollable_v, 
                                             text=num_volume,
                                             font=("Impact",13),
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
                num_volume = self.serie_obj.get_list_numeros_volumes()[(n_row*n_col)+j]
                url_cover = self.serie_obj.volumes[num_volume][0]
                # get_cover_manga(title_manga, n_vol, url_cover, download_dir)
                cover_path = get_cover_manga(self.serie_obj.titre.lower().replace(" ","_"),
                                            num_volume,
                                            url_cover, 
                                            DIR_TMP_COVERS)
                image = Image.open(cover_path)
                image_resize = image.resize((120, 160))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)
                print("volume",(n_row*n_col)+j)
                label_volume = tk.Label(self.frame_scrollable_v, 
                                         text=num_volume, 
                                         font=("Impact",13),
                                         image=tk_image, 
                                         compound='top',
                                         borderwidth=2, 
                                         relief="groove")
                
                label_volume.bind("<Button-1>", self.onClickVolume)
                label_volume.bind("<Enter>", self.onEnter)
                label_volume.bind("<Leave>", self.onLeave)
                
                label_volume.grid(row=n_row,column=j, padx=15, pady=20, sticky='ew')
                self.update()            


