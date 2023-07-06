import tkinter as tk
from tkinter import ttk
from tkwebview2.tkwebview2 import WebView2
from utils.FileManager import DIR_IMG_ICON
from utils.utils import edit_url
from PIL import Image, ImageTk

class MangaReader(tk.Toplevel):
    def __init__(self, parent, title, list_pages):
        tk.Toplevel.__init__(self, parent)

        self.title("Manga Reader - " + title)

        self.parent = parent
        self.list_pages = list_pages
        self.cursor = 0

        self.go()

    def go(self):
        try:
            self.__set_gui()
        except Exception as err:
            print(err)

    def __set_gui(self):
        # webview
        self.webview_frame = WebView2(self, 500, 800)
        self.webview_frame.pack(side='top', fill='both', expand=True)
        self.webview_frame.load_url(edit_url(self.list_pages[self.cursor]))

        # cursor
        self.cursor_frame = tk.Frame(self, background="#1e1e1e")
        self.cursor_frame.pack(side="bottom", fill="x")

        
        self.tk_img_next = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "next_page.png"))
        self.next_btn = tk.Button(self.cursor_frame, text="Next", 
                                  command=self.next, 
                                  background="#1e1e1e",
                                  borderwidth=0,
                                  image= self.tk_img_next,
                                  cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.next_btn.pack(side="left", padx=(150,0))

        self.current_page_var = tk.StringVar()
        self.current_page_var.set(str(self.cursor+1))
        self.current_page_selector = ttk.Combobox(self.cursor_frame, 
                                                  height=30, 
                                                  width=1, 
                                                  textvariable=self.current_page_var)
        self.current_page_selector.bind('<<ComboboxSelected>>', self.onChangePage)
        self.current_page_selector['values'] = [str(i+1) for i in range(len(self.list_pages))]
        self.current_page_selector.pack(side="left", fill="both", expand=True)

        self.slash_label = tk.Label(self.cursor_frame,
                                         text="/",
                                         fg="#7f7f7f",
                                         bg="#1e1e1e")
        self.slash_label.pack(side="left", fill="both", expand=True)

        self.total_page_label = tk.Label(self.cursor_frame,
                                         text=str(len(self.list_pages)),
                                         fg="#7f7f7f",
                                         bg="#1e1e1e")
        self.total_page_label.pack(side="left", fill="both", expand=True)

        self.tk_img_prev = ImageTk.PhotoImage(Image.open(DIR_IMG_ICON + "prev_page.png"))                             
        self.prev_btn = tk.Button(self.cursor_frame, text="Prev", 
                                  command=self.prev,
                                  background="#1e1e1e",
                                  borderwidth=0,
                                  image=self.tk_img_prev,
                                  cursor="@"+DIR_IMG_ICON+"aero_link.cur")
        self.prev_btn.pack(side="right", padx=(0,150))
        
    def onChangePage(self, event):
        self.cursor = int(self.current_page_var.get())-1
        self.webview_frame.load_url(edit_url(self.list_pages[self.cursor]))

    def next(self):
        if self.cursor < len(self.list_pages):
            self.cursor += 1
            self.webview_frame.load_url(edit_url(self.list_pages[self.cursor]))
            self.current_page_var.set(str(self.cursor + 1))
        else : 
            self.destroy()

    def prev(self):
        if self.cursor > 0 :
            self.cursor -= 1
            self.webview_frame.load_url(edit_url(self.list_pages[self.cursor]))
            self.current_page_var.set(str(self.cursor + 1))