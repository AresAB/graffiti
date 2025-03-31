from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow

key_binds = { "quit" : 'q',
              "clear": 'c',
              "hide" : 's',
              "undo" : 'z',
              "redo" : 'y',
              "brush size -" : 'j',
              "brush size +" : 'k' }

is_drawing = False

def on_press(key):
    if key == kb.KeyCode.from_char(key_binds["quit"]):
        mouse_listener.stop()
        window.destroy()
        return False
    if key == kb.KeyCode.from_char(key_binds["clear"]):
        window.clear()
    if key == kb.KeyCode.from_char(key_binds["hide"]):
        window.hide()
    if key == kb.KeyCode.from_char(key_binds["undo"]):
        window.undo()
    if key == kb.KeyCode.from_char(key_binds["redo"]):
        window.redo()
    if key == kb.KeyCode.from_char(key_binds["brush size -"]):
        window.update_pen(-3)
    if key == kb.KeyCode.from_char(key_binds["brush size +"]):
        window.update_pen(3)

def on_click(x, y, button, pressed):
    global is_drawing
    if button == mouse.Button.left:
        if pressed: window.update_tag(1)
        is_drawing = not is_drawing
        window.paint(x, y)
        window.preview_draw(x, y)
        key_listener.suppress_event()

def on_move(x, y):
    global is_drawing
    if is_drawing: window.paint_line(x, y)
    window.preview_draw(x, y)

def on_scroll(x, y, dx, dy):
    window.update_pen(dy / abs(dy))

window = AppWindow()
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
