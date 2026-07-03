# Start-Assistant
An assistant that helps you in basic tasks, so it can log in to sites, if configured well.
Coded in python, it uses tkinter, ttk for GUI.
Has a config.txt file that it handles automatically, updates, reades, applies the settings in it.

Sorry for the messy code, I always place test print commands to see where the code breaks or what it skips when it shouldn't.
Main problems that I struggled a lot with:
1. I had a lot of trouble with the proper handling of the config file
2. To create buttons well, as IDK how, but it started the buttons' functions, which were in a list, so I have to fix that too, as the main idea was to store the buttons main characteristics in a list such as name, title, command when pressed and create them with a 'for' cycle that iterates through that list and applies them
