from tkinter import *

class AppWindow:
    def __init__(self):
        self.root = Tk()

        self.root.title("Graffiti")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.root.overrideredirect(True) # this removes self.root frame
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#add123")
        self.root.attributes("-transparentcolor", "#add123")

        lbl = Label(self.root, text = "test", bg = "red", height = 30, width = 20)
        lbl.pack(side = TOP)

    def setup(self):
        self.root.bind("<x>", self.x_pressed)

    def run(self):
        self.setup()
        self.root.mainloop()

    def x_pressed(self, event):
        self.root.destroy()
