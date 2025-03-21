from tkinter import *

window = Tk()

window.title("Graffiti")
window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")

window.overrideredirect(True) # this removes window frame
window.attributes("-topmost", True)
window.configure(bg="#add123")
window.attributes("-transparentcolor", "#add123")

lbl = Label(text = "test", bg = "red", height = 30, width = 20)
lbl.pack(side = TOP)

def x_pressed(event):
    window.destroy()
window.bind("<x>", x_pressed)

window.mainloop()
