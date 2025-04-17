from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow

key_binds = { "focus/unfocus" : 't',
              "quit" : 'q',
              "clear": 'c',
              "hide/unhide" : 's',
              "undo" : 'z',
              "redo" : 'y',
              "brush size -" : 'j',
              "brush size +" : 'k',
              "hue +" : 'b',
              "hue -" : 'i', 
              "saturation +" : 'n',
              "saturation -" : 'o',
              "luminance +" : 'm',
              "luminance -" : 'p',
              "eyedropper" : 'e'
             }

is_drawing = False
is_dragging = False
is_focused = True

def on_press(key):
    global is_focused
    if key == kb.KeyCode.from_char(key_binds["focus/unfocus"]):
        window.update_cheatsheet(0)
        is_focused = not is_focused
        window.hide_ui(is_focused)
    if is_focused:
        if key == kb.KeyCode.from_char(key_binds["quit"]):
            window.update_cheatsheet(1)
            mouse_listener.stop()
            window.destroy()
            return False
        if key == kb.KeyCode.from_char(key_binds["clear"]):
            window.update_cheatsheet(2)
            window.clear()
        if key == kb.KeyCode.from_char(key_binds["hide/unhide"]):
            window.update_cheatsheet(3)
            window.hide()
        if key == kb.KeyCode.from_char(key_binds["undo"]):
            window.update_cheatsheet(4)
            window.undo()
        if key == kb.KeyCode.from_char(key_binds["redo"]):
            window.update_cheatsheet(5)
            window.redo()
        if key == kb.KeyCode.from_char(key_binds["brush size -"]):
            window.update_cheatsheet(6)
            window.update_pen(-3)
        if key == kb.KeyCode.from_char(key_binds["brush size +"]):
            window.update_cheatsheet(7)
            window.update_pen(3)
        if key == kb.KeyCode.from_char(key_binds["hue +"]):
            window.update_cheatsheet(8)
            window.update_hsl(1, 0., 0.)
        if key == kb.KeyCode.from_char(key_binds["hue -"]):
            window.update_cheatsheet(9)
            window.update_hsl(-1, 0., 0.)
        if key == kb.KeyCode.from_char(key_binds["saturation +"]):
            window.update_cheatsheet(10)
            window.update_hsl(0, 0.01, 0.)
        if key == kb.KeyCode.from_char(key_binds["saturation -"]):
            window.update_cheatsheet(11)
            window.update_hsl(0, -0.01, 0.)
        if key == kb.KeyCode.from_char(key_binds["luminance +"]):
            window.update_cheatsheet(12)
            window.update_hsl(0, 0, 0.01)
        if key == kb.KeyCode.from_char(key_binds["luminance -"]):
            window.update_cheatsheet(13)
            window.update_hsl(0, 0, -0.01)
        if key == kb.KeyCode.from_char(key_binds["eyedropper"]):
            window.update_cheatsheet(14)
            window.eyedrop(controller.position[0], controller.position[1])

def on_click(x, y, button, pressed):
    global is_drawing, is_dragging
    if is_focused:
        if button == mouse.Button.left:
            top_widget = window.find_widget(x, y)
            if not pressed:
                is_drawing = False
                is_dragging = False
            elif top_widget == "mouse":
                window.update_tag(1)
                is_drawing = True
                window.paint(x, y)
                window.preview_draw(x, y)
            elif top_widget == "tray":
                window.paint_tray(x, y)
            else:
                is_dragging = True
        if button == mouse.Button.right:
            if pressed:
                window.init_scrnshot(x, y)
            else:
                window.take_scrnshot(x, y)
        key_listener.suppress_event()
    else:
        is_dragging = False
        is_drawing = False

def on_move(x, y):
    if is_drawing: window.paint_line(x, y)
    if is_dragging: window.drag_widget(x, y)
    window.preview_draw(x, y)

def on_scroll(x, y, dx, dy):
    global is_focused
    if dy != 0 and is_focused: window.update_pen(dy / abs(dy))

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
