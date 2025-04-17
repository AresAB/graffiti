from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow

key_binds = { "quit" : 'q',
              "clear": 'c',
              "hide" : 's',
              "undo" : 'z',
              "redo" : 'y',
              "brush size -" : 'j',
              "brush size +" : 'k',
              "hue +" : 'b',
              "hue -" : 'i', 
              "saturation +" : 'n',
              "saturation -" : 'o',
              "luminance +" : 'm',
              "luminance -" : 'p'
             }

is_drawing = False
is_dragging = False

def on_press(key):
    if key == kb.KeyCode.from_char(key_binds["quit"]):
        window.update_cheatsheet(0)
        mouse_listener.stop()
        window.destroy()
        return False
    if key == kb.KeyCode.from_char(key_binds["clear"]):
        window.update_cheatsheet(1)
        window.clear()
    if key == kb.KeyCode.from_char(key_binds["hide"]):
        window.update_cheatsheet(2)
        window.hide()
    if key == kb.KeyCode.from_char(key_binds["undo"]):
        window.update_cheatsheet(3)
        window.undo()
    if key == kb.KeyCode.from_char(key_binds["redo"]):
        window.update_cheatsheet(4)
        window.redo()
    if key == kb.KeyCode.from_char(key_binds["brush size -"]):
        window.update_cheatsheet(5)
        window.update_pen(-3)
    if key == kb.KeyCode.from_char(key_binds["brush size +"]):
        window.update_cheatsheet(6)
        window.update_pen(3)
    if key == kb.KeyCode.from_char(key_binds["hue +"]):
        window.update_hsl(1, 0., 0.)
    if key == kb.KeyCode.from_char(key_binds["hue -"]):
        window.update_hsl(-1, 0., 0.)
    if key == kb.KeyCode.from_char(key_binds["saturation +"]):
        window.update_hsl(0, 0.01, 0.)
    if key == kb.KeyCode.from_char(key_binds["saturation -"]):
        window.update_hsl(0, -0.01, 0.)
    if key == kb.KeyCode.from_char(key_binds["luminance +"]):
        window.update_hsl(0, 0, 0.01)
    if key == kb.KeyCode.from_char(key_binds["luminance -"]):
        window.update_hsl(0, 0, -0.01)

def on_click(x, y, button, pressed):
    global is_drawing, is_dragging
    if button == mouse.Button.left:
        if window.find_widget(x, y) == "mouse":
            if pressed: 
                window.update_tag(1)
                is_drawing = True
                window.paint(x, y)
                window.preview_draw(x, y)
            else: 
                is_drawing = False
        else:
            is_dragging = not is_dragging
    if button == mouse.Button.right:
        if pressed:
            window.init_scrnshot(x, y)
        else:
            window.take_scrnshot(x, y)
    key_listener.suppress_event()

def on_move(x, y):
    global is_drawing
    if is_drawing: window.paint_line(x, y)
    if is_dragging: window.drag_widget(x, y)
    window.preview_draw(x, y)

def on_scroll(x, y, dx, dy):
    if dy != 0: window.update_pen(dy / abs(dy))

window = AppWindow(key_binds)
controller = mouse.Controller()

key_listener = kb.Listener(on_press = on_press)
mouse_listener = mouse.Listener(on_move = on_move,
                                on_click = on_click,
                                on_scroll = on_scroll)
key_listener.start()
mouse_listener.start()

window.mainloop()

key_listener.join()
mouse_listener.join()
