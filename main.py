from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MainWindow
import sys


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


sys.excepthook = except_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Macros Creator')
    app.setApplicationDisplayName('Macros Creator')
    app.setDesktopFileName('Macros Creator')
    app.setOrganizationName('lenemter')

    # Stylesheet
    app.setStyle('Fusion')
    # with open('gui/py_dracula_dark.qss', mode='r', encoding='UTF-8') as file:
    #     app.setStyleSheet(file.read())

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
