from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener
import pygetwindow, pyautogui
import time
from time import sleep
from customtkinter import *
from tkinter import *

class Record:
    def __init__(self, gui):
        self.session=0
        self.gui=gui
        self.config=gui.config

    def on_release(self, key):
        if key==Key.esc:
            keyboard_listener.stop()
            mouse_listener.stop()
            file.close()
        else:
            global first_letter
            if first_letter:
                global temp_session
                temp_session=self.session
                first_letter=False
                file.write(f"\nwrite, {key}")
            elif temp_session==self.session:
                file.write(key)

    def start_record(self):
        print("A")
        global clock
        clock=int(time())
        s=pygetwindow.getAllTitles()
        for window in s:
            if window!="":
                window=pygetwindow.getWindowsWithTitle(window)[0]
                window.minimize()
        #global focus
        #focus=pygetwindow.getActiveWindowTitle()
        global keyboard_listener
        global mouse_listener
        global file
        file=open("map.txt", "a", encoding="utf-8")
        with Listener(on_release=self.on_release) as keyboard_listener, \
            mouse.Listener(on_click=self.mouse_track) as mouse_listener:
                keyboard_listener.join()
                mouse_listener.join()

    def mouse_track(self, x, y, button, pressed):
        global clock
        delta=int(time())-clock
        clock=int(time())
        print(clock, delta)
        if button==mouse.Button.left and pressed:
            print("mouse button pressed", button, delta)
            focus=pygetwindow.getActiveWindowTitle()
            session+=1
            first_letter=True
            file.write(f"click, {x};{y}, {delta}, {focus}\n")

    def mouse_move(self, x, y):
        global mouse_moved
        if mouse_moved+3==int(time()):
            global stop_track
            stop_track=True
            print("X")
        else:
            mouse_moved=int(time())

    def execute_record(self, record, win):
        win.destroy()
        s=pygetwindow.getAllTitles()
        for window in s:
            if window!="":
                window=pygetwindow.getWindowsWithTitle(window)[0]
                window.minimize()
        rec=False
        print(record)
        with open("map.txt", encoding="utf-8") as file:
            for line in file:
                sp=line.split(", ")
                if sp[0]=="!" and sp[2].strip()==record:
                    rec=True
                    print(rec)
                elif rec==True:
                    if sp[0]=="!":
                        return
                    [x,y]=sp[1].split(";")
                    sp[2]=sp[2].strip()
                    sp[3]=sp[3].strip()
                    focus=sp[3]
                    print(sp)
                    sleep(int(sp[2]))
                    if sp[3]!="\n":
                        while focus!=pygetwindow.getActiveWindowTitle():
                            sleep(1)
                            print(pygetwindow.getActiveWindowTitle(), focus)
                    
                    pyautogui.leftClick(int(x), int(y))                                
                    print(int(x), int(y), int(sp[2]))
            print("End of action")

    def choose_action(self):
        action_list=[]
        with open("map.txt", encoding="utf-8") as file:
            for line in file:
                if line.split(", ")[0]=="!":
                    action_list.append(line.split(", ")[2].strip())
                    print(line.split(" ")[1].strip())
        print(action_list)
        chgwin=CTkToplevel(self.gui.window, takefocus=True)
        chgwin.geometry("400x120")
        label=CTkLabel(chgwin, text="Choose the action that you want to execute:")
        label.pack()
        for action in action_list:
            iterbutton=CTkButton(chgwin, width=10, height=1, text=action, command=lambda: self.execute_record(action, chgwin))
            iterbutton.pack()

    def set_rec_name(self):
        chgwin=CTkToplevel(self.gui.window, takefocus=True)
        chgwin.geometry("400x120")
        label=CTkLabel(chgwin, width=10, justify="left", text="You have 10 seconds to record your actions.\n If you need more time choose Continue in the pop-up window.\nWrite here the name of the new action:")
        dimensions=Text(chgwin, height=3, width=30)
        save=CTkButton(chgwin, width=10, height=1, text="Save", command=lambda: self.gui.save_config(param="action", widget=dimensions, win=chgwin))
        label.pack()
        dimensions.pack()
        save.pack()
