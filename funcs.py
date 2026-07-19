import tkinter as tk
from tkinter import*
import customtkinter
from customtkinter import *


s=0
    while stop_track!=True:
        while s<=10:
            s+=1
            sleep(float(1))
        chgwin=CTkToplevel()
        chgwin.after(100, chgwin.lift)
        label=Label(chgwin, text="Click Continue to continue recording \n or save to exit and save actions")
        save=CTkButton(chgwin, width=50, height=25, command=lambda: end(chgwin), text="Save")
        cont=CTkButton(chgwin, width=50, height=25, command=lambda: chgwin.destroy(), text="Continue")
        label.pack()
        save.pack()
        cont.pack()
        s=0
