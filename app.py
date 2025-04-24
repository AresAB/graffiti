from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow
import math
import win32api

key_binds = { "focus/unfocus" : 't',
              "quit" : 'q',
              "clear": 'c',
              "hide/unhide" : 's',
              "undo" : 'u',
              "redo" : 'y',
              "brush size -" : 'j',
              "brush size +" : 'k',
              "luminance +/-" : 'b',
              "chroma +/-" : 'n',
              "hue +/-" : 'm',
              "eyedropper" : 'e',
              "2nd mode" : 'shift'
             }

is_drawing = False
is_dragging = False
is_focused = True
is_alt_mode = False
is_pressed = False

def win32_event_filter(msg, data):
    global is_focused, is_alt_mode, is_pressed
    is_pressed = not is_pressed

    scan_code = win32api.MapVirtualKey(data.vkCode, 1)
    key = win32api.ToAsciiEx(data.vkCode, scan_code, win32api.GetKeyboardState()).decode('ascii')

    if is_pressed:
        if key == key_binds["focus/unfocus"]:
            window.update_cheatsheet(0)
            is_focused = not is_focused
            window.hide_ui(is_focused)
            key_listener.suppress_event()
        if is_focused:
            if data.vkCode == 160: # shift
                window.update_cheatsheet(12)
                is_alt_mode = not is_alt_mode
                window.invert_cheatsheet(is_alt_mode)
            if key == key_binds["quit"]:
                window.update_cheatsheet(1)
                mouse_listener.stop()
                window.destroy()
                key_listener.stop()
            if key == key_binds["clear"]:
                window.update_cheatsheet(2)
                window.clear()
            if key == key_binds["hide/unhide"]:
                window.update_cheatsheet(3)
                window.hide()
            if key == key_binds["undo"]:
                window.update_cheatsheet(4)
                window.undo()
            if key == key_binds["redo"]:
                window.update_cheatsheet(5)
                window.redo()
            if key == key_binds["brush size -"]:
                window.update_cheatsheet(6)
                window.update_pen(-3)
            if key == key_binds["brush size +"]:
                window.update_cheatsheet(7)
                window.update_pen(3)
            if key == key_binds["luminance +/-"]:
                window.update_cheatsheet(8)
                if is_alt_mode: window.update_oklch(-0.01, 0., 0.)
                else: window.update_oklch(0.01, 0., 0.)
            if key == key_binds["chroma +/-"]:
                window.update_cheatsheet(9)
                if is_alt_mode: window.update_oklch(0, -0.01, 0.)
                else: window.update_oklch(0, 0.01, 0.)
            if key == key_binds["hue +/-"]:
                window.update_cheatsheet(10)
                if is_alt_mode: window.update_oklch(0, 0, -1 * (math.pi / 180))
                else: window.update_oklch(0, 0, 1 * (math.pi / 180))
            if key == key_binds["eyedropper"]:
                window.update_cheatsheet(11)
                window.eyedrop(controller.position[0], controller.position[1])
            key_listener.suppress_event()

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
        key_listener.suppress_event() #check if this does smth
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

key_listener = kb.Listener(win32_event_filter=win32_event_filter)
mouse_listener = mouse.Listener(on_move = on_move,
                                on_click = on_click,
                                on_scroll = on_scroll)
key_listener.start()
mouse_listener.start()

window.mainloop()

key_listener.join()
mouse_listener.join()
