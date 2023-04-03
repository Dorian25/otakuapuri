


import tkinter as tk

class InfoBulle(tk.Toplevel):
    def __init__(self, object, info, w=230, h=35, x=-100, y=-100):
        tk.Toplevel.__init__(self)

        self.geometry(f'{w}x{h}+{x}+{y}')

        self.overrideredirect(True)

        self.canvas = tk.Canvas(self, 
                                width=w, 
                                height=h, 
                                bg='orange',
                                highlightthickness=0)
        self.canvas.create_rectangle(0,0,w,h, fill="#333333")
        self.canvas.place(x=0, y=0)

        self.wm_attributes('-transparentcolor', 'orange')

        self.canvas.create_text(15, 17, text=info, fill='white', anchor="w")

        object.bind('<Enter>', self.show_infobulle)
        object.bind('<Leave>', self.hide_infobulle)


    def show_infobulle(self, event):
        x0, y0 = event.x_root - event.x - 20, event.y_root - event.y - 20
        self.geometry(f'+{x0}+{y0}')

    def hide_infobulle(self, event):
        x0, y0 = -100, -100
        self.geometry(f'+{x0}+{y0}')