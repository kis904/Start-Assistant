import pyautogui, pygetwindow
from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener


def on_release(key):
    if key==Key.down:
        print("A")
    if key==Key.esc:
        keyboard_listener.stop()
        mouse_listener.stop()
def mouse_track(x, y, button, pressed):
    if button==mouse.Button.left and pressed:
        print("mouse button pressed", button)

with Listener(on_release=on_release) as keyboard_listener, \
    mouse.Listener(on_click=mouse_track) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

Key.down