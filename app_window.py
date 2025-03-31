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
        self.col = "#ff1d0d"

        self.canvas.pack()

        self.hidden = False
        self.current_tag = "0"
        self.history = []
        self.prev_x = 0
        self.prev_y = 0

        self.hover = self.canvas.create_oval(0, 0, 
                                             self.rad * 2, self.rad * 2,
                                             outline = self.col,
                                             tags = ("ui"))

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
        if self.history:
            for tag in self.history:
                for item in self.canvas.find_withtag(tag):
                    self.canvas.delete(item)
            self.history.clear()

        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.create_oval(x - self.rad, y - self.rad,
                                x + self.rad, y + self.rad,
                                fill = self.col, outline="",
                                tags = ("a" + self.current_tag))
        self.prev_x = x
        self.prev_y = y

    def preview_draw(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.itemconfig(self.hover, outline = self.col)
        self.canvas.coords(self.hover, x - self.rad, y - self.rad,
                           x + self.rad, y + self.rad,)
        self.canvas.tag_raise("ui")

    def paint_line(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()

        self.canvas.create_line(self.prev_x, self.prev_y, x, y,
                                capstyle = "round",
                                fill = self.col, width = self.rad * 2,
                                tags = ("a" + self.current_tag))
        self.prev_x = x
        self.prev_y = y

    def clear(self):
        self.canvas.tag_raise("ui")
        items = self.canvas.find_all()
        items = items[:len(items) - len(self.canvas.find_withtag("ui"))]

        for item in items:
            self.canvas.delete(item)
        self.history.clear()
        self.current_tag = "0"

    def hide(self):
        new_state = "normal" if self.hidden else "hidden"
        for item in self.canvas.find_all():
            self.canvas.itemconfig(item, state = new_state)
        self.hidden = not self.hidden

    def update_tag(self, i):
        self.current_tag = str(int(self.current_tag) + i)

    def undo(self):
        if self.current_tag != "0":
            for item in self.canvas.find_withtag("a" + self.current_tag):
                self.canvas.itemconfig(item, state = "hidden")
            self.history.append("a" + self.current_tag)
            self.update_tag(-1)

    def redo(self):
        if self.history: # empty lists return false
            for item in self.canvas.find_withtag(self.history[-1]):
                self.canvas.itemconfig(item, state = "normal")
            del self.history[-1]
            self.update_tag(1)

    def update_pen(self, i):
        self.rad = min(max(self.rad + i, 3), 30)

        coords = self.canvas.coords(self.hover)
        coords = [(coords[2] - coords[0]) / 2 + coords[0], 
                  (coords[3] - coords[1]) / 2 + coords[1]]

        self.preview_draw(coords[0], coords[1])
