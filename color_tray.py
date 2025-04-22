from tkinter import *
import math

class ColorTray:
    def __init__(self, root):
        self.parent = root
        self.frame = Frame(self.parent.canvas, borderwidth = 3,
                           relief = RIDGE)

        self.hex = self.parent.col
        self.rgb = hex_to_rgb(self.hex)
        self.oklch = rgb_to_oklch(self.rgb[0], self.rgb[1], self.rgb[2])

        self.hex_l = Label(self.frame, text = self.hex,
                           bg = "#242424", fg = "#cccccc")
        self.hex_l.pack(fill = 'both')

        self.col_display = Label(self.frame, bg = self.parent.col)
        self.col_display.pack(fill = 'both')

        self.lum_l = Label(self.frame, 
                           text = f"Luminance: {int(self.oklch[0] * 100)}%",
                           bg = "#242424", fg = "#cccccc")
        self.lum_l.pack(fill = 'both')
        
        self.chroma_l = Label(self.frame, 
                              text = f"Chroma: {int(self.oklch[1] * 100)}%",
                              bg = "#242424", fg = "#cccccc")
        self.chroma_l.pack(fill = 'both')

        self.hue_l = Label(self.frame, 
                           text = f"Hue: {int(self.oklch[2] * (180 / math.pi))} deg",
                           bg = "#242424", fg = "#cccccc")
        self.hue_l.pack(fill = 'both')

        self.canvas = Canvas(self.frame, width = 80, height = 120)
        self.canvas.pack(fill = 'both')

        self.rad = 7


    def get_widget(self):
        return self.frame

    def overlapping_canvas(self, abs_y):
        if abs_y > self.canvas.winfo_rooty():
            return True
        return False

    def paint(self, abs_x, abs_y):
        x = abs_x - self.canvas.winfo_rootx()
        y = abs_y - self.canvas.winfo_rooty()
        self.canvas.create_oval(x - self.rad, y - self.rad,
                                x + self.rad, y + self.rad,
                                fill = self.parent.col, outline="")

    def update_oklch(self, l_i, c_i, h_i):
        self.oklch[0] += l_i
        self.oklch[0] = min(max(self.oklch[0], 0), 1)
        self.oklch[1] += c_i
        self.oklch[1] = min(max(self.oklch[1], 0), 1)
        self.oklch[2] += h_i
        self.oklch[2] %= 361 * (math.pi / 180)
        if self.oklch[2] < 0: self.oklch[2] = (math.pi * 2.) + self.oklch[2]

        self.lum_l.config(text = f"Luminance: {int(self.oklch[0] * 100)}%")
        self.chroma_l.config(text = f"Chroma: {int(self.oklch[1] * 100)}%")
        self.hue_l.config(text = f"Hue: {int(self.oklch[2] * (180 / math.pi))} deg")

        self.rgb = oklch_to_rgb(self.oklch[0], self.oklch[1], self.oklch[2])

        self.hex = rgb_to_hex(self.rgb[0], self.rgb[1], self.rgb[2])
        self.col_display.config(bg = self.hex)
        self.hex_l.config(text = self.hex)

        return self.hex

    def set_rgb(self, r, g, b):
        self.rgb = [r, g, b]
        self.oklch = rgb_to_oklch(self.rgb[0], self.rgb[1], self.rgb[2])
        if self.oklch[2] < 0: self.oklch[2] = (math.pi * 2.) + self.oklch[2]

        self.lum_l.config(text = f"Luminance: {int(self.oklch[0] * 100)}%")
        self.chroma_l.config(text = f"Chroma: {int(self.oklch[1] * 100)}%")
        self.hue_l.config(text = f"Hue: {int(self.oklch[2] * (180 / math.pi))} deg")

        self.hex = rgb_to_hex(self.rgb[0], self.rgb[1], self.rgb[2])
        self.col_display.config(bg = self.hex)
        self.hex_l.config(text = self.hex)

        return self.hex

def hex_to_rgb(hex_code):
    return [int(hex_code[1:3], 16), 
            int(hex_code[3:5], 16), 
            int(hex_code[5:], 16)]

def rgb_to_hsl(r, g, b):
    r_p = r / 255
    g_p = g / 255
    b_p = b / 255

    c_max = max(r_p, g_p, b_p)
    c_min = min(r_p, g_p, b_p)
    delta = c_max - c_min

    if delta == 0:
        h = 0
    elif c_max == r_p:
        h = 60 * ((g_p - b_p)/delta % 6)
    elif c_max == g_p:
        h = 60 * ((b_p - r_p)/delta + 2)
    else:
        h = 60 * ((r_p - g_p)/delta + 4)

    l = (c_max + c_min) / 2

    if delta == 0:
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))

    return [round(h) * 1., round(s * 100) * 0.01, round(l * 100) * 0.01]

def hsl_to_rgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c * 0.5

    if h < 60:
        rgb_p = [c, x, 0]
    elif h < 120:
        rgb_p = [x, c, 0]
    elif h < 180:
        rgb_p = [0, c, x]
    elif h < 240:
        rgb_p = [0, x, c]
    elif h < 300:
        rgb_p = [x, 0, c]
    else:
        rgb_p = [c, 0, x]

    rgb = [int((rgb_p[0] + m) * 255), int((rgb_p[1] + m) * 255), int((rgb_p[2] + m) * 255)]

    return rgb

def rgb_to_hex(r, g, b):
    r_hex = hex(r)[2:]
    if len(r_hex) < 2: r_hex = "0" + r_hex
    g_hex = hex(g)[2:]
    if len(g_hex) < 2: g_hex = "0" + g_hex
    b_hex = hex(b)[2:]
    if len(b_hex) < 2: b_hex = "0" + b_hex

    return "#" + r_hex + g_hex + b_hex

def rgb_to_oklch(r, g, b):
    r_ = r / 255
    g_ = g / 255
    b_ = b / 255

    l = 0.4122214708 * r_ + 0.5363325363 * g_ + 0.0514459929 * b_
    m = 0.2119034982 * r_ + 0.6806995451 * g_ + 0.1073969566 * b_
    s = 0.0883024619 * r_ + 0.2817188376 * g_ + 0.6299787005 * b_

    l_ = l ** (1/3)
    m_ = m ** (1/3)
    s_ = s ** (1/3)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    C = (a * a + b * b) ** 0.5
    h = math.atan2(b, a)

    return [round(L * 100) * 0.01, round(C * 100) * 0.01, round(h * 100) * 0.01]

def oklch_to_rgb(L, C, h):
    a = C * math.cos(h)
    b = C * math.sin(h)

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    return [min(max(int((4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s) * 255), 0), 255),
            min(max(int((-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s) * 255), 0), 255),
            min(max(int((-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s) * 255), 0), 255)]
