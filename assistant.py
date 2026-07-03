import tkinter as tk
from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
import os, pynput, pyautogui, pytesseract
from PIL import Image

#open config file
print("A")
config=open("config.txt", "r+", encoding="UTF-8")
lines=config.readlines()
for line in lines:
    line.strip()
    sp=line.split(" : ")
    print(sp)
    if sp[0]=="dimensions":
        dim=sp[1].strip()


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
back_ground(window, 'C:/dev/startassist/start.jpg')


#def enter(event):
#    event.widget.config(style=)

def Macondo():
    os.startfile("C:/Program Files/Mozilla Firefox/firefox.exe")
    url="https://macondo.hackclub.com/"
    #if findImg("C:/dev/startassist/searchbar.png", 10, 0.5):
    #    pyautogui.typewrite(url)
    #    pyautogui.press('Enter')

def gmail():
    os.startfile("C:/Program Files/Mozilla Firefox/firefox.exe")
    url="https://gmail.com/"
    if findImg("C:/dev/startassist/searchbar.png", 3, 0.5):
        pyautogui.hotkey("ctrl", "l")
        pyautogui.typewrite(url)
        pyautogui.press('Enter')

def overwrite(param, conf):
    with open("config.txt", "w") as file:
        new=[]
        print(lines)
        for line in lines:
            if line!=param:
                new.append(line)
        new.append(f"dimensions : {conf}\n")
        print(*new)
        file.writelines(new)

def save_config(param, widget, win):
    print("B")
    conf=widget.get("1.0", "end-1c")
    containes=False
    if param=="dimensions":
        print("C")
        for line in lines:
            print("D")
            sp=line.split(" : ")
            print(sp)
            if sp[0]=="dimensions":
                overwrite(f"{sp[0]} : {sp[1]}", conf)
                containes=True
        if containes==False:
            config.write(f"\ndimensions : {conf}")
    win.destroy()

def chg_dim():
    chgwin=Toplevel(window, takefocus=True)
    label=Label(chgwin, text="Write here the new dimensions \n in widthxheight format e.g 1080x720")
    dimensions=Text(chgwin, height=50, width=100)
    save=Button(chgwin, width=50, height=25, bg="green", command=lambda: save_config("dimensions", dimensions, chgwin))
    label.pack()
    dimensions.pack()
    save.pack()

buttons=[
    ("button_1", "Gmail"),
    ("button_2", "Macondo")
]

def ex():
    window.quit()

buttons1=[
    #["change_dim","Change dimensions of the window", chg_dim()],
    (4,5,6)
]
for name, title, command in buttons1:
    iterbutton=ttk.Button(window, text=title, command=lambda: command)
    iterbutton.pack()
button = ttk.Button(window, text="test", command=lambda: chg_dim())
button.pack()

window.mainloop()