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

        self.cheatsheet = Listbox(self.canvas, height = len(key_binds) + 5,
                                  borderwidth = 3, relief = RIDGE,
                                  bg = "#242424", fg = "#cccccc",
                                  selectbackground = "#ed213c")
        self.cheatsheet.insert(1, "")
        self.cheatsheet.insert(2, "   Use CTRL to interact")
        self.cheatsheet.insert(3, "   when not focused")
        self.cheatsheet.insert(4, "")
        for key in key_binds:
            self.cheatsheet.insert(END, f"   {key_binds[key]} : {key}")

        self.canvas.create_window(self.root.winfo_screenwidth() - 40, 40, 
                                  window = self.cheatsheet,
                                  anchor = "ne", tags = ("ui", "cs"))

        self.mouse_offset = [0, 0]
        self.selected = 0

        self.col_tray = ColorTray(self)
        self.canvas.create_window(self.root.winfo_screenwidth() - 40,
                                  100 + 20 * len(key_binds), 
                                  window = self.col_tray.get_widget(),
                                  anchor = "ne", tags = ("ui", "ct"))

        self.scrnshot_x = 0
        self.scrnshot_y = 0
        self.imgs = []


    def clear(self):
        for item in self.get_drawings():
            self.canvas.delete(item)
        self.history.clear()
        self.imgs.clear()
        self.current_tag = "0"
        self.hidden = False

    def destroy(self):
        self.is_running = False

    def drag_widget(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        
        self.canvas.coords(self.selected, x + self.mouse_offset[0],
                           y + self.mouse_offset[1])

    def eyedrop(self, x, y):
        img = ImageGrab.grab()
        r, g, b = img.getpixel((x, y))
        self.col = self.col_tray.set_rgb(r, g, b)
        self.canvas.itemconfig(self.hover, outline = self.col)

    def find_widget(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.tag_raise("ui")

        stack = self.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        if len(stack) == 0:
            return "mouse"

        top = stack[-1]
        top_tags = self.canvas.gettags(top)

        if top_tags[0] == "scr":
            self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                 self.canvas.coords(top)[1] - y]
            self.selected = top
            return "screen shot"
        elif top_tags[0] != "ui":
            return "mouse"
        elif top_tags[1] == "ct":
            if self.col_tray.overlapping_canvas(abs_y):
                return "tray"
            else:
                self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                 self.canvas.coords(top)[1] - y]
                self.selected = top
                return ""
        elif top_tags[1] != "mouse":
            self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                 self.canvas.coords(top)[1] - y]
            self.selected = top
            return ""
        else:
            if len(stack) > 1:
                top = stack[-2]
                top_tags = self.canvas.gettags(top)
                if top_tags[0] == "scr":
                    self.mouse_offset = [self.canvas.coords(top)[0] - x,
                                         self.canvas.coords(top)[1] - y]
                    self.selected = top
                    return "screen shot"
            return "mouse"

    def get_drawings(self):
        self.canvas.tag_raise("ui")
        items = self.canvas.find_all()
        return items[:len(items) - len(self.canvas.find_withtag("ui"))]

    def hide(self):
        new_state = "normal" if self.hidden else "hidden"
        for item in self.get_drawings():
            self.canvas.itemconfig(item, state = new_state)
        self.hidden = not self.hidden

    def hide_ui(self, is_hidden):
        if is_hidden:
            self.canvas.itemconfig(self.hover, state = "normal")
            self.root.attributes("-alpha", 1.)
        else:
            self.canvas.itemconfig(self.hover, state = "hidden")
            self.root.attributes("-alpha", 0.5)

    def hide_window(self, hide):
        if hide:
            self.root.attributes("-alpha", 0.)
        else:
            self.root.attributes("-alpha", 1.)

    def init_scrnshot(self, x, y):
        if self.history:
            for tag in self.history:
                for item in self.canvas.find_withtag(tag):
                    self.canvas.delete(item)
            self.history.clear()

        self.canvas.itemconfig(self.hover, state = "hidden")
        self.scrnshot_x = x
        self.scrnshot_y = y

        scrn_x = x - self.canvas.winfo_rootx()
        scrn_y = y - self.canvas.winfo_rooty()

        self.canvas.create_rectangle(scrn_x, scrn_y, scrn_x + 1, scrn_y + 1,
                                   fill = "#add123",
                                   outline = "#344ceb",
                                   tags = ("drag"))

    def inputloop(self):
        if self.is_running:
            self.root.after(10, self.inputloop)
        else:
            self.root.destroy()

    def invert_cheatsheet(self, yes_invert):
        if yes_invert: 
            self.cheatsheet.configure(bg = "#ed213c",
                                      fg = "#242424",
                                      selectbackground = "#242424")
        else:
            self.cheatsheet.configure(bg = "#242424",
                                      fg = "#cccccc",
                                      selectbackground = "#ed213c")

    def mainloop(self):
        self.is_running = True
        self.inputloop()
        self.root.mainloop()

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

    def paint_line(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()

        self.canvas.create_line(self.prev_x, self.prev_y, x, y,
                                capstyle = "round",
                                fill = self.col, width = self.rad * 2,
                                tags = ("a" + self.current_tag))
        self.prev_x = x
        self.prev_y = y

    def preview_draw(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.coords(self.hover, x - self.rad, y - self.rad,
                           x + self.rad, y + self.rad,)
        self.canvas.tag_raise("ui")

    def redo(self):
        if self.history: # empty lists return false
            for item in self.canvas.find_withtag(self.history[-1]):
                self.canvas.itemconfig(item, state = "normal")
            del self.history[-1]
            self.update_tag(1)

    def take_scrnshot(self, x, y):
        self.canvas.delete(self.canvas.find_withtag("drag")[0])
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
                                 tags = ("scr", "a" + self.current_tag))
        self.canvas.tag_raise("ui")
        self.canvas.itemconfig(self.hover, state = "normal")

    def undo(self):
        if self.current_tag != "0":
            for item in self.canvas.find_withtag("a" + self.current_tag):
                self.canvas.itemconfig(item, state = "hidden")
            self.history.append("a" + self.current_tag)
            self.update_tag(-1)

    def update_cheatsheet(self, i):
        self.cheatsheet.selection_clear(0, END)
        self.cheatsheet.select_set(i + 4)

    def update_drag(self, abs_x, abs_y):
        x = self.scrnshot_x - self.canvas.winfo_rootx()
        y = self.scrnshot_y - self.canvas.winfo_rooty()
        x2 = abs_x - self.canvas.winfo_rootx()
        y2 = abs_y - self.canvas.winfo_rooty()
        if x > x2: (x, x2) = (x2, x)
        if y > y2: (y, y2) = (y2, y)
        self.canvas.coords(self.canvas.find_withtag("drag")[0],
                           x, y, x2, y2)

    def update_oklch(self, l_i, c_i, h_i):
        self.col = self.col_tray.update_oklch(l_i, c_i, h_i)
        self.canvas.itemconfig(self.hover, outline = self.col)

    def update_pen(self, i):
        self.rad = min(max(self.rad + i, 3), 30)

        coords = self.canvas.coords(self.hover)
        coords = [(coords[2] - coords[0]) / 2 + coords[0], 
                  (coords[3] - coords[1]) / 2 + coords[1]]

        self.preview_draw(coords[0], coords[1])

    def update_tag(self, i):
        self.current_tag = str(int(self.current_tag) + i)

