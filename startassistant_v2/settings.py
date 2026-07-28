from customtkinter import CTkButton, CTkImage, CTkToplevel, filedialog
from PIL import Image, ImageTk
from tkinter import Text, Label

class Settings:
    def __init__(self, gui):
        self.gui=gui
        self.config=gui.config

    def settings(self):
        self.settings_obj_list=[]
        for button in self.gui.button_obj_list:
            button.destroy()
        self.settings_list=[
            ["change_dim","Change dimensions of the window", "", self.chg_dim],
            ["change_back", "Change background", "", self.change_background],
            ["exit", "Exit", "exit_left.png", self.exit_setup]
        ]
        for n, (name, title, picture, command) in enumerate(self.settings_list):
            if picture!="":
                
                image=Image.open(picture)
                photo=CTkImage(image, image)
                iterbutton=CTkButton(self.gui.window, command=command, fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w", image=photo, text=title)
            else:
                iterbutton=CTkButton(self.gui.window, text=title, command=command, fg_color="#48484D", 
                                    bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                    width=220, anchor="w")
            self.settings_obj_list.append(iterbutton)
            iterbutton.grid(row=n+1, column=0, pady=(6, 0), padx=(20,0))

    def chg_dim(self):
        chgwin=CTkToplevel(master=self.gui.window, takefocus=True)
        chgwin.after(100, chgwin.lift)
        label=Label(chgwin, text="Write here the new dimensions \n in widthxheight format e.g 1080x720")
        dimensions=Text(chgwin, height=50, width=100)
        save=CTkButton(chgwin, width=50, height=25, command=lambda: self.config.save_config(param="dimensions", widget=dimensions, win=chgwin))
        label.pack()
        dimensions.pack()
        save.pack()
        
    def change_background(self):
        chgwin=CTkToplevel(self.gui.window, takefocus=True)
        chgwin.after(100, chgwin.lift)
        label=Label(chgwin, text="Select the new background \n supported self.file format is jpg")
        label.pack()
        background=self.filedialog.askopenself.file(title="Select the new background", filetypes=[("JPEG", "*.jpg")])
        background=background.name
        self.config.save_config(param="background", win=chgwin, conf=background)
        print(background)

    def exit_setup(self):
        for button in self.settings_obj_list:
            button.destroy()
        self.gui.start()