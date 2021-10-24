common_stylesheet = """
QLabel {
    padding: 8px;
}
QPushButton, QLineEdit, QTextEdit, QMenu {
    border-radius: 2px
}
QComboBox QAbstractItemView {
    background-color: #eee;
    border: 1px solid #bbb;
    padding: 4px;
}
QPushButton {
    padding: 6px 12px;
}
QLineEdit {
    padding: 6px;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    padding: 6px;
}
QTextEdit {
    padding: 1px;
    margin: 2px;
    background-color: palette(base);  /* fix for border-radius */
}
QHeaderView::section {
    font-weight: bold;
}
"""

light_stylesheet = common_stylesheet + """
* {
    color: #333333;
}
QMainWindow, QDialog, #container {
    background-color: #eeeeee;
}
QPushButton {
    background-color: #ffffff;
    border: 1px solid #bbbbbb;
}
QLineEdit {
    border: 1px solid #bbbbbb;
}
QTextEdit {
    border: 1px solid #bbbbbb;
}
QTableView {
    border-color: #999999;
}
QTableView::item {
    selection-background-color: #6fb2dc;
}
QHeaderView::section {
    background-color: #ffffff;
}
QMenu {
    border: 1px solid #000000;
    background-color: #ffffff;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
}
"""

dark_stylesheet = common_stylesheet + """
* {
    color: #ddd;
}
QMainWindow, QDialog, #container {
    background-color: #2a2a2a;
}
QPushButton {
    background-color: #4a4a4a;
    border: 1px solid #444;
}
QLineEdit {
    background-color: #4a4a4a;
    border: 1px solid #444;
}
QTextEdit {
    background-color: #4a4a4a;
    border: 1px solid #444;
}
QTableView {
    background-color: #444;
}
QTableView::item {
    selection-background-color: #5174a3;
}
QHeaderView::section {
    background-color: #444;
}
"""