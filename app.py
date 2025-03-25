from pynput import keyboard as kb
from app_window import AppWindow

def on_press(key):
    if key == kb.KeyCode.from_char('s'):
        return False
    if key == kb.KeyCode.from_char('x'):
        global is_running
        is_running = False
        return False

is_running = True
while is_running:
    window = AppWindow()
    with kb.Listener(on_press = on_press) as listener:
        listener.join()
    if is_running:
        window.run()
