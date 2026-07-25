import customtkinter
from customtkinter import*
from config import Config
from settings import Settings
from record import Record
from PIL import Image, ImageTk
import pywinstyles

class GUI:
    def __init__(self):
        self.window=CTk()
        self.window.title("Start Assistant")
        self.window._set_appearance_mode("dark")
        self.window.geometry("500x600")
        
        #SET GLOBAL VARIABLES
        self.stop_track=False
        self.mouse_moved=0
        self.button_obj_list=[]
        self.settings_obj_list=[]
        self.session=0
        #self.global first_letter
        self.first_letter=True

        #IMPORT
        self.config=Config()
        self.settings=Settings(self)
        self.record=Record(self)
        self.config.start()
        self.window.geometry(self.config.dim)

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
            ["settings", "Settings", "", self.settings.settings],
            ["start_record", "Start recording actions", "", self.record.set_rec_name],
            ["execute_record", "Execute record", "", self.record.choose_action],
        ]
        self.window.quit()
        place_holder=CTkLabel(self.window, fg_color="transparent", height=50, text="Welcome at Start Assistant",
                                bg_color="#000001", border_width=3, border_color="#2B2B68",
                                corner_radius=10, text_color="#F9F9FA", font=("Comic Sans MS", 20))
        place_holder.grid(pady=(6, 0), padx=(0, 0))
        pywinstyles.set_opacity(place_holder, color="#000001")
        self.start()

    def start(self):   
        for n, (name, title, picture, command) in enumerate(self.home_buttons):
            if name=="exit":
                image=Image.open(picture)
                photo=CTkImage(image, image)
                iterbutton=CTkButton(self.window, text=title, command=command, fg_color="#973B3B", 
                                    bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                    width=220, anchor="w", image=photo)
                iterbutton.grid(pady=(50, 0), padx=(15,0), sticky="W")
                self.button_obj_list.append(iterbutton)
            else:
                iterbutton=CTkButton(self.window, text=title, command=command, fg_color="#48484D", 
                                bg_color="#000001", border_color="#1E1D66", border_width=1.5,
                                width=220, anchor="w")
                iterbutton.grid(pady=(6, 0), padx=(15,0), sticky="W")
                self.button_obj_list.append(iterbutton)
            pywinstyles.set_opacity(iterbutton, color="#000001")
    def run(self):
        self.window.mainloop()

if __name__=="__main__":
    app=GUI()
    app.run()