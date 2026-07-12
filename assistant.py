import tkinter as tk
from tkinter import*
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os, pyautogui, pytesseract
from PIL import Image
from time import sleep, time
import webbrowser
from pynput import mouse, keyboard
from tkinter.messagebox import showinfo

#open config file
#print("A")
config=open("config.txt", "r+", encoding="UTF-8")
lines=config.readlines()
for line in lines:
    line.strip()
    sp=line.split(" : ")
    #print(sp)
    if sp[0]=="dimensions":
        dim=sp[1].strip()
    if sp[0]=="background":
        background_route=sp[1]

#creating variables that will be used later
stop_track=False
mouse_moved=0

def back_ground(window, image_path):
    image=Image.open(image_path)
    image=image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
    photo=ImageTk.PhotoImage(image)
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
except:
    window.geometry("1080x720")
try:
    back_ground(background_route)
except:
    back_ground(window, 'C:/dev/startassist/start.jpg')

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
    mouse_listener=mouse.Listener(
        on_click=mouse_track,
        on_move=mouse_move
    )
    mouse_listener.start()
    s=0
    while s<=10:
        if stop_track==True:
            mouse_listener.stop()
            #mouse_listener.join()
            print("E")
            s+=1
            sleep(1)
            return
    mouse_listener.stop()
    #mouse_listener.join()

def mouse_track(x, y, button, pressed):
    if button==mouse.Button.left and pressed:
        print("mouse button pressed", pressed, button)
        with open("map.txt", "a+") as file:
            file.write(f"click : {x};{y}\n")

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
    containes=False
    if param=="dimensions":
        widget=kwargs.get("widget")
        win=kwargs.get("win")
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
                overwrite(sp[0], sp[1], conf)
                containes=True
        if containes==False:
            config.write(f"background : {conf}\n")
    showinfo("Changes in config", "Saved changes successfully in config.txt")

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
    ["exit", "Exit", ex]
]
for name, title, command in buttons1:
    iterbutton=ttk.Button(window, text=title, command=command)
    iterbutton.pack()

window.mainloop()