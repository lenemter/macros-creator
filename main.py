from PyQt5.QtWidgets import QApplication, qApp
from gui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    qApp.setApplicationName('Macros Creator')
    qApp.setApplicationDisplayName('Macros Creator')
    qApp.setDesktopFileName('Macros Creator')
    qApp.setOrganizationName('lenemter')
    main_window = MainWindow()
    main_window.show()

    app.exec_()
