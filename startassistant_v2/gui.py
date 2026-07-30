import customtkinter
from customtkinter import*
from config import Config
from settings import Settings
from record import Record
from PIL import Image, ImageTk
import pywinstyles
from tkinter.messagebox import showinfo

class GUI:
    def __init__(self):
        #IMPORT
        self.config=Config()
        self.settings=Settings(self)
        self.record=Record()
        
        self.window=CTk()
        self.window.title("Start Assistant")
        self.window._set_appearance_mode("dark")
        self.window.geometry("500x600")
        self.im=Image.open("exit_left.png")
        self.photo=CTkImage(self.im, self.im)
        #SET GLOBAL VARIABLES
        self.stop_track=False
        self.mouse_moved=0
        self.button_obj_list=[]
        self.settings_obj_list=[]
        self.session=0
        
        self.config.start()
        self.window.geometry(self.config.dim)
        try:
            self.font_size=self.config.fontsize
        except:
            self.font_size=12
        try:
            self.font=self.config.font
        except:
            self.font="Comic Sans MS"


        self.window.grid_columnconfigure(1,weight=1)
        self.window.grid_rowconfigure(0, weight=0)
        
        #SET BACKGROUND SOMEHOW NO Route yet
        '''image=Image.open(self.config.background_route)
        (width, height)=image.size
        x, y=self.config.dim.split("x")
        x, y=int(x), int(y)
        if (x>y and height>width) or (y>x and height>width):
            r=y/height
            x=int(r*width)
        else:
            r=x/width
            y=int(r*height)
        print(x, y)
        image_rs=image.resize([x, y])
        photo=CTkImage(image_rs)
        background_label=customtkinter.CTkCanvas(self.window, image=photo)
        background_label.image=photo
        background_label.place(relwidth=1, relheight=1)
        '''

        #creating buttons
        self.home_buttons=[
            ["settings", "Settings", "gear.png", self.settings.settings],
            ["start_record", "Start recording actions", "rec.png", self.set_rec_name],
            ["execute_record", "Execute record", "play.png", self.choose_action],
            ["exit", "Exit", "exit_X.png", self.exit]
        ]
        place_holder=CTkLabel(self.window, fg_color="transparent", height=50, text="Welcome at Start Assistant",
                                bg_color="#000001", border_width=3, border_color="#2B2B68",
                                corner_radius=10, text_color="#F9F9FA", font=("self.font", 20))
        place_holder.grid(pady=(6, 20), padx=(10, 0))
        pywinstyles.set_opacity(place_holder, color="#000001")
        self.start()

    def start(self):   
        for n, (name, title, picture, command) in enumerate(self.home_buttons):
            if picture!="":
                image=Image.open(picture)
                photo=CTkImage(image, image)
                if name=="exit":
                    iterbutton=CTkButton(self.window, text=title, command=command, fg_color="#973B3B", 
                                                        bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                                        width=220, anchor="w", image=photo, font=("self.font", int(self.config.fontsize)))
                    iterbutton.grid(pady=(50, 0), padx=(25,0), sticky="W")
                else:
                    iterbutton=CTkButton(self.window, text=title, command=command, fg_color="#48484D", 
                                        bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                        width=220, anchor="w", image=photo, font=("self.font", int(self.config.fontsize)))
                    iterbutton.grid(pady=(6, 2), padx=(25,0), sticky="W")
                self.button_obj_list.append(iterbutton)
            else:
                iterbutton=CTkButton(self.window, text=title, command=command, fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w", font=("self.font", int(self.config.fontsize)))
                iterbutton.grid(pady=(6, 0), padx=(25,0), sticky="W")
                self.button_obj_list.append(iterbutton)
            pywinstyles.set_opacity(iterbutton, color="#000001")
    def run(self):
        self.window.mainloop()

    def exit(self):
        self.window.quit()

    def choose_action(self):
        action_list=[]
        with open("map.txt", encoding="utf-8") as self.file:
            for line in self.file:
                if line.split(", ")[0]=="!":
                    action_list.append(line.split(", ")[2].strip())
                    print(line.split(" ")[2].strip())
        print(action_list)
        if action_list!=[]:
            chgwin=CTkToplevel(self.window, takefocus=True, fg_color="#313135")
            #chgwin.geometry("400x120")
            #chgwin._set_appearance_mode("dark")
            label=CTkLabel(chgwin, text="Choose the action that you want to execute:", text_color="#7575C5", 
                           font=("self.font", int(self.config.fontsize)))
            label.grid(padx=(10,0), pady=(6,10))
            for action in action_list:
                iterbutton=CTkButton(chgwin, text=action, 
                                     command=lambda: self.record.execute_record(action, chgwin), fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                    width=220, anchor="w", font=("self.font", int(self.config.fontsize)))
                iterbutton.grid(padx=(20,0), pady=(6, 0), sticky="W")
                pywinstyles.set_opacity(iterbutton, color="#000001")
            chgwin.focus=True
        else:
            showinfo("No records available", "You have no records yet, first start with recording an action", icon="warning")

    def set_rec_name(self):
        chgwin=CTkToplevel(self.window, takefocus=True)
        chgwin.geometry("400x120")
        label=CTkLabel(chgwin, width=10, justify="left", text="Press Esc if you're ready, otherwise don't as it stops recording\nWrite here the name of the new action:")
        dimensions=CTkTextbox(chgwin, height=50, width=300)
        save=CTkButton(chgwin, width=10, height=1, text="Save",  fg_color="#0CB854",
                       command=lambda: self.rec_sequence(widget=dimensions, win=chgwin))
        label.pack()
        dimensions.pack()
        save.pack()

    def rec_sequence(self, widget, win):
        conf=widget.get("1.0", "end-1c")
        win.destroy()
        self.config.save_config(param="action", conf=conf)
        self.record.start_record()
        self.window.focus_set()
        showinfo("Changes in records", "Saved user events successfully in map.txt", icon="info")

if __name__=="__main__":
    app=GUI()
    app.run()