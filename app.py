from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow

is_drawing = False

def on_press(key):
    if key == kb.KeyCode.from_char('q'):
        mouse_listener.stop()
        window.destroy()
        return False
    if key == kb.KeyCode.from_char('c'):
        window.clear()
    if key == kb.KeyCode.from_char('s'):
        window.hide()
    if key == kb.KeyCode.from_char('z'):
        window.undo()
    if key == kb.KeyCode.from_char('y'):
        window.redo()
    if key == kb.KeyCode.from_char('j'):
        window.update_pen(-3)
    if key == kb.KeyCode.from_char('k'):
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

window = AppWindow()
controller = mouse.Controller()

key_listener = kb.Listener(on_press = on_press)
mouse_listener = mouse.Listener(on_move = on_move,
                                on_click = on_click)
key_listener.start()
mouse_listener.start()

window.mainloop()

key_listener.join()
mouse_listener.join()
