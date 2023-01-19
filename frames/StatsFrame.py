

import utils.mtTkinter as tk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils.utils import *

class StatsFrame(tk.Frame):
    
    font_label_frame_details = ("Verdana",12)
    font_label_frame_info = ("Verdana", 12, "bold")
    
    def __init__(self, parent, stats):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        #configuration pour avoir une frame sans bordure
        self.config(borderwidth=0)
        self.config(highlightthickness=0)

        self.notes = list(stats["Score Stats"].keys())
        self.values = [v["percentage"] for v in list(stats["Score Stats"].values())]

        self.plot_values()

    def plot_values(self):
        figure = plt.figure(figsize=(4,3), dpi=100)
        figure.add_subplot(111).barh(self.notes, self.values)

        chart = FigureCanvasTkAgg(figure, self)
        chart.get_tk_widget().pack()