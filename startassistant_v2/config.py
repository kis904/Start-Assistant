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
                    self.background_route.split()
                    print(self.background_route)

    def overwrite(self, param, param2, conf):
        with open("config.txt", "w", encoding="utf-8") as self.file:
            self.new=[]
            self.target=f"{param} : {param2}"
            #print(lines)
            for self.line in self.lines:
                if self.line!=self.target:
                    self.new.append(self.line)
            self.new.append(f"{param} : {conf}\n")
            self.file.writelines(self.new)
            return

    def save_config(self, param, **kwargs):
        with open("config.txt", "a+", encoding="utf-8") as config:
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
            elif param=="background":
                conf=kwargs.get("conf")
                for line in self.lines:
                    sp=line.split(" : ")
                    #print(sp)
                    if sp[0]=="background":
                        print("A")
                        self.overwrite(sp[0], sp[1], conf)
                        containes=True
                if containes==False:
                    print("B")
                    config.write(f"background : {conf}\n")
            elif param=="action":
                widget=kwargs.get("widget")
                win=kwargs.get("win")
                conf=widget.get("1.0", "end-1c")
                with open("map.txt", "a", encoding="utf-8") as self.file:
                    self.file.write(f"!, action, {conf}\n")
                win.destroy()
                self.record.start_record()
        showinfo("Changes in config", "Saved changes successfully in config.txt")
