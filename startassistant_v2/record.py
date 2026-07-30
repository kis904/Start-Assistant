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
        print(key)
        if key==Key.esc:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            try:
                if self.string!=[]:
                    self.file.write(f"write, {"".join(self.string)}, {self.focus}\n")
            except:
                print("Error during writing", self.string)
            self.file.close()
        else:
            if self.first_letter:
                self.temp_session=self.session
                self.first_letter=False
                self.focus=pygetwindow.getActiveWindowTitle()
                try:
                    if self.string!=[]:                        
                        self.file.write(f"write, {"".join(self.string)}, {self.focus}\n")
                except:
                    print("Error during writing", self.string)
                self.string=[]
            if self.first_letter or self.temp_session==self.session:
                print("IN THE RECORD")
                try:
                    print("alphanumeric {0} pressed".format(key.char))
                    self.string.append("{0}".format(key.char))
                except AttributeError:
                    print("special key {0} pressed".format(key))
                    self.file.write(f"write, {"".join(self.string)}, {self.focus}\n")
                    self.string=[]
                    keystring="{0}".format(key).split(".")
                    self.file.write(f"specwrite, {keystring[1]}\n")
                    self.focus=pygetwindow.getActiveWindowTitle()
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
                    print(sp)
                    if sp[0]=="!":
                        return
                    if sp[0]=="click":
                        [x,y]=sp[1].split(";")
                        sp[3]=sp[3].strip("\n")
                        focus=sp[3]
                        #print(sp)
                        sleep(int(sp[2]))
                        if sp[3]!="\n":
                            while focus!=pygetwindow.getActiveWindowTitle():
                                sleep(1)
                                print(pygetwindow.getActiveWindowTitle(), focus)
                        pyautogui.leftClick(int(x), int(y))                                
                        print(int(x), int(y), int(sp[2]))
                    if sp[0]=="write":
                        focus=sp[2].strip("\n")
                        while focus!=pygetwindow.getActiveWindowTitle():
                                sleep(1)
                                print(pygetwindow.getActiveWindowTitle(), focus)
                        pyautogui.typewrite(sp[1])
                        print(sp[1])
                    print(sp[0])
                    if sp[0]=="specwrite":
                        sp[1]=sp[1].strip("\n")
                        pyautogui.press(sp[1])
                        print("pressed", sp[1])
            print("End of action")
