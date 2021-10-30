def get_dark_palette():
    from PyQt5.QtGui import QPalette, QColor
    from PyQt5.QtCore import Qt

    DEFAULT_TEXT = QColor('#f0f0f0')
    DISABLED_TEXT = QColor('#515151')
    WINDOW = QColor('#333333')
    BASE = QColor('#3a3a3a')
    RED = QColor('#c6262e')
    PURPLE = QColor('#a56de2')
    DARKER_PURPLE = QColor('#955ad6')

    palette = QPalette()
    palette.setColor(QPalette.Window, WINDOW)
    palette.setColor(QPalette.WindowText, DEFAULT_TEXT)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, DISABLED_TEXT)
    palette.setColor(QPalette.Base, BASE)
    palette.setColor(QPalette.AlternateBase, BASE)
    palette.setColor(QPalette.ToolTipBase, BASE)
    palette.setColor(QPalette.ToolTipText, DEFAULT_TEXT)
    palette.setColor(QPalette.Text, DEFAULT_TEXT)
    palette.setColor(QPalette.Disabled, QPalette.Text, DISABLED_TEXT)
    palette.setColor(QPalette.Dark, BASE)
    palette.setColor(QPalette.Shadow, QColor(40, 40, 40))
    palette.setColor(QPalette.Button, BASE)
    palette.setColor(QPalette.ButtonText, DEFAULT_TEXT)
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, DISABLED_TEXT)
    palette.setColor(QPalette.BrightText, RED)
    palette.setColor(QPalette.Link, PURPLE)
    palette.setColor(QPalette.Highlight, DARKER_PURPLE)
    palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(78, 72, 89))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    palette.setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(127, 127, 127))

    return palette


def get_font():
    from PyQt5.QtWidgets import QApplication

    font = QApplication.font()
    font.setPointSize(font.pointSize() + 1)
    return font
