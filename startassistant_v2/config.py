from customtkinter import *
from tkinter.messagebox import showinfo
from record import Record

class Config:
    #open config self.file
    #print("A")
    def start(self):
        self.record=Record()
        with open("C:/Danimunka/startassist/config.txt", "r+", encoding="UTF-8") as config:
            self.lines=config.readlines()
            for line in self.lines:
                line.strip()
                sp=line.split(" : ")
                #print(sp)
                if sp[0]=="dimensions":
                    self.dim=sp[1].strip()
                    self.dim.split()
                if sp[0]=="background":
                    self.background_route=sp[1].strip()
                    #print(self.background_route)
                if sp[0]=="fontsize":
                    self.fontsize=sp[1].strip()
                if sp[0]=="font":
                    self.font=sp[1].strip()
                
    def overwrite(self, param, param2, conf):
        with open("config.txt", "r", encoding="utf-8") as self.file:
            self.lines=self.file.readlines()
        with open("config.txt", "w", encoding="utf-8") as self.file:
            self.new=[]
            self.target=f"{param} : {param2}"
            #print(self.lines)
            for line in self.lines:
                #print(line, self.target)
                if line!=self.target:
                    self.new.append(line)
            self.new.append(f"{param} : {conf}\n")
            self.file.writelines(self.new)
            return

    def save_config(self, param, **kwargs):
        with open("config.txt", "r+", encoding="utf-8") as config:
            self.lines=config.readlines()
            #print(self.lines)
            containes=False
            if param=="dimensions":
                widget=kwargs.get("widget")
                win=kwargs.get("win")
                win=CTk()
                conf=widget.get("1.0", "end-1c")
                for line in self.lines:
                    sp=line.split(" : ")
                    #print(sp)
                    if sp[0]=="dimensions":
                        self.overwrite(sp[0], sp[1], conf)
                        containes=True
                if containes==False:
                    config.write(f"\ndimensions : {conf}")
                win.destroy()
                showinfo("Changes in config", "Saved dimensions successfully in config.txt", icon="info")
            elif param=="background":
                conf=kwargs.get("conf")
                for line in self.lines:
                    sp=line.split(" : ")
                    #print(sp)
                    if sp[0]=="background":
                        #print("A")
                        self.overwrite(sp[0], sp[1], conf)
                        containes=True
                if containes==False:
                    #print("B")
                    config.write(f"background : {conf}\n")
                showinfo("Changes in config", "Saved background route successfully in config.txt", icon="info")
            elif param=="action":
                conf=kwargs.get("conf")
                with open("map.txt", "a", encoding="utf-8") as self.file:
                    self.file.write(f"!, action, {conf}\n")
            elif param=="fontsize":
                conf=kwargs.get("conf")
                for line in self.lines:
                    sp=line.split(" : ")
                    #print(sp)
                    if sp[0]=="fontsize":
                        #print("A")
                        self.overwrite(sp[0], sp[1], conf)
                        containes=True
                if containes==False:
                    #print("B fontsize")
                    config.write(f"fontsize : {conf}\n")
                showinfo("Changes in config", "Saved font size successfully in config.txt", icon="info")
            elif param=="font":
                conf=kwargs.get("conf")
                for line in self.lines:
                    sp=line.split(" : ")
                    #print(sp)
                    if sp[0]=="font":
                        #print("A")
                        self.overwrite(sp[0], sp[1], conf)
                        containes=True
                if containes==False:
                    #print("B font")
                    config.write(f"font : {conf}\n")
                showinfo("Changes in config", "Saved font successfully in config.txt", icon="info")