from tkinter import *

class ColorTray:
    def __init__(self, root):
        self.parent = root
        self.frame = Frame(self.parent.canvas, borderwidth = 3,
                           relief = RIDGE)

        self.col_display = Label(self.frame, text = "   ",
                                 bg = self.parent.col)
        self.col_display.pack(fill = 'both')

        self.rgb = hex_to_rgb(self.parent.col)
        self.hsl = rgb_to_hsl(self.rgb[0], self.rgb[1], self.rgb[2])

        self.hue_l = Label(self.frame, text = f"hue: {self.hsl[0]} deg",
                           bg = "#242424", fg = "#cccccc")
        self.hue_l.pack(fill = 'both')
        
        self.sat_l = Label(self.frame, 
                           text = f"saturation: {int(self.hsl[1] * 100)}%",
                           bg = "#242424", fg = "#cccccc")
        self.sat_l.pack(fill = 'both')

        self.lum_l = Label(self.frame, 
                           text = f"luminance: {int(self.hsl[2] * 100)}%",
                           bg = "#242424", fg = "#cccccc")
        self.lum_l.pack(fill = 'both')


    def get_widget(self):
        return self.frame

    def update_hsl(self, h_i, s_i, l_i):
        self.hsl[0] += h_i
        self.hsl[0] %= 361
        if self.hsl[0] < 0: 360 + self.hsl[0]
        self.hsl[1] += s_i
        self.hsl[1] = min(max(self.hsl[1], 0), 1)
        self.hsl[2] += l_i
        self.hsl[2] = min(max(self.hsl[2], 0), 1)

        self.hue_l.config(text = f"hue: {self.hsl[0]} deg")
        self.sat_l.config(text = f"saturation: {int(self.hsl[1] * 100)}%")
        self.lum_l.config(text = f"luminance: {int(self.hsl[2] * 100)}%")

        self.rgb = hsl_to_rgb(self.hsl[0], self.hsl[1], self.hsl[2])

        hex_code = rgb_to_hex(self.rgb[0], self.rgb[1], self.rgb[2])
        self.col_display.config(bg = hex_code)

        return hex_code


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
