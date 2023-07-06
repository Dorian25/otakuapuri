# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:09:00 2022

@author: Dorian
"""

import time
import webbrowser

import utils.mtTkinter as tk
from tkinter import ttk

from frames.DetailsTabFrame import DetailsTabFrame
from frames.ScrollableFrame import ScrollableFrame
from frames.StatsFrame import StatsFrame
from frames.InfoFrame import InfoFrame
from frames.VideoPlayerFrame import VideoPlayerFrame
from frames.CodecFrame import CodecFrame
from frames.MangaReader import MangaReader
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

import threading
import concurrent.futures

from utils.FileManager import FileManager, DIR_TMP_COVERS, DIR_TMP_PAGES, DIR_TMP_CHARACTERS, DIR_IMG_ICON
from utils.utils import *

class SerieFrame(tk.Frame):
    # TODO : Afficher la barre de chargement uniquement quand on télécharge
    # TODO : Lecteur de manga intégré avoir à télécharger
    font_label_frame_details = ("Verdana",12)
    font_label_frame_info = ("Verdana", 12)
    
    def __init__(self, parent, serie_obj):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        # style
        self.s = ttk.Style()
        self.s.theme_use("default")
        #TODO add text inside progressbar https://stackoverflow.com/questions/24768090/progressbar-in-tkinter-with-a-label-inside

        # change the text of the progressbar, 
        # the trailing spaces are here to properly center the text
        self.s.configure("red.Horizontal.TProgressbar", text="Ready !", foreground="white")
        self.s.configure("red.Horizontal.TProgressbar", 
                    thickness=20,
                    background='#cf2410')
        # add the label to the progressbar style
        self.s.layout("red.Horizontal.TProgressbar",
                        [('red.Horizontal.TProgressbar.trough',
                        {'children': [('red.Horizontal.TProgressbar.pbar',
                                        {'side': 'left', 'sticky': 'ns'}),
                                        ("red.Horizontal.TProgressbar.label",   # label inside the bar
                                        {"sticky": ""})],
                        'sticky': 'nswe'})])
        # remove_arrow: https://stackoverflow.com/questions/48698283/can-you-remove-arrows-on-tkinter-scrollbar-widget-in-python
        self.s.layout('Vertical.TScrollbar', 
                        [('Vertical.Scrollbar.trough',
                        {'children': [('Vertical.Scrollbar.thumb', 
                                    {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'ns'})])
        self.s.configure("Vertical.TScrollbar", 
                         troughcolor="#1e1e1e",
                         background="#333333",
                         bordercolor="#1e1e1e")

        self.s.configure("TNotebook",
                         background="#252526",
                         borderwidth=0)

        self.s.configure('TNotebook.Tab',
                         padding= [10, 10],
                         font=("Verdana", 12),
                         background= "#333333",
                         foreground= "white")
        self.s.map("TNotebook.Tab",
                   background=[("selected", "#1e1e1e")],
                   font=[("selected", ("Verdana", 12, "bold"))])
        
        # variables
        self.serie_obj = serie_obj
        self.covers_img = []
        self.downloading = False

        # Widgets
        self.nav_bar = ttk.Notebook(self)
        self.nav_bar.bind('<<NotebookTabChanged>>', self.onChangeTab)

        self.frame_info = tk.Frame(self, borderwidth=0, width=30, background="#252526")

        # webview
        self.label_cover = WebView2(self.frame_info, 200, 293)
        self.label_cover.load_url(edit_url(self.serie_obj.volumes["1"][0]) if len(self.serie_obj.volumes)>0 else "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg") 
        self.info_status = InfoFrame(self.frame_info, key="Status", value="Finished" if (serie_obj.statut == "Terminé" or serie_obj.statut == "Completed")
                                                                    else "Publishing" if (serie_obj.statut == "En Cours" or serie_obj.statut == "Ongoing")
                                                                    else "On Hiatus" if serie_obj.statut == "Abandonné"
                                                                    else "Paused" if serie_obj.statut == "En Pause"
                                                                    else "Unknown")
        self.info_type = InfoFrame(self.frame_info, key="Type", value=serie_obj.type)
        self.info_annee = InfoFrame(self.frame_info, key="Year of release", value=serie_obj.annee_sortie)
        self.info_auteur = InfoFrame(self.frame_info, key="Author", value=serie_obj.auteur)
        self.info_dessinateur = InfoFrame(self.frame_info, key="Drawer", value=serie_obj.dessinateur)
        
        image = Image.open(DIR_IMG_ICON + "icon_left.png")
        tk_image_button = ImageTk.PhotoImage(image)
        self.covers_img.append(tk_image_button)
        self.button_back = tk.Button(self,
                                    background="#333333",
                                    image= tk_image_button, 
                                    command=self.return_searching_frame,
                                    borderwidth=0,
                                    cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        
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
        self.nav_bar.add(self.frame_resume, text="Details")

        self.progressbar = ttk.Progressbar(self, 
                                           style="red.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           mode="determinate", 
                                           value=0)
        
        self.frame_anime = None
        self.frame_codec = None
        
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
        
        self.label_cover.pack(side="top", padx=5, pady=5)
        self.info_status.pack(side="bottom", fill="x", padx=5)
        self.info_type.pack(side="bottom", fill="x", padx=5)
        self.info_annee.pack(side="bottom", fill="x", padx=5)
        self.info_dessinateur.pack(side="bottom", fill="x", padx=5)
        self.info_auteur.pack(side="bottom", fill="x", padx=5)
            
        self.progressbar.pack(side="bottom", fill="x")
        self.nav_bar.pack(side="right", fill="both", expand=True)

        self.launch_threads()
            
    def launch_threads(self):
        #self.thread_dl_cover = threading.Thread(target=self.download_cover_serie, daemon=True)
        #self.thread_dl_cover.start()

        if self.serie_obj.get_number_volumes() > 0:
            frame_volumes = ScrollableFrame(parent=self.nav_bar,
                                            app=self.parent,
                                            title_series=self.serie_obj.titre,
                                            cover_element=DIR_IMG_ICON+'cover_manga.png',
                                            onClickElement=self.onClickVolume,
                                            elements=self.serie_obj.get_list_numeros_volumes())

            self.nav_bar.add(frame_volumes, text="Volumes ("+ str(self.serie_obj.get_number_volumes()) +")")
            
            self.thread_show_volumes = threading.Thread(target=frame_volumes.show_elements,daemon=True)
            self.thread_show_volumes.start()
            
        if self.serie_obj.get_number_chapitres() > 0:
            frame_chapters = ScrollableFrame(parent=self.nav_bar,
                                             app=self.parent, 
                                             title_series=self.serie_obj.titre,
                                             cover_element=DIR_IMG_ICON+'cover_chapitre.png',
                                             onClickElement=self.onClickChapter,
                                             elements=self.serie_obj.get_list_numeros_chapitres())

            self.nav_bar.add(frame_chapters, text="Chapters ("+ str(self.serie_obj.get_number_chapitres()) +")")
            
            self.thread_show_chapters = threading.Thread(target=frame_chapters.show_elements,daemon=True)
            self.thread_show_chapters.start()

        if len(self.serie_obj.characters) > 0:
            characters = self.serie_obj.get_top20_characters()
            frame_characters = ScrollableFrame(parent=self.nav_bar,
                                               app=self.parent, 
                                               title_series=self.serie_obj.titre, 
                                               type_filter="advanced", 
                                               elements=characters)

            self.nav_bar.add(frame_characters, text="Characters")

            self.thread_dl_char = threading.Thread(target=self.download_characters_img, args=(frame_characters, characters), daemon=True)
            self.thread_dl_char.start()

            self.frame_codec = CodecFrame(parent=self.nav_bar,
                                          characters=characters, 
                                          title_series=self.serie_obj.titre)
            self.nav_bar.add(self.frame_codec, text="Codec") 

        if self.serie_obj.get_number_versions() > 0:
            self.frame_anime = VideoPlayerFrame(self.nav_bar,
                                                vf=self.serie_obj.seasons_vf, 
                                                vo=self.serie_obj.seasons_vostfr, 
                                                app=self.parent,
                                                serieframe=self,
                                                p_bar=self.progressbar)        
            
            self.nav_bar.add(self.frame_anime, text="Anime")

    def onChangeTab(self, event):
        current_tab = self.nav_bar.tab(self.nav_bar.select(), "text")

        if self.frame_anime:
            pass

        if current_tab == "Codec":
            if self.frame_codec and not self.frame_codec.is_running:
                self.frame_codec.set_gui()

    def return_searching_frame(self):
        # delete all covers in tmp dir
        #if self.thread_download_covers.is_alive():
            # kill thread
        #TODO : penser à kill le vlc si l'anime est en cours - appel à la fonction exit()
        if self.frame_anime:
            self.frame_anime.stop(quit=True)
            time.sleep(1.5)

        self.parent.show_searching_frame()
        FileManager().delete_tmp_files()
        
    def onClickVolume(self, event):
        if not self.downloading :
            if messagebox.askyesno("Download","Download this volume ?") :
                self.downloading = True
                
                pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the volume ?",
                                                        filetypes=[("Pdf files",".pdf")],
                                                        initialfile="volume_" + event.widget.cget("text"),
                                                        defaultextension='.pdf')
                
                if pdf_path.endswith(".pdf"):
                    self.show_progressbar()
                    
                    url_pages = self.serie_obj.volumes[event.widget.cget("text")]
                    
                    t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path), daemon=True)
                    t1.start()
                else :
                    messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
                    self.downloading = False
            else :
                # on affiche le MangaReader
                url_pages = self.serie_obj.volumes[event.widget.cget("text")]
                reader = MangaReader(self.parent, self.serie_obj.titre + " - Volume " + event.widget.cget("text"), url_pages)
        else :
            messagebox.showerror("Error", "Wait until your download finish")
    
    def onClickChapter(self, event):
        if not self.downloading :
            if messagebox.askyesno("Download","Download this chapter ?") :
                self.downloading = True
                
                
                pdf_path = filedialog.asksaveasfilename(title="Where do you want to save the chapter ?",
                                                        filetypes=[("Pdf files",".pdf")],
                                                        initialfile="chapter_" + event.widget.cget("text"),
                                                        defaultextension='.pdf')
                
                if pdf_path.endswith(".pdf"):
                    self.show_progressbar()
                    
                    # optimiser cette recherche ?
                    url_pages = self.serie_obj.chapitres[event.widget.cget("text")]
                    
                    t1 = threading.Thread(target=self.download_volume, args=(url_pages, pdf_path), daemon=True)
                    t1.start()
                else :
                    messagebox.showerror("Error","Please specify a filename that ends with '.pdf'")
                    self.downloading = False
            else :
                # on affiche le MangaReader
                url_pages = self.serie_obj.chapitres[event.widget.cget("text")]
                reader = MangaReader(self.parent, self.serie_obj.titre + " - Chapitre " + event.widget.cget("text"), url_pages)
        else:
            messagebox.showerror("Error", "Wait until your download finish")

    def download_characters_img(self, frame, characters):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            futures = []
            for rank, charac in enumerate(characters) :
                futures.append(pool.submit(download_element, 
                                        url_page=charac['url_image'], 
                                        filename=charac["path_image"].replace(DIR_TMP_CHARACTERS,"").split(".")[0],
                                        dir_tmp=DIR_TMP_CHARACTERS))
            
            for future in concurrent.futures.as_completed(futures):
                msg, filename = future.result()
        
        thread_show_characters = threading.Thread(target=frame.show_elements_plus, daemon=True)
        thread_show_characters.start()
                    
    def download_cover_serie(self):
        msg, filename = download_element(self.serie_obj.cover, 
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

    def show_progressbar(self):
        self.progressbar["value"] = 0
        self.downloading = True
        #self.button_back.config(state="disabled")

    def hide_progressbar(self):
        self.s.configure("red.Horizontal.TProgressbar", foreground='white', text="Ready !")
        self.progressbar["value"] = 0
        self.downloading = False
        #self.button_back.config(state="normal")
        self.update()  

    def download_volume(self, url_pages, pdf_path):
        self.progressbar.config(maximum=len(url_pages))
        n_downloaded = 0

        for num_page, url_img_page in enumerate(url_pages) :
            msg, filename = download_element(url_page=url_img_page,
                                filename=str(num_page+1),
                                dir_tmp=DIR_TMP_PAGES)
            
            if "GOOD" in msg:
                self.progressbar["value"] = num_page+1
                percentage = int(100*(num_page+1)/len(url_pages))
                self.s.configure("red.Horizontal.TProgressbar", foreground='white', text="Downloading pages {0}/{1} ({2}%)      ".format(num_page+1, len(url_pages),percentage))
                self.update()
                n_downloaded += 1
            else :
                messagebox.showerror("Error", "An error occurred while downloading the manga !\n" + msg)
                break
            
            # some delay
            time.sleep(random.random())

        """
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
                    percentage = int(100*(num_page+1)/len(url_pages))
                    self.s.configure("red.Horizontal.TProgressbar", foreground='white', text="Downloading ({0}%)      ".format(percentage))
                    self.update()
        """

        if n_downloaded == len(url_pages):            
            self.s.configure("red.Horizontal.TProgressbar", foreground='white', text="PDF Conversion in progress")
            convert_to_pdf(pdf_path)
            self.s.configure("red.Horizontal.TProgressbar", foreground='white', text="Conversion PDF completed")
            
            messagebox.showinfo("Done", pdf_path + " successfully downloaded !")
            webbrowser.open(pdf_path)

        self.hide_progressbar()
        FileManager().delete_tmp_pages()   