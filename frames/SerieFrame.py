# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:09:00 2022

@author: Dorian
"""

import webbrowser

import utils.mtTkinter as tk
from tkinter import ttk

from frames.DetailsTabFrame import DetailsTabFrame
from frames.ScrollableFrame import ScrollableFrame
from frames.StatsFrame import StatsFrame

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

import threading
import concurrent.futures

from utils.FileManager import FileManager, DIR_TMP_COVERS, DIR_TMP_PAGES, DIR_TMP_CHARACTERS, DIR_IMG_ICON
from utils.utils import *

class SerieFrame(tk.Frame):
    
    font_label_frame_details = ("Verdana",12)
    font_label_frame_info = ("Verdana", 12)
    
    def __init__(self, parent, serie_obj):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        # style
        s = ttk.Style()
        s.theme_use("default")
        s.configure("red.Horizontal.TProgressbar", 
                    thickness=10,
                    background='#cf2410')
        s.configure("TNotebook",
                    background="#1e1e1e",
                    borderwidth=0)

        s.configure('TNotebook.Tab',
                    padding= [10, 10],
                    font=("Verdana", 12),
                    background= "#333333",
                    foreground= "white")
        s.map("TNotebook.Tab",
                background=[("selected", "#1e1e1e")],
                font=[("selected", ("Verdana", 12, "bold"))])
        
        # variables
        self.serie_obj = serie_obj
        self.covers_img = []
        self.downloading = False

        # Widgets
        self.nav_bar = ttk.Notebook(self)

        self.frame_info = tk.Frame(self, borderwidth=0, width=30, background="#252526")
        self.label_statut = tk.Label(self.frame_info, text=serie_obj.statut, font=self.font_label_frame_info)
        if serie_obj.statut == "Terminé":
            self.label_statut.config(bg="#32d74b")
        elif serie_obj.statut == "En Cours":
            self.label_statut.config(bg="#ff9f0a")
        elif serie_obj.statut == "Abandonné":
            self.label_statut.config(bg="#ff375f")
        elif serie_obj.statut == "En Pause":
            self.label_statut.config(bg="#98989d")
        self.label_type = tk.Label(self.frame_info, text=serie_obj.type_serie, font=self.font_label_frame_info)
        self.label_annee = tk.Label(self.frame_info, text=serie_obj.annee_sortie, font=self.font_label_frame_info)
        self.label_auteur = tk.Label(self.frame_info, text=serie_obj.auteur, font=self.font_label_frame_info, wraplength=200)
        
        image = Image.open("images\icons\icon_left.png")
        tk_image_button = ImageTk.PhotoImage(image)
        self.covers_img.append(tk_image_button)
        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= tk_image_button, 
                                    command=self.return_searching_frame,
                                    borderwidth=0)
        
        self.frame_resume = tk.Frame(self, background="#1e1e1e")
        self.label_resume_h = tk.Label(self.frame_resume,
                                        text="Synopsis",
                                        fg="white",
                                        bg="#1e1e1e",
                                        font=("Georgia", 14, "bold"))
        self.label_resume = tk.Label(self.frame_resume, 
                                    text=self.serie_obj.synopsis,
                                    justify="center",
                                    fg="white",
                                    bg="#1e1e1e",
                                    font=self.font_label_frame_details,
                                    wraplength=700)
        
        self.progressbar = ttk.Progressbar(self, 
                                           style="red.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           mode="determinate", 
                                           value=0)
        
        # VOLUMES
        self.frame_volumes = ScrollableFrame(self)
        # CHAPITRES
        self.frame_chapitres = ScrollableFrame(self)
        # CHARACTERS 
        self.frame_characters = ScrollableFrame(self)
        
        self.nav_bar.add(self.frame_resume, text="Details")
        '''
        if self.serie_obj.statistics:
            # STATISTICS
            self.frame_statistics = StatsFrame(self, self.serie_obj.statistics)
            self.frame_stats = DetailsTabFrame(self.frame_statistics, self.serie_obj.statistics)
            self.frame_stats.pack(side="top", fill="x", pady=15)
            self.nav_bar.add(self.frame_statistics, text="Statistics")
        '''
            
        # PACK
        self.label_resume_h.pack()
        self.label_resume.pack(side="top", pady=15)
        
        self.button_back.pack(side="left", fill="y")
        self.frame_info.pack(side="left", fill="y")
        
        self.label_statut.pack(side="bottom", fill="x", padx=5, pady=5)
        self.label_type.pack(side="bottom", fill="x", padx=5, pady=5 )
        self.label_annee.pack(side="bottom", fill="x", padx=5, pady=5)
        self.label_auteur.pack(side="bottom", fill="x", padx=5, pady=5)
            
        self.progressbar.pack(side="bottom", fill="x")
        self.nav_bar.pack(side="right", fill="both", expand=True)

        self.launch_threads()
            
    def launch_threads(self):
        self.thread_dl_cover = threading.Thread(target=self.download_cover_serie, daemon=True)
        self.thread_dl_cover.start()

        if len(self.serie_obj.volumes) > 0:
            self.nav_bar.add(self.frame_volumes, text="Volumes ("+ str(self.serie_obj.get_number_volumes()) +")")
            
            self.thread_download_covers = threading.Thread(target=self.show_covers, daemon=True)
            self.thread_download_covers.start()
            
        if len(self.serie_obj.chapitres) > 0:
            self.nav_bar.add(self.frame_chapitres, text="Chapitres ("+ str(self.serie_obj.get_number_chapitres()) +")")
            
            self.thread_show_chapters = threading.Thread(target=self.show_chapters, daemon=True)
            self.thread_show_chapters.start()

        if len(self.serie_obj.characters) > 0:
            self.nav_bar.add(self.frame_characters, text="Personnages")

            self.thread_dl_char = threading.Thread(target=self.download_characters_img, daemon=True)
            self.thread_dl_char.start()  

    def return_searching_frame(self):
        # delete all covers in tmp dir
        #if self.thread_download_covers.is_alive():
            # kill thread
            
        self.parent.show_searching_frame()
        FileManager().delete_tmp_files()
        
    def onClickVolume(self, event):
        if not self.downloading :
            if messagebox.askyesno("Download","Download this volume ?") :
                self.downloading = True
                self.button_back.config(state="disabled")
                
                pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the volume ?",
                                                        filetypes=[("Pdf files",".pdf")],
                                                        defaultextension='.pdf')
                
                if pdf_path.endswith(".pdf"):
                    print(pdf_path)
                    
                    url_pages = self.serie_obj.volumes[event.widget.cget("text")]
                    
                    t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path), daemon=True)
                    t1.start()
                else :
                    messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
            else :
                self.button_back.config(state="normal")
        else :
            messagebox.showerror("Error", "Wait until your download finish")
    
    def onClickChapter(self, event):
        if not self.downloading :
            if messagebox.askyesno("Download","Download this chapter ?") :
                self.downloading = True
                self.button_back.config(state="disabled")
                
                pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the chapter ?",
                                                        filetypes=[("Pdf files",".pdf")],
                                                        defaultextension='.pdf')
                
                if pdf_path.endswith(".pdf"):
                    print(pdf_path)
                    
                    # optimiser cette recherche ?
                    url_pages = self.serie_obj.chapitres[event.widget.cget("text")]
                    
                    t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path), daemon=True)
                    t1.start()
                else :
                    messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
            else :
                self.button_back.config(state="normal")
        else:
            messagebox.showerror("Error", "Wait until your download finish")

    def download_characters_img(self):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            futures = []
            for rank, charac in enumerate(self.serie_obj.get_top20_characters()[0]) :
                futures.append(pool.submit(download_element, 
                                        url_page=charac['url_image'], 
                                        filename=str(rank) + "_" + charac['name'].lower().replace(',','').replace(' ','_'),
                                        dir_tmp=DIR_TMP_CHARACTERS))
            
            for future in concurrent.futures.as_completed(futures):
                msg, filename = future.result()
                if "GOOD" in msg :
                    print(msg)
        
        thread_show_characters = threading.Thread(target=self.show_characters, daemon=True)
        thread_show_characters.start()
                    


    def download_cover_serie(self):
        '''
        chrome_opts = uc.ChromeOptions()
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--headless")
        driver = uc.Chrome(options=chrome_opts)

        download_cover(self.serie_obj.titre.lower().replace(" ","_"), self.serie_obj.volumes["1"][0], driver)

        driver.close()
        '''
        if len(self.serie_obj.volumes)>0:
            msg, filename = download_element(self.serie_obj.volumes["1"][0], 
                                            self.serie_obj.titre.lower().replace(" ","_"), 
                                            DIR_TMP_COVERS)
        else :
            msg, filename = download_element(self.serie_obj.chapitres["1"][0], 
                                            self.serie_obj.titre.lower().replace(" ","_"), 
                                            DIR_TMP_COVERS)

        if "GOOD" in msg:
            image = Image.open(filename)
            image_resize = image.resize((200, 293))
            tk_image_cover = ImageTk.PhotoImage(image_resize)
            self.covers_img.append(tk_image_cover)
            self.label_cover = tk.Label(self.frame_info, 
                                        image=tk_image_cover, 
                                        highlightthickness=0, 
                                        borderwidth=0)
            self.label_cover.pack(side="top", padx=5, pady=5)
            self.update()
        else :
            print(msg)
            # default cover with "?" 

    def download_volume(self, url_pages, pdf_path):
        self.progressbar.config(maximum=len(url_pages))
        print("Number Page to DL", len(url_pages))
        
        with concurrent.futures.ThreadPoolExecutor() as pool:
            futures = []
            for num_page, url_img_page in enumerate(url_pages) :
                futures.append(pool.submit(download_element, 
                                        url_page=url_img_page, 
                                        filename=str(num_page+1),
                                        dir_tmp=DIR_TMP_PAGES))
            
            for future in concurrent.futures.as_completed(futures):
                msg, filename = future.result()
                if "GOOD" in msg :
                    self.progressbar["value"] = num_page+1
                    self.update()

        
        convert_to_pdf(pdf_path)
        messagebox.showinfo("Done", pdf_path + " successfully downloaded !")
        
        webbrowser.open(pdf_path)
        FileManager().delete_tmp_pages()
        
        self.button_back.config(state="normal")
        
        self.progressbar["value"] = 0
        self.downloading = False
        self.update()     

    def onEnter(self, event) :
        event.widget["relief"] = "groove"
     
        
    def onLeave(self, event) :
        event.widget["relief"] = "flat"
 

    def show_characters(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        top20, top20_i = self.serie_obj.get_top20_characters()
        n_col = 5
        n_row = len(top20) // n_col
        n_col_rest = len(top20) - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    name_charact = top20[(i*n_col)+j]["name"]

                    image = Image.open(DIR_TMP_CHARACTERS+top20_i[(i*n_col)+j])
                    image_resize = image.resize((100, 140))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
                    
                    label_volume = tk.Label(self.frame_characters.viewport, 
                                            text=name_charact, 
                                            image=tk_image,
                                            font=("Verdana",13),
                                            fg="white",
                                            bg="#1e1e1e",
                                            compound='top',
                                            wraplength=100,
                                            highlightthickness=0, 
                                            borderwidth=0)
                    
                    label_volume.grid(row=i,column=j, padx=20, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                name_charact = top20[(n_row*n_col)+j]["name"]
                
                image = Image.open(DIR_TMP_CHARACTERS+top20_i[(n_row*n_col)+j])
                image_resize = image.resize((100,140))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)
                
                label_volume = tk.Label(self.frame_characters.viewport, 
                                        text=name_charact, 
                                        image=tk_image,
                                        font=("Verdana",13),
                                        fg="white",
                                        bg="#1e1e1e",
                                        compound='top',
                                        wraplength=100,
                                        highlightthickness=0, 
                                        borderwidth=0)
                
                label_volume.grid(row=n_row,column=j, padx=20, pady=20, sticky='ew')
                self.update() 

        
    def show_chapters(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        total_tome = len(self.serie_obj.chapitres)
        n_col = 5
        n_row = total_tome // n_col
        n_col_rest = total_tome - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    num_volume = self.serie_obj.get_list_numeros_chapitres()[(i*n_col)+j]

                    image = Image.open(DIR_IMG_ICON+'cover_chapitre.png')
                    image_resize = image.resize((110, 150))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
                    
                    label_volume = tk.Label(self.frame_chapitres.viewport, 
                                            text=num_volume, 
                                            image=tk_image,
                                            font=("Impact",13),
                                            compound='top',
                                            borderwidth=2, 
                                            fg="white",
                                            bg="#1e1e1e",
                                            relief="flat")
                    
                    label_volume.bind("<Button-1>", self.onClickChapter)
                    label_volume.bind("<Enter>", self.onEnter)
                    label_volume.bind("<Leave>", self.onLeave)
                    
                    label_volume.grid(row=i,column=j, padx=15, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                num_volume = self.serie_obj.get_list_numeros_chapitres()[(n_row*n_col)+j]
                
                image = Image.open(DIR_IMG_ICON+'cover_chapitre.png')
                image_resize = image.resize((110, 150))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)
                
                label_volume = tk.Label(self.frame_chapitres.viewport, 
                                        text=num_volume, 
                                        image=tk_image,
                                        font=("Impact",13),
                                        compound='top',
                                        borderwidth=2, 
                                        fg="white",
                                        bg="#1e1e1e",
                                        relief="flat")
                
                label_volume.bind("<Button-1>", self.onClickChapter)
                label_volume.bind("<Enter>", self.onEnter)
                label_volume.bind("<Leave>", self.onLeave)
                
                label_volume.grid(row=n_row,column=j, padx=15, pady=20, sticky='ew')
                self.update() 
            

    def show_covers(self) :
        # ideas
        ## change color cover grayscale if already rade
        
        total_tome = len(self.serie_obj.volumes)
        n_col = 5
        n_row = total_tome // n_col
        n_col_rest = total_tome - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    num_volume = self.serie_obj.get_list_numeros_volumes()[(i*n_col)+j]

                    # url_cover = self.serie_obj.volumes[num_volume][0]
                    # get_cover_manga(title_manga, n_vol, url_cover, download_dir)
                    # cover_path = get_cover_manga(self.serie_obj.titre.lower().replace(" ","_"),
                    #                            num_volume,
                    #                            url_cover, 
                    #                            DIR_TMP_COVERS)
                    image = Image.open(DIR_IMG_ICON+'cover_manga.png')
                    image_resize = image.resize((110, 150))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_img.append(tk_image)
    
                    label_volume = tk.Label(self.frame_volumes.viewport, 
                                            text=num_volume,
                                            font=("Impact",13),
                                            image=tk_image,
                                            fg="white",
                                            bg="#1e1e1e",
                                            borderwidth=2,
                                            compound='top',
                                            relief="flat")
                    
                    label_volume.bind("<Button-1>", self.onClickVolume)
                    label_volume.bind("<Enter>", self.onEnter)
                    label_volume.bind("<Leave>", self.onLeave)
                    
                    label_volume.grid(row=i,column=j, padx=15, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                num_volume = self.serie_obj.get_list_numeros_volumes()[(n_row*n_col)+j]
                # url_cover = self.serie_obj.volumes[num_volume][0]
                # get_cover_manga(title_manga, n_vol, url_cover, download_dir)
                # cover_path = get_cover_manga(self.serie_obj.titre.lower().replace(" ","_"),
                #                            num_volume,
                #                            url_cover, 
                #                            DIR_TMP_COVERS)
                image = Image.open(DIR_IMG_ICON+'cover_manga.png')
                image_resize = image.resize((110, 150))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_img.append(tk_image)

                label_volume = tk.Label(self.frame_volumes.viewport, 
                                        text=num_volume, 
                                        font=("Impact",13),
                                        image=tk_image, 
                                        fg="white",
                                        bg="#1e1e1e",
                                        compound='top',
                                        borderwidth=2,
                                        relief="flat")
                
                label_volume.bind("<Button-1>", self.onClickVolume)
                label_volume.bind("<Enter>", self.onEnter)
                label_volume.bind("<Leave>", self.onLeave)
                
                label_volume.grid(row=n_row,column=j, padx=15, pady=20, sticky='ew')
                self.update()            