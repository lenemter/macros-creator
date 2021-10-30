# Macros Creator

Simple application for creating macros

![img.png](img.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)

Build app with PyInstaller:

### Linux / MacOS

`pyinstaller --onefile -w --add-data "gui/icons/.:." main.py`

### Windows

`pyinstaller --onefile -w --add-data "gui/icons/.;." main.py`

Icons: [Breeze icon theme](https://github.com/KDE/breeze-icons)