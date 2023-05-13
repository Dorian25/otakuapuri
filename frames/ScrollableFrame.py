# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 18:10:45 2022

@author: Dorian
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from utils.FileManager import DIR_IMG_ICON
from tkinter.messagebox import showwarning
from utils.Dialogue import Dialogue

class ScrollableFrame(tk.Frame):
# source = https://stackoverflow.com/questions/68362391/using-mousewheel-on-scrollable-frame/68363151#68363151

    def __init__(self, parent, app, title_series, cover_element=None, onClickElement=None, elements=[], type_filter="basic"):
        tk.Frame.__init__(self, parent)

        self.app = app
        self.parent = parent
        self.config(borderwidth=0)
        self.config(highlightthickness=0)
        self.config(bg="#1e1e1e")

        self.credit_talk = 5
        self.current_dialogue = None

        self.title_series = title_series
        self.elements = elements
        self.onClickElement = onClickElement
        self.cover_element = cover_element
        self.covers_storage = []

        listeOptions = ['Sorted from newest to oldest', 'Sorted from oldest to newest']
        self.var_filter = tk.StringVar()

        if type_filter == "advanced":
            listeOptions = ["Sorted by name : A-Z", "Sorted by name : Z-A", "Sorted by favorites : ascending", "Sorted by favorites : descending"]
            self.var_filter.set("Sorted by favorites : descending")
        else :
            self.var_filter.set('Sorted from newest to oldest')

        self.filter = ttk.Combobox(self, 
                                   height=30, 
                                   width=30, 
                                   textvariable=self.var_filter, 
                            )
        self.filter.bind('<<ComboboxSelected>>', self.onChangeFilter)
        self.filter['state'] = 'readonly'
        self.filter['values'] = listeOptions
        
        self.canvas = tk.Canvas(self, 
                        bg="#1e1e1e",
                        bd=0, 
                        highlightthickness=0)
        # zone d'affichage // ajouter element ici
        self.viewport = tk.Frame(self.canvas,
                                bg="#1e1e1e", 
                                borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, 
                                orient="vertical", 
                                command=self.canvas.yview,
                                style="Vertical.TScrollbar")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # pack // place widgets
        self.filter.pack(side="top", anchor="ne", padx=40)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_window = self.canvas.create_window((0, 0), 
                                                        window=self.viewport, 
                                                        anchor="nw")
        #bind an event whenever the size of the viewport frame changes.
        self.viewport.bind("<Configure>", self.onFrameConfigure)
        #bind an event whenever the size of the viewport frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)

        self.viewport.bind('<Enter>', self._bound_to_mousewheel)
        self.viewport.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #whenever the size of the frame changes, alter the scroll region respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        #whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)
    
    def onEnter(self, event) :
        event.widget["relief"] = "groove"
     
    def onLeave(self, event) :
        event.widget["relief"] = "flat"

    def delete_widgets(self):
        for label in self.viewport.grid_slaves():
            label.destroy()

    def onChangeFilter(self, event):
        self.delete_widgets()
        self.covers_storage = []

        if self.var_filter.get() == "Sorted from oldest to newest" :
            self.elements = sorted(self.elements, key=float)  
            self.show_elements()
        elif self.var_filter.get() == "Sorted from newest to oldest" :
            self.elements = sorted(self.elements, key=float, reverse=True)
            self.show_elements()
        elif self.var_filter.get() == "Sorted by name : A-Z":
            self.elements = sorted(self.elements, key= lambda d: d['name'])
            self.show_elements_plus()
        elif self.var_filter.get() == "Sorted by name : Z-A":
            self.elements = sorted(self.elements, key= lambda d: d['name'], reverse=True)
            self.show_elements_plus()
        elif self.var_filter.get() == "Sorted by favorites : ascending":
            self.elements = sorted(self.elements, key= lambda d: d['n_favorites'])
            self.show_elements_plus()
        elif self.var_filter.get() == "Sorted by favorites : descending":
            self.elements = sorted(self.elements, key= lambda d: d['n_favorites'], reverse=True)
            self.show_elements_plus()

    def onClickCharacter(self, charactername, characterimg):
        pass
        """
        if self.credit_talk > 0 :
            if self.current_dialogue:
                if self.current_dialogue.winfo_exists(): # un 
                    self.current_dialogue.destroy()
            
            self.credit_talk -= 1
            self.current_dialogue = Dialogue(self.app, charactername, characterimg, self.title_series)
        else :
            showwarning("0 credits", "You don't have enough credits ! Try later !")
        """
        
    def show_elements_plus(self):
        # ideas
        ## change color cover grayscale if already rade
        
        total_elements = len(self.elements)
        n_col = 5
        n_row = total_elements // n_col
        n_col_rest = total_elements - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    label_text = self.elements[(i*n_col)+j]["name"]

                    image = Image.open(self.elements[(i*n_col)+j]["path_image"])
                    image_resize = image.resize((100, 140))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_storage.append(tk_image)
                    
                    label_element = tk.Label(self.viewport, 
                                            text=label_text, 
                                            image=tk_image,
                                            font=("Verdana",13),
                                            fg="white",
                                            bg="#1e1e1e",
                                            compound='top',
                                            wraplength=100,
                                            highlightthickness=0, 
                                            borderwidth=0)
                    #label_element.bind("<Button-1>", 
                    #                   lambda event, 
                    #                   charactername=label_text, 
                    #                   characterimg=self.elements[(i*n_col)+j]["path_image"] : self.onClickCharacter(charactername, characterimg))
                    
                    label_element.grid(row=i,column=j, padx=30, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                label_text = self.elements[(n_row*n_col)+j]["name"]
                
                image = Image.open(self.elements[(n_row*n_col)+j]["path_image"])
                image_resize = image.resize((100,140))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_storage.append(tk_image)
                
                label_volume = tk.Label(self.viewport, 
                                        text=label_text, 
                                        image=tk_image,
                                        font=("Verdana",13),
                                        fg="white",
                                        bg="#1e1e1e",
                                        compound='top',
                                        wraplength=100,
                                        highlightthickness=0, 
                                        borderwidth=0)
                #label_element.bind("<Button-1>", 
                #                   lambda event,
                #                   charactername=label_text,
                #                   characterimg=self.elements[(n_row*n_col)+j]["path_image"]: self.onClickCharacter(charactername, characterimg))
                
                label_volume.grid(row=n_row,column=j, padx=30, pady=20, sticky='ew')
                self.update()

    def show_elements(self):
        #TODO change color cover grayscale if already rade

        # Download cover manga :
        # url_cover = self.serie_obj.volumes[num_volume][0]
        # get_cover_manga(title_manga, n_vol, url_cover, download_dir)
        # cover_path = get_cover_manga(self.serie_obj.titre.lower().replace(" ","_"),
        #                            num_volume,
        #                            url_cover, 
        #                            DIR_TMP_COVERS)
        
        total_elements = len(self.elements)
        n_col = 5
        n_row = total_elements // n_col
        n_col_rest = total_elements - (n_row*n_col)
        
        if n_row > 0:
            for i in range(n_row):
                for j in range(n_col) :
                    label_text = self.elements[(i*n_col)+j]

                    image = Image.open(self.cover_element)
                    image_resize = image.resize((110, 150))
                    tk_image = ImageTk.PhotoImage(image_resize)
                    self.covers_storage.append(tk_image)
                    
                    label_element = tk.Label(self.viewport, 
                                            text=label_text, 
                                            image=tk_image,
                                            font=("Impact",13),
                                            compound='top',
                                            borderwidth=2, 
                                            fg="white",
                                            bg="#1e1e1e",
                                            relief="flat",
                                            cursor="@"+DIR_IMG_ICON+"aero_link.cur")
                    
                    label_element.bind("<Button-1>", self.onClickElement)
                    label_element.bind("<Enter>", self.onEnter)
                    label_element.bind("<Leave>", self.onLeave)
                    
                    label_element.grid(row=i,column=j, padx=20, pady=20, sticky='ew')
                    self.update()
                
        if n_col_rest > 0 :
            for j in range(n_col_rest) :
                label_text = self.elements[(n_row*n_col)+j]
                
                image = Image.open(self.cover_element)
                image_resize = image.resize((110, 150))
                tk_image = ImageTk.PhotoImage(image_resize)
                self.covers_storage.append(tk_image)
                
                label_element = tk.Label(self.viewport, 
                                        text=label_text, 
                                        image=tk_image,
                                        font=("Impact",13),
                                        compound='top',
                                        borderwidth=2, 
                                        fg="white",
                                        bg="#1e1e1e",
                                        relief="flat",
                                        cursor="@"+DIR_IMG_ICON+"aero_link.cur")
                
                label_element.bind("<Button-1>", self.onClickElement)
                label_element.bind("<Enter>", self.onEnter)
                label_element.bind("<Leave>", self.onLeave)
                
                label_element.grid(row=n_row,column=j, padx=20, pady=20, sticky='ew')
                self.update() 