from tkinter import *
from PIL import ImageGrab, ImageTk, Image
from color_tray import ColorTray

class AppWindow:
    def __init__(self, key_binds):
        self.is_running = False

        self.root = Tk()

        self.root.title("Graffiti")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")

        self.root.overrideredirect(True) # this removes window frame
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#add123")
        self.root.attributes("-transparentcolor", "#add123")

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
                                             tags = ("ui", "mouse"))

        self.cheatsheet = Listbox(self.canvas, height = len(key_binds) + 2,
                                  borderwidth = 3, relief = RIDGE,
                                  bg = "#242424", fg = "#cccccc",
                                  selectbackground = "#ed213c")
        self.cheatsheet.insert(1, "")
        for key in key_binds:
            self.cheatsheet.insert(END, f"   {key_binds[key]} : {key}")

        self.canvas.create_window(self.root.winfo_screenwidth() - 40, 40, 
                                  window = self.cheatsheet,
                                  anchor = "ne", tags = ("ui", "cs"))

        self.mouse_offset = [0, 0]
        self.selected = 0

        self.col_tray = ColorTray(self)
        self.canvas.create_window(self.root.winfo_screenwidth() - 40,
                                  60 + 20 * len(key_binds), 
                                  window = self.col_tray.get_widget(),
                                  anchor = "ne", tags = ("ui", "ct"))

        self.scrnshot_x = 0
        self.scrnshot_y = 0
        self.imgs = []


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

    def paint_tray(self, abs_x, abs_y):
        self.col_tray.paint(abs_x, abs_y)

    def preview_draw(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
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

    def get_drawings(self):
        self.canvas.tag_raise("ui")
        items = self.canvas.find_all()
        return items[:len(items) - len(self.canvas.find_withtag("ui"))]

    def clear(self):
        for item in self.get_drawings():
            self.canvas.delete(item)
        self.history.clear()
        self.imgs.clear()
        self.current_tag = "0"

    def hide(self):
        new_state = "normal" if self.hidden else "hidden"
        for item in self.get_drawings():
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

    def init_scrnshot(self, x, y):
        if self.history:
            for tag in self.history:
                for item in self.canvas.find_withtag(tag):
                    self.canvas.delete(item)
            self.history.clear()

        self.canvas.itemconfig(self.hover, state = "hidden")
        self.scrnshot_x = x
        self.scrnshot_y = y

    def take_scrnshot(self, x, y):
        x2 = x
        y2 = y
        if self.scrnshot_x > x2: (self.scrnshot_x, x2) = (x2, self.scrnshot_x)
        if self.scrnshot_y > y2: (self.scrnshot_y, y2) = (y2, self.scrnshot_y)
        img = ImageGrab.grab((self.scrnshot_x, self.scrnshot_y, x2, y2))
        tk_img = ImageTk.PhotoImage(img)
        self.imgs.append(tk_img)
        self.canvas.create_image((self.scrnshot_x, self.scrnshot_y),
                                 image = tk_img,
                                 anchor = "nw",
                                 tags = (f"{tk_img}"))
        self.canvas.tag_raise("mouse")
        self.canvas.itemconfig(self.hover, state = "normal")

    def eyedrop(self, x, y):
        img = ImageGrab.grab()
        r, g, b = img.getpixel((x, y))
        self.col = self.col_tray.set_rgb(r, g, b)
        self.canvas.itemconfig(self.hover, outline = self.col)

    def update_cheatsheet(self, i):
        self.cheatsheet.selection_clear(0, END)
        self.cheatsheet.select_set(i + 1)

    def find_widget(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.tag_raise("ui")

        stack = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        if len(stack) == 0:
            return "mouse"

        top = stack[-1]
        top_tags = self.canvas.gettags(top)
        if top_tags[0] != "ui":
            return "mouse"
        
        if top_tags[1] == "ct":
            if self.col_tray.overlapping_canvas(abs_y):
                return "tray"
            else:
                self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                 self.canvas.coords(top)[1] - y]
                self.selected = top
                return ""
        if top_tags[1] != "mouse" and top_tags[0] == "ui":
            self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                 self.canvas.coords(top)[1] - y]
            self.selected = top
            return ""
        else:
            return "mouse"

    def drag_widget(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        
        self.canvas.coords(self.selected, x + self.mouse_offset[0],
                           y + self.mouse_offset[1])

    def hide_ui(self, is_hidden):
        if is_hidden:
            self.canvas.itemconfig(self.hover, state = "normal")
            self.root.attributes("-alpha", 1.)
        else:
            self.canvas.itemconfig(self.hover, state = "hidden")
            self.root.attributes("-alpha", 0.5)

    def update_hsl(self, h_i, s_i, l_i):
        self.col = self.col_tray.update_hsl(h_i, s_i, l_i)
        self.canvas.itemconfig(self.hover, outline = self.col)

