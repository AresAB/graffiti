from tkinter import *

class AppWindow:
    def __init__(self):
        self.is_running = False

        self.root = Tk()

        self.root.title("Graffiti")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.root.overrideredirect(True) # this removes window frame
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#add123")
        self.root.attributes("-transparentcolor", "#add123")

        #lbl = Label(self.root, text = "test", bg = "red", height = 30, width = 20)
        #lbl.pack()

        self.canvas = Canvas(self.root, 
                             width = self.root.winfo_screenwidth(), 
                             height = self.root.winfo_screenheight(),
                             bg = "#add123")

        self.rad = 3
        self.col = "#000fff000"

        self.canvas.pack()

        self.hidden = False

    def mainloop(self):
        self.is_running = True
        self.inputloop()
        self.root.mainloop()

    def inputloop(self):
        if self.is_running:
            self.root.after(10, self.inputloop)
        else:
            self.root.destroy()

    def destroy(self):
        self.is_running = False

    def paint(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.create_oval(x - self.rad, y - self.rad,
                                x + self.rad, y + self.rad,
                                fill = self.col, outline="")

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def hide(self):
        new_state = "normal" if self.hidden else "hidden"
        for item in self.canvas.find_all():
            self.canvas.itemconfig(item, state = new_state)
        self.hidden = not self.hidden
