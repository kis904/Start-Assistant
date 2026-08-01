# Start-Assistant

IMPORTANT: TO VIEW DETAILED LOGS VIEW THE COMMITS TO THIS PROJECT THERE IS THE TITLE AND OPEN TO READ DETAIL WHERE THE IMPROVEMENTS, CHANGES ARE DESCRIBED. ALSO YOU CAN TRACK THERE THE DEVELOPMENT IN CODE.

There are 2 versions of the project:

  1. As I started I started it in one file you can find it in the main branch right where you open it. All the files there are from the first version and experiments that didn't work like pytesseractocr.py is where I tried text on image detection, but it's too slow and not accurate enough plus the AI speech recognition that you can find at startassistant_v2/speechrecognition.py I tried python's SpeechRecognition library with Vosk's engine, but on my laptop it was too slow and didn't work properly so I aborted it

  2. The second version (v2) came when the first version became too crowded and messy, so I decided to split it into multiple files and start using classes, so it took a few hours just to make the code from the first version work here and then developed that one, so that version is what I was developing, that's the final. You can find it at startassistant_v2 folder.


There is one finished build yet, that's Start Assistant v1, that is a build based on the second version (mentioned above) that's currently at startassistant_build_v1/StartAssistant_v1 folder. It is built with pyinstaller, that created:
  1. gui.exe, you can start the program by launching that exe, double click on it
  2. _internal folder: everything the gui.exe needs to launch, all dependencies, libraries
  3. icons that the program uses
  4. text files that are needed in order to launch the program (map.txt for recording and config.txt for ssaving settings)


Installation manual:

To install, clone/copy this folder first: startassistant_build_v1/StartAssistant_v1

Unzip it, then start the program with launching the gui.exe. It opens a command prompt and an app with GUI. You can use the app, just ignore the command line. 

You don't need to install anything else. Every dependency, library is included.


How to use it:

First you can see the home page:

  1. Settings opens the settings tab where you can change font, font size and the dimensions of this window in pixel
      IMPORTANT: It saves your changed settings just if you click on the right button after you set. For example set font size on the slider, then click on Change font size button that saves your changes

  2. Start recording, if you click on that you can set the name of the action that you'll record in a pop-up window. Write it into the text field then click save.
     
          How it records:
     
          a) It'll minimize every window, so you'll start from your Desktop
     
          b) Now every click you make, every button you hit will be recorded. It can't record hotkeys yet.
     
          c) IMPORTANT: IT STOPS RECORDING IF YOU HIT THE ESC BUTTON ANYTIME
     
  3. Execute record: here you can select which recorded action you want to execute by clicking on it on the pop-up window.
    
  4. Exit: it closes the program


If you have questions how to use it, watch the demo, every feature is shown there.

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
  3. It can monitor, record and remake keyboard activities like typing, just hotkeys not yet


Future plans:
  1. Make a new version that the one main file is split to multiple smaller and make it class based program.
  #2026.07.29. Already has a working better version than the single file, now that's the main
  2. Add AI speech recognition and make it controllable just with voice
  3. Make recording hotkeys available


Sorry for the messy code, I always place test print commands to see where the code breaks or what it skips when it shouldn't and import a lot of things and make unused functions as I hope once I get there I'll use them.


Main problems that I struggled a lot with:
1. I had a lot of trouble with the proper handling of the config file, solved partially but still have decoding and encoding problems #solved
2. To create buttons well, as IDK how, but it started the buttons' functions, which were in a list, so I have to fix that too, as the main idea was to store the buttons main characteristics in a list such as name, title, command when pressed and create them with a 'for' cycle that iterates through that list and applies them #solved
3. Not a problem, but it took so much time to design the GUI, set the colors, always relaunch the code, see how it looks and then modify if it's ugly... The same problem when setting padding, fonts, borders and so on
4. Get keyboard monitoring and saving to map.txt and reproducate it, as the listener returns a KeyCode or Key object not string, that can't be written into file because not string, but it's hard to recover it's name. In addition to reproducate, the command waits for a string too. #solved
