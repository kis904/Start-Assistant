from customtkinter import CTkButton, CTkImage, CTkToplevel, filedialog, CTkSlider, CTkTextbox, CTkLabel, CTkFrame, CTkOptionMenu
from PIL import Image, ImageTk
from tkinter import Text, Label, filedialog
from config import Config
from tkinter.messagebox import showinfo
from fonts import Fonts
import pywinstyles

class Settings:
    def __init__(self, gui):
        self.gui=gui
        self.config=Config()

    def settings(self):
        self.font_var=self.gui.font
        self.example_size=self.gui.font_size
        self.settings_obj_list=[]
        for button in self.gui.button_obj_list:
            button.destroy()
        self.settings_list=[
            ["change_dim","Change dimensions of the window", "", self.chg_dim],
            #["change_back", "Change background", "", self.change_background],
            ["change_size", "Change font size", "", self.change_font_size],
            ["change_font", "Change font", "", ""],
            ["exit", "Exit", "exit_left.png", self.exit_setup]
        ]
        place_holder=CTkLabel(self.gui.window, fg_color="transparent", height=50, text="Settings",
                                bg_color="#000001", border_width=3, border_color="#2B2B68",
                                corner_radius=10, text_color="#F9F9FA", font=(self.font_var, 20))
        place_holder.grid(pady=(6, 20), padx=(10, 0), sticky="w")
        pywinstyles.set_opacity(place_holder, color="#000001")
        self.settings_obj_list.append(place_holder)
        
        for n, (name, title, picture, command) in enumerate(self.settings_list):
            if picture!="":                
                image=Image.open(picture)
                photo=CTkImage(image, image)
                iterbutton=CTkButton(self.gui.window, command=command, fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w", image=photo, text=title, 
                                font=(self.font_var, int(self.gui.font_size)))
                iterbutton.grid(row=n+1, column=0, pady=(6, 0), padx=(20,0), sticky="w")
                self.settings_obj_list.append(iterbutton)
            else:
                if name=="change_size":
                    self.change_size_frame=CTkFrame(self.gui.window, bg_color="#000001", fg_color="#000001")
                    self.change_size_frame.grid(row=n+1, column=0, pady=(18, 0), padx=(15,0), sticky="w")
                    iterbutton=CTkButton(self.change_size_frame, command=command, fg_color="#48484D", 
                                        bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                        width=220, anchor="w", text=title, 
                                        font=(self.font_var, int(self.gui.font_size)))
                    set_main=CTkSlider(self.change_size_frame,from_=6, to=32, scroll_step=10, bg_color="#000001", 
                                    command=lambda value: self.chg_font_var(value=value), width=220)
                    self.example=CTkLabel(self.gui.window, text="Example text\nto check size and font", font=(self.font_var, int(self.example_size)), 
                                                    bg_color="#000001", fg_color="#48484D", corner_radius=4, text_color="#9B9BDA")
                    set_main.grid(row=0, column=0, pady=(0,10))
                    self.example.grid(row=2, column=1)
                    iterbutton.grid(row=1, column=0)
                    pywinstyles.set_opacity(self.change_size_frame, color="#000001")
                    self.settings_obj_list.append(self.example)  
                    self.settings_obj_list.append(self.change_size_frame)
                elif name=="change_font":
                    self.fonts=Fonts.fonts
                    self.font_frame=CTkFrame(self.gui.window, bg_color="#000001", fg_color="#000001")
                    self.font_frame.grid(row=n+1, column=0, pady=(20, 0), padx=(20,0), sticky="w")
                    font_list=[]
                    for i in range(20):
                        font_list.append(self.fonts[i])
                    self.options=CTkOptionMenu(self.font_frame, values=font_list, command=lambda v: self.change_font(v))
                    iterbutton=CTkButton(self.font_frame, text=title, command= self.change_font_perm, fg_color="#48484D", 
                                        bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                        width=220, anchor="w", font=(self.font_var, int(self.gui.font_size)))
                    self.options.grid(row=0, column=0, pady=(0,15))
                    iterbutton.grid(row=1, column=0)
                    pywinstyles.set_opacity(self.font_frame, color="#000001")
                    self.settings_obj_list.append(self.font_frame)
                else:
                    iterbutton=CTkButton(self.gui.window, text=title, command=command,
                                fg_color="#48484D", bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w", font=(self.font_var, int(self.gui.font_size)))
                    iterbutton.grid(row=n+1, column=0, pady=(6, 6), padx=(20,0), sticky="w")
                    self.settings_obj_list.append(iterbutton)
                    

    def change_font_perm(self):
        self.config.save_config(param="font", conf=self.font_var)
        self.gui.font=self.font_var

    def change_font_size(self):
        self.gui.font_size=self.example_size
        self.config.save_config(param="fontsize", conf=self.example_size)

    def chg_font_var(self, value):
        self.example_size=round(value)
        self.example.destroy()
        self.example=CTkLabel(self.gui.window, text="Example text\nto check size and font", font=(self.font_var, int(self.example_size)), 
                                 bg_color="#000001", fg_color="#48484D", corner_radius=4, text_color="#9B9BDA")
        self.example.grid(row=2, column=6, sticky="w")
        self.settings_obj_list.append(self.example)

    def change_font(self, var):
        self.font_var=var
        self.example.destroy()
        self.example=CTkLabel(self.gui.window, text="Example text\nto check size and font", font=(self.font_var, int(self.example_size)), 
                                 bg_color="#000001", fg_color="#48484D", corner_radius=4, text_color="#9B9BDA")
        self.example.grid(row=2, column=6, sticky="w")
        self.settings_obj_list.append(self.example)
        

    def chg_dim(self):
        chgwin=CTkToplevel(master=self.gui.window, takefocus=True)
        chgwin.after(100, chgwin.lift)
        label=Label(chgwin, text="Write here the new dimensions \n in widthxheight format e.g 1080x720")
        dimensions=Text(chgwin, height=10, width=50)
        save=CTkButton(chgwin, width=50, height=25, command=lambda: self.config.save_config(param="dimensions",
                        widget=dimensions, win=chgwin), text="Save")
        label.pack()
        dimensions.pack()
        save.pack()
        
    def change_background(self):
        chgwin=CTkToplevel(self.gui.window, takefocus=True)
        chgwin.after(100, chgwin.lift)
        label=Label(chgwin, text="Select the new background \n supported self.file format is jpg")
        label.pack()
        showinfo("Select the new background", "supported file format is jpg")
        background=filedialog.askopenfile(title="Select the new background", filetypes=[("JPEG", "*.jpg")])
        background=background.name
        self.config.save_config(param="background", win=chgwin, conf=background)
        #print(background)

    def exit_setup(self):
        for button in self.settings_obj_list:
            button.destroy()
        self.gui.start()