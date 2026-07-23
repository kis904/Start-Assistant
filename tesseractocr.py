import os
import pyautogui
from PIL import Image, ImageEnhance
import pytesseract
from time import sleep
import difflib
import math
import pyautogui, pygetwindow
from pynput import mouse, keyboard
from pynput.keyboard import Key, Listener

pytesseract.pytesseract.tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"

def findImg(img_path, minSearchTime, confidence, mod):
    img=Image.open(img_path)
    location=pyautogui.locateOnScreen(image=img, minSearchTime=minSearchTime, confidence=confidence)
    if location is not None:
        if mod==1:
            return location.left, location.top
        elif mod==2:
            x,y=pyautogui.center(location)
            return x,y
        
def preprocess(image):
    enhancer=ImageEnhance.Contrast(image)
    image=enhancer.enhance(10)
    image=image.convert('L')
    image.save("C:/Users/danie/Desktop/gray.png")
    return image

s=False
#starting detecting mouse and keyboard movements
def on_release(key):
    if key==Key.alt_l:
        print("A")
        print(pyautogui.position())
        
    if key==Key.esc:
        keyboard_listener.stop()
        mouse_listener.stop()

def mouse_track(x, y, button, pressed):
    if button==mouse.Button.left and pressed:
        print("mouse button pressed", button)
        screenshot=pyautogui.screenshot()
        screenshot.save("picture.png")
        img=preprocess(screenshot)
        img.save("gray.png")
        #text=pytesseract.image_to_string(img, config='--psm 6 --oem 3 -l hun')
        dictionary=pytesseract.image_to_data(img, config='--psm 6 --oem 3 -l hun', output_type=pytesseract.Output.DICT)
        print(dictionary)
        (x,y)=pyautogui.position()
        print(x,y)
        min_x, min_y=200,200
        for n in range(len(dictionary['width'])):
            if abs(y-dictionary['top'][n])<min_y:
                if abs(x-dictionary['left'][n])<min_x:
                    min_x=abs(x-dictionary['left'][n])
                    min_y=abs(y-dictionary['top'][n])
                    text=dictionary["text"][n]
                    print(min_x, min_y, text)
            elif abs(y-dictionary['top'][n]+dictionary['height'][n])<min_y:
                if  abs(x-dictionary['left'][n]+dictionary['width'][n])<min_x:
                    min_x=abs(x-dictionary['left'][n]+dictionary['width'][n])
                    min_y=abs(y-dictionary['top'][n]+dictionary['top'][n])
                    text=dictionary["text"][n]
                    print(min_x, min_y, text)
                    
        #with open("map.txt", "a+", encoding="utf-8") as file:
         #   file.write(f"click, {x};{y}\n")

def search_txt(txt):
    screenshot=pyautogui.screenshot()
    img=preprocess(screenshot)
    datas=pytesseract.image_to_data(img, lang="hun")
    for n in range(len(datas['level'])):
        if datas["text"][n]==txt:
            print("Found", datas["left"][n], datas["top"][n])
with Listener(on_release=on_release) as keyboard_listener, \
    mouse.Listener(on_click=mouse_track) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()

#search_txt("Run")