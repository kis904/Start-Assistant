# Start-Assistant
An assistant that helps you in basic tasks, so it can log in to sites, if configured well.
Coded in python, it uses tkinter, ttk for GUI.
Has a config.txt file that it handles automatically, updates, reades, applies the settings in it.
Records users clicks, stores, and reproducates it with monitoring focus and evading too early clicks

Methods that used to mimic user's activity:
  1. The most basic algorithm is that works right now (2026.07.17), is that it detects left clicks and logs its exact coordinates and time between them to a txt file and if activated it reproduces the same input. Unfortunately I see a couple of places when it won't work as
     if the program opened updates or takes more time to open compared to when it was recorded, it will result in too early clicks and malfunctions
  2. My second thought is what I want to make next, that it takes screenshots when clicked and with the exact coordinates of the click and pytesseract ocr module, it could get for example the text of the button that the user clicked. This would help us in 2 problems: first
     if the design changes it could still locate the text of the button that the user clicked, second if it takes more time to load it won't continue until it can locate that specific text. So it would be an important update to the program
     #2026.07.23 until now I could make it monitor window in focus and wait until it's not the desired one. Also started working on saving screenshots when clicking and on screen text detection with Pytesseract OCR. That part is in the pytesseractocr.py file, to make it easier to debug, test

Future plans:
  1. Make a new version that the one main file is split to multiple smaller and make it class based program.

Sorry for the messy code, I always place test print commands to see where the code breaks or what it skips when it shouldn't and import a lot of things and make unused functions as I hope once I get there I'll use them.
Main problems that I struggled a lot with:
1. I had a lot of trouble with the proper handling of the config file, solved partially but still have decoding and encoding problems
2. To create buttons well, as IDK how, but it started the buttons' functions, which were in a list, so I have to fix that too, as the main idea was to store the buttons main characteristics in a list such as name, title, command when pressed and create them with a 'for' cycle that iterates through that list and applies them #solved
3. Not a problem, but it took so much time to design the GUI, set the colors, always relaunch the code, see how it looks and then modify if it's ugly... The same problem when setting padding, fonts, borders and so on
