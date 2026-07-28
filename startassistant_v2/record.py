from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener, KeyCode
import pygetwindow, pyautogui
from time import sleep, time
from customtkinter import *
from tkinter import *

class Record:
    def __init__(self):
        self.session=0
        self.first_letter=True

    def on_release(self, key):
        if key==Key.esc:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            try:
                if self.string!=[]:
                    self.file.write(f"write, {"".join(self.string)}\n")
            except:
                print("Error during writing", self.string)
            self.file.close()
        else:
            if self.first_letter:
                self.temp_session=self.session
                self.first_letter=False
                try:
                    if self.string!=[]:
                        self.file.write(f"write, {"".join(self.string)}\n")
                except:
                    print("Error during writing", self.string)
                self.string=[]
            elif self.first_letter or self.temp_session==self.session:
                try:
                    print("alphanumeric {0} pressed".format(key.char))
                    self.string.append("{0}".format(key.char))
                except AttributeError:
                    print("special key {0} pressed".format(key))
                    self.string.append("{0}".format(key))
                print(key, self.string)

    def start_record(self):
        print("A")
        self.string=[]
        self.clock=int(time())
        s=pygetwindow.getAllTitles()
        for window in s:
            if window!="":
                window=pygetwindow.getWindowsWithTitle(window)[0]
                window.minimize()
        #global focus
        #focus=pygetwindow.getActiveWindowTitle()
        self.file=open("map.txt", "a", encoding="utf-8")
        with Listener(on_release=self.on_release) as self.keyboard_listener, \
            mouse.Listener(on_click=self.mouse_track) as self.mouse_listener:
                self.keyboard_listener.join()
                self.mouse_listener.join()

    def mouse_track(self, x, y, button, pressed):
        delta=int(time())-self.clock
        self.clock=int(time())
        print(self.clock, delta)
        if button==mouse.Button.left and pressed:
            print("mouse button pressed", button, delta)
            focus=pygetwindow.getActiveWindowTitle()
            self.session+=1
            self.first_letter=True
            self.file.write(f"click, {x};{y}, {delta}, {focus}\n")

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
        with open("map.txt", encoding="utf-8") as self.file:
            for line in self.file:
                sp=line.split(", ")
                if sp[0]=="!" and sp[2].strip()==record:
                    rec=True
                    print(rec)
                elif rec==True:
                    if sp[0]=="!":
                        return
                    elif sp[0]=="click":
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
                    elif sp[0]=="write":
                        pyautogui.typewrite(sp[1].strip())
            print("End of action")