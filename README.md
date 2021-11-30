# Macros Creator

Simple application for creating macros for mouse and keyboard

### Features:

* Click
* Move cursor
* Press Key
* Write Text
* Pause
* Loops
* Absolute / Relative mouse positioning

### OS Support:

* Windows
* Linux (X11)
* MacOS **_should work_** (not tested)
* Linux (Wayland) **does not work**

![img.png](img.png)  
![img_1.png](img_1.png)
![img_2.png](img_2.png)

### Build app with PyInstaller:

#### Linux / MacOS

`pyinstaller --onefile --name macros_creator --noconsole --add-data "gui/icons/.:." main.py`

#### Windows

`pyinstaller --onefile --name macros_creator --noconsole --add-data "gui/icons/.;." main.py`

Icons: [Breeze icon theme](https://github.com/KDE/breeze-icons)

### How to use

### Click

1. Action. What to do: Click, Press or Release mouse button
2. Button. Mouse button
3. Amount. Clicks amount (Available when chosen Click in Action)
4. Interval. Interval between clicks (Available when chosen Click in Action and Amount > 1)
5. Move type. How to move mouse cursor
    1. Absolute. absolute screen position. (0; 0) is the left top corner
    2. Relative. Relative to previous mouse position
6. Position X
7. Position Y
8. Restore cursor position. Restore cursor position after action

### Move cursor

1. Move type. How to move mouse cursor
    1. Absolute. absolute screen position. (0; 0) is the left top corner
    2. Relative. Relative to previous mouse position
2. Position X
3. Position Y
4. Duration. Duration of move
5. Button. What mouse button to hold while moving the cursor

### Cursor path

1. Move type. How to move mouse cursor
    1. Absolute. absolute screen position (0; 0) is the left top corner
    2. Relative. Relative to previous mouse position
2. Duration. Duration of each individual move
3. Button. What mouse button to hold while moving the cursor
4. Table with points

### Press key

1. Key. What key to
   press [Available Keys](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys)
2. Action. What to do
3. Amount. Amount of key press (Available only when chosen Press and release in Action)
4. Interval. Interval between key presses (Available only when chosen Press and release in Action and
   Amount > 0)

### Write text

1. Text. What to write (English only. If you want to write in others languages write in English and
   change layout for executing)
2. Amount. How many times to repeat the text
3. Interval. Interval between every key press

### Pause

1. Duration. Pause duration

### Loop

1. Loop start. Where to start the loop
2. Count. How many times go to loop start

### Goto

1. Loop start. Where to go