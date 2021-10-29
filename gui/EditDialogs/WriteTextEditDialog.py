from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QTextEdit, QSpinBox, QDoubleSpinBox

from gui.EditDialogs.EditDialog import EditDialog


class WriteTextEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.text_textEdit.setText(self.action.text)
        self.amount_spinBox.setValue(self.action.amount)
        self.interval_doubleSpinBox.setValue(self.action.interval)

    def properties(self) -> tuple:
        return (self.comment_lineEdit.text(), self.text_textEdit.toPlainText(), self.amount_spinBox.value(),
                self.interval_doubleSpinBox.value())

    def init_ui(self):
        super().init_ui()

        # Text
        self.text_label = QLabel("Text:")  # Label
        self.text_label.setAlignment(Qt.AlignRight)
        self.text_textEdit = QTextEdit()  # TextEdit

        self.properties_grid.addWidget(self.text_label, 0, 0)
        self.properties_grid.addWidget(self.text_textEdit, 0, 1)

        # Amount
        self.amount_label = QLabel('Amount:')  # Label
        self.amount_label.setAlignment(Qt.AlignRight)
        self.amount_spinBox = QSpinBox()  # SpinBox
        self.amount_spinBox.setMinimum(1)

        self.properties_grid.addWidget(self.amount_label, 1, 0)
        self.properties_grid.addWidget(self.amount_spinBox, 1, 1)

        # Interval
        self.interval_label = QLabel("Interval:")  # Label
        self.interval_label.setAlignment(Qt.AlignRight)
        self.interval_doubleSpinBox = QDoubleSpinBox()  # DoubleSpinBox

        self.properties_grid.addWidget(self.interval_label, 2, 0)
        self.properties_grid.addWidget(self.interval_doubleSpinBox, 2, 1)
