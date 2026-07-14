import tkinter as tk
from tkinter import*
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os, pyautogui, pytesseract, pygetwindow
from PIL import Image
from time import sleep, time
import webbrowser
from pynput import mouse, keyboard
from tkinter.messagebox import showinfo

#           CHECK BACKGROUND SOURCE !!!!

#open config file
#print("A")
with open("config.txt", "r+", encoding="UTF-8") as config:
    lines=config.readlines()
    for line in lines:
        line.strip()
        sp=line.split(" : ")
        #print(sp)
        if sp[0]=="dimensions":
            dim=sp[1].strip()
            dim.split()
        if sp[0]=="background":
            background_route=sp[1].strip()
            background_route.split()
            print(background_route)

#creating variables that will be used later
stop_track=False
mouse_moved=0

def back_ground(window, image_path, dim):
    image=Image.open(image_path)
    (width, height)=image.size
    x, y=dim.split("x")
    x, y=int(x), int(y)
    if (x>y and height>width) or (y>x and height>width):
        r=y/height
        x=int(r*width)
    else:
        r=x/width
        y=int(r*height)
    print(x, y)
    image_rs=image.resize([x, y])
    photo=ImageTk.PhotoImage(image_rs)
    background_label=tk.Label(window, image=photo)
    background_label.image=photo
    background_label.place(relwidth=1, relheight=1)

def findImg(img_path, minSearchTime, confidence):
    img=Image.open(img_path)
    location=pyautogui.locateOnScreen(image=img, minSearchTime=minSearchTime, confidence=confidence)
    center=pyautogui.center(location)
    x, y=center
    return x, y

window=tk.Tk()
window.title("Start Assistant")
try:
    window.geometry(dim)
    #print(dim)
except:
    window.geometry("1080x720")

#back_ground(window, background_route, dim)
back_ground(window, 'C:/dev/startassist/start.jpg', dim)

buttonhoverstyle=ttk.Style()
buttonhoverstyle.configure("buttonStyle.TButton",
                         width=20,
                         height=5,
                         background="#98BBE9")

#def enter(event):
#    event.widget.config(style=)

def Macondo():
    os.startfile("C:/Program Files/Mozilla Firefox/firefox.exe")
    start_mouse_track()
    
def start_mouse_track():
    print("A")
    global clock
    clock=int(time())
    s=pygetwindow.getAllTitles()
    for window in s:
        if window!="":
            window=pygetwindow.getWindowsWithTitle(window)[0]
            window.minimize()
    mouse_listener=mouse.Listener(
        on_click=mouse_track,
        #on_move=mouse_move
    )
    mouse_listener.start()
    s=0
    while s<=10:
        if stop_track==True:
            mouse_listener.stop()
            #mouse_listener.join()
            print("E")
            return
        s+=1
        sleep(float(1))
    mouse_listener.stop()
    #mouse_listener.join()

def mouse_track(x, y, button, pressed):
    global clock
    delta=int(time())-clock
    clock=int(time())
    print(clock, delta)
    if button==mouse.Button.left and pressed:
        focus=pygetwindow.getActiveWindowTitle()
        print("mouse button pressed", button, delta)
        with open("map.txt", "a+") as file:
            file.write(f"click, {x};{y}, {delta}, {focus}\n")

def mouse_move(x, y):
    global mouse_moved
    if mouse_moved+3==int(time()):
        global stop_track
        stop_track=True
        print("X")
    else:
        mouse_moved=int(time())

def gmail():
    #webbrowser.open("gmail.com")
    webbrowser.open("gmail.com")
    #os.startfile("C:/Program Files/Mozilla Firefox/firefox.exe")
    url="https://gmail.com/"
    if findImg("screenshots/searchbar.png", 3, 0.5):
        pyautogui.hotkey("ctrl", "l")
        sleep(0.5)
        pyautogui.typewrite(url)
        pyautogui.press('Enter')

def overwrite(param, param2, conf):
    with open("config.txt", "w") as file:
        new=[]
        target=f"{param} : {param2}"
        #print(lines)
        for line in lines:
            if line!=target:
                new.append(line)
        new.append(f"{param} : {conf}\n")
        file.writelines(new)
        return

def save_config(param, **kwargs):
    with open("config.txt", "a+") as config:
        containes=False
        if param=="dimensions":
            widget=kwargs.get("widget")
            win=kwargs.get("win")
            win=window
            conf=widget.get("1.0", "end-1c")
            for line in lines:
                sp=line.split(" : ")
                #print(sp)
                if sp[0]=="dimensions":
                    overwrite(sp[0], sp[1], conf)
                    containes=True
            if containes==False:
                config.write(f"\ndimensions : {conf}")
            win.destroy()
        elif param=="background":
            conf=kwargs.get("conf")
            for line in lines:
                sp=line.split(" : ")
                #print(sp)
                if sp[0]=="background":
                    print("A")
                    overwrite(sp[0], sp[1], conf)
                    containes=True
            if containes==False:
                print("B")
                config.write(f"background : {conf}\n")
        elif param=="action":
            widget=kwargs.get("widget")
            win=kwargs.get("win")
            conf=widget.get("1.0", "end-1c")
            with open("map.txt", "a") as file:
                file.write(f"!, action, {conf}\n")
            win.destroy()
            start_mouse_track()
    showinfo("Changes in config", "Saved changes successfully in config.txt")

def retrieve_textinput(widget, win):
    text=widget.get("1.0", "end")
    win.destroy()
    return text

def execute_record(record, win=window):
    win.destroy()
    s=pygetwindow.getAllTitles()
    for window in s:
        if window!="":
            window=pygetwindow.getWindowsWithTitle(window)[0]
            #window.minimize()
    rec=False
    print(record)
    with open("map.txt") as file:
        for line in file:
            sp=line.split(", ")
            print(sp)
            if sp[0]=="!" and sp[2].strip()==record:
                rec=True
                print(rec)
            elif rec==True:
                if sp[0]=="!":
                    return
                [x,y]=sp[1].split(";")
                sp[2]=sp[2].strip()
                pyautogui.leftClick(int(x), int(y))                                
                print(int(x), int(y), int(sp[2]))
                sleep(int(sp[2]))

def choose_action():
    action_list=[]
    with open("map.txt") as file:
        for line in file:
            if line.split(", ")[0]=="!":
                action_list.append(line.split(", ")[2].strip())
                print(line.split(" ")[1].strip())
    print(action_list)
    chgwin=Toplevel(window, takefocus=True)
    chgwin.geometry("400x120")
    for action in action_list:
        iterbutton=Button(chgwin, width=10, height=1, text=action, command=lambda: execute_record(action, chgwin))
        iterbutton.pack()
    label=Label(chgwin, text="Choose the action that you want to execute:")
    label.pack()

def start_record():
    chgwin=Toplevel(window, takefocus=True)
    chgwin.geometry("400x120")
    label=Label(chgwin, text="Write here the name of the new action:")
    dimensions=Text(chgwin, height=3, width=30)
    save=Button(chgwin, width=10, height=1, bg="green", text="Save", command=lambda: save_config(param="action", widget=dimensions, win=chgwin))
    label.pack()
    dimensions.pack()
    save.pack()

def chg_dim():
    chgwin=Toplevel(window, takefocus=True)
    label=Label(chgwin, text="Write here the new dimensions \n in widthxheight format e.g 1080x720")
    dimensions=Text(chgwin, height=50, width=100)
    save=Button(chgwin, width=50, height=25, bg="green", command=lambda: save_config(param="dimensions", widget=dimensions, win=chgwin))
    label.pack()
    dimensions.pack()
    save.pack()

def change_background():
    chgwin=Toplevel(window, takefocus=True)
    label=Label(chgwin, text="Select the new background \n supported file format is jpg")
    label.pack()
    background=filedialog.askopenfile(title="Select the new background", filetypes=[("JPEG", "*.jpg")])
    background=background.name
    save_config(param="background", win=chgwin, conf=background)
    print(background)

buttons=[
    ("button_1", "Gmail"),
    ("button_2", "Macondo")
]

def ex():
    window.quit()

buttons1=[
    ["change_dim","Change dimensions of the window", chg_dim],
    ["change_back", "Change background", change_background],
    ["gmail", "Gmail", gmail],
    ["macondo", "Macondo", Macondo],
    ["start_record", "Start recording actions", start_record],
    ["execute_record", "Execute record", choose_action],
    ["exit", "Exit", ex]
]
for name, title, command in buttons1:
    iterbutton=ttk.Button(window, text=title, command=command)
    iterbutton.pack()

window.mainloop()