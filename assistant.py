import tkinter as tk
from PIL import Image, ImageTk

def back_ground(window, image_path):
    image=Image.open(image_path)
    image=image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))
    photo=ImageTk.PhotoImage(image)
    background_label=tk.Label(window, image=photo)
    background_label.image=photo
    background_label.place(relwidth=1, relheight=1)

window=tk.Tk('Start Assistant')
window.title='Start Assistant'
back_ground(window, 'C:/dev/startassist/start.jpg')
window.mainloop()