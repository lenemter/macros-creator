from PyQt5.QtWidgets import QApplication
import sys
from gui import stylesheet

from gui.MainWindow import MainWindow


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
    app.setPalette(stylesheet.get_dark_palette())
    app.setFont(stylesheet.get_font())

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
