from pynput import keyboard as kb
from pynput import mouse
from app_window import AppWindow
import math
import win32api
import sys

key_binds = { "focus/unfocus" : 's',
              "hide/unhide" : 'q',
              "quit" : 'x',
              "clear": 'c',
              "undo/redo" : 'z',
              "brush size +/-" : 'f',
              "luminance +/-" : 'a',
              "chroma +/-" : 'd',
              "hue +/-" : 'w',
              "eyedropper" : 'e',
              "2nd mode" : 'shift'
             }

is_drawing = False
is_dragging = False
is_scrn_shotting = False
is_focused = True
is_hidden = False
is_alt_mode = False
is_pressed = False
is_ctrl = False

def win32_event_filter(msg, data):
    global is_focused, is_hidden, is_alt_mode, is_pressed, is_ctrl
    is_pressed = not is_pressed

    scan_code = win32api.MapVirtualKey(data.vkCode, 1)
    key = win32api.ToAsciiEx(data.vkCode, scan_code, win32api.GetKeyboardState()).decode('ascii')
    
    if data.vkCode == 162: # ctrl
        is_ctrl = not is_ctrl

    if is_pressed and (is_ctrl or (is_focused and not is_hidden)):
        if key == key_binds["focus/unfocus"]:
            window.update_cheatsheet(0)
            is_focused = not is_focused
            is_hidden = False
            window.hide_ui(is_focused)
            key_listener.suppress_event()
        if key == key_binds["hide/unhide"]:
            window.update_cheatsheet(1)
            is_hidden = not is_hidden
            is_focused = True
            window.hide_window(is_hidden)
            key_listener.suppress_event()
        if key == key_binds["quit"]:
            window.update_cheatsheet(2)
            mouse_listener.stop()
            window.destroy()
            key_listener.stop()
            sys.exit(0)
        if key == key_binds["clear"]:
            window.update_cheatsheet(3)
            window.clear()
        if key == key_binds["undo/redo"]:
            window.update_cheatsheet(4)
            if is_alt_mode: window.redo()
            else: window.undo()
        if key == key_binds["brush size +/-"]:
            window.update_cheatsheet(5)
            if is_alt_mode: window.update_pen(-3)
            else: window.update_pen(3)
        if key == key_binds["luminance +/-"]:
            window.update_cheatsheet(6)
            if is_alt_mode: window.update_oklch(-0.05, 0., 0.)
            else: window.update_oklch(0.05, 0., 0.)
        if key == key_binds["chroma +/-"]:
            window.update_cheatsheet(7)
            if is_alt_mode: window.update_oklch(0, -0.05, 0.)
            else: window.update_oklch(0, 0.05, 0.)
        if key == key_binds["hue +/-"]:
            window.update_cheatsheet(8)
            if is_alt_mode: window.update_oklch(0, 0, -10 * (math.pi / 180))
            else: window.update_oklch(0, 0, 10 * (math.pi / 180))
        if key == key_binds["eyedropper"]:
            window.update_cheatsheet(9)
            window.eyedrop(controller.position[0], controller.position[1])
        if data.vkCode == 160: # shift
            window.update_cheatsheet(10)
            is_alt_mode = not is_alt_mode
            window.invert_cheatsheet(is_alt_mode)

        key_listener.suppress_event()

def on_click(x, y, button, pressed):
    global is_drawing, is_dragging, is_scrn_shotting
    if is_focused and not is_hidden:
        if button == mouse.Button.left:
            top_widget = window.find_widget(x, y)
            if not pressed:
                is_drawing = False
                is_dragging = False
            elif top_widget == "mouse":
                window.update_tag(1)
                if not is_alt_mode:
                    is_drawing = True
                    window.paint(x, y)
                    window.preview_draw(x, y)
            elif top_widget == "tray":
                window.paint_tray(x, y)
            elif top_widget == "screen shot" and not is_alt_mode:
                window.update_tag(1)
                is_drawing = True
                window.paint(x, y)
                window.preview_draw(x, y)
            else:
                is_dragging = True
        if button == mouse.Button.right:
            if pressed:
                window.update_tag(1)
                is_scrn_shotting = True
                window.init_scrnshot(x, y)
            else:
                is_scrn_shotting = False
                window.take_scrnshot(x, y)
        key_listener.suppress_event() 
    else:
        is_dragging = False
        is_drawing = False

def on_move(x, y):
    if is_drawing: window.paint_line(x, y)
    if is_dragging: window.drag_widget(x, y)
    if is_scrn_shotting: window.update_drag(x, y)
    window.preview_draw(x, y)

def on_scroll(x, y, dx, dy):
    if dy != 0 and is_focused and not is_hidden: 
        window.update_pen(dy / abs(dy))

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
