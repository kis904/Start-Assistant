import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
import customtkinter
from customtkinter import CTkButton, CTkToplevel, CTkLabel, CTkImage
from PIL import Image, ImageTk
import os, pyautogui, pytesseract, pygetwindow
from PIL import Image
from time import sleep, time
import webbrowser, pywinstyles
from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener
from tkinter.messagebox import showinfo

#           CHECK BACKGROUND SOURCE !!!!

#open config file
#print("A")
with open("C:/Danimunka/startassist/config.txt", "r+", encoding="UTF-8") as config:
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
button_obj_list=[]
settings_obj_list=[]
session=0
#global first_letter
first_letter=True

#creating functions
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
    photo=PhotoImage(image_rs)
    background_label=customtkinter.CTkCanvas(window, image=photo)
    background_label.image=photo
    background_label.place(relwidth=1, relheight=1)

def end(win):
    win.destroy()

def findImg(img_path, minSearchTime, confidence):
    img=Image.open(img_path)
    location=pyautogui.locateOnScreen(image=img, minSearchTime=minSearchTime, confidence=confidence)
    center=pyautogui.center(location)
    x, y=center
    return x, y

window=customtkinter.CTk()
window.title("Start Assistant")
window._set_appearance_mode("dark")
try:
    window.geometry(dim)
    #print(dim)
except:
    window.geometry("1080x720")

#back_ground(window, background_route, dim)
#back_ground(window, 'C:/dev/startassist/start.jpg', dim)

#def enter(event):
#    event.widget.config(style=)

def Macondo():
    os.startfile("C:/Program Files/Mozilla Firefox/firefox.exe")
    start_record()
    
def on_release(key):
    if key==Key.esc:
        keyboard_listener.stop()
        mouse_listener.stop()
        file.close()
    else:
        global first_letter
        if first_letter:
            global temp_session
            temp_session=session
            first_letter=False
            file.write(f"\nwrite, {key}")
        elif temp_session==session:
            file.write(key)

def start_record():
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
    with Listener(on_release=on_release) as keyboard_listener, \
        mouse.Listener(on_click=mouse_track) as mouse_listener:
            keyboard_listener.join()
            mouse_listener.join()

def mouse_track(x, y, button, pressed):
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
    with open("config.txt", "w", encoding="utf-8") as file:
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
    with open("config.txt", "a+", encoding="utf-8") as config:
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
            with open("map.txt", "a", encoding="utf-8") as file:
                file.write(f"!, action, {conf}\n")
            win.destroy()
            start_record()
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

def choose_action():
    action_list=[]
    with open("map.txt", encoding="utf-8") as file:
        for line in file:
            if line.split(", ")[0]=="!":
                action_list.append(line.split(", ")[2].strip())
                print(line.split(" ")[1].strip())
    print(action_list)
    chgwin=CTkToplevel(window, takefocus=True)
    chgwin.geometry("400x120")
    label=CTkLabel(chgwin, text="Choose the action that you want to execute:")
    label.pack()
    for action in action_list:
        iterbutton=CTkButton(chgwin, width=10, height=1, text=action, command=lambda: execute_record(action, chgwin))
        iterbutton.pack()

def set_rec_name():
    chgwin=CTkToplevel(window, takefocus=True)
    chgwin.geometry("400x120")
    label=CTkLabel(chgwin, width=10, justify="left", text="You have 10 seconds to record your actions.\n If you need more time choose Continue in the pop-up window.\nWrite here the name of the new action:")
    dimensions=Text(chgwin, height=3, width=30)
    save=CTkButton(chgwin, width=10, height=1, text="Save", command=lambda: save_config(param="action", widget=dimensions, win=chgwin))
    label.pack()
    dimensions.pack()
    save.pack()

def chg_dim():
    chgwin=CTkToplevel(master=window, takefocus=True)
    chgwin.after(100, chgwin.lift)
    label=Label(chgwin, text="Write here the new dimensions \n in widthxheight format e.g 1080x720")
    dimensions=Text(chgwin, height=50, width=100)
    save=CTkButton(chgwin, width=50, height=25, command=lambda: save_config(param="dimensions", widget=dimensions, win=chgwin))
    label.pack()
    dimensions.pack()
    save.pack()
    

def change_background():
    chgwin=CTkToplevel(window, takefocus=True)
    chgwin.after(100, chgwin.lift)
    label=Label(chgwin, text="Select the new background \n supported file format is jpg")
    label.pack()
    background=filedialog.askopenfile(title="Select the new background", filetypes=[("JPEG", "*.jpg")])
    background=background.name
    save_config(param="background", win=chgwin, conf=background)
    print(background)

def exit_setup():
    for button in settings_obj_list:
        button.destroy()
    start()

def ex():
    window.quit()

def settings():
    for button in button_obj_list:
        button.destroy()
    settings_list=[
        ["change_dim","Change dimensions of the window", "", chg_dim],
        ["change_back", "Change background", "", change_background],
        ["exit", "Exit", "exit_left.png", exit_setup]
    ]
    for n, (name, title, picture, command) in enumerate(settings_list):
        if picture!="":
            image=Image.open(picture)
            photo=CTkImage(image, image)
            iterbutton=CTkButton(window, command=command, fg_color="#48484D", 
                            bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                            width=220, anchor="w", image=photo, text=title)
        else:
            iterbutton=CTkButton(window, text=title, command=command, fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w")
        settings_obj_list.append(iterbutton)
        iterbutton.grid(row=n+1, column=0, pady=(6, 0), padx=(20,0))


#creating buttons
buttons1=[
    ["settings", "Settings", "", settings],
    ["gmail", "Gmail", "", gmail],
    ["macondo", "Macondo", "", Macondo],
    ["start_record", "Start recording actions", "", set_rec_name],
    ["execute_record", "Execute record", "", choose_action],
    ["exit", "Exit", "exit_X.png", ex]
]
window.quit()
def start():   
    for n, (name, title, picture, command) in enumerate(buttons1):
        if name=="exit":
            image=Image.open(picture)
            photo=CTkImage(image, image)
            iterbutton=CTkButton(window, text=title, command=command, fg_color="#973B3B", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w", image=photo)
            iterbutton.grid(pady=(50, 0), padx=(15,0), sticky="W")
            button_obj_list.append(iterbutton)
        else:
            iterbutton=CTkButton(window, text=title, command=command, fg_color="#48484D", 
                            bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                            width=220, anchor="w")
            iterbutton.grid(pady=(6, 0), padx=(15,0), sticky="W")
            button_obj_list.append(iterbutton)
        pywinstyles.set_opacity(iterbutton, color="#000001")
place_holder=CTkLabel(window, fg_color="transparent", height=50, text="Welcome at Start Assistant",
                        bg_color="#000001", border_width=3, border_color="#2B2B68",
                        corner_radius=10, text_color="#F9F9FA", font=("Comic Sans MS", 20))
place_holder.grid(pady=(6, 0), padx=(0, 0))
pywinstyles.set_opacity(place_holder, color="#000001")
start()
window.mainloop()