from PyQt5.QtWidgets import QLabel, QTextEdit, QSpinBox
from PyQt5.QtCore import Qt

from gui.EditDialogs.EditDialog import EditDialog


class WriteTextEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.text_textEdit.setText(self.action.text)
        self.amount_spinBox.setValue(self.action.amount)

    def init_ui(self):
        super().init_ui()

        # Text property
        self.text_label = QLabel("Text:")
        self.text_label.setAlignment(Qt.AlignRight)
        self.text_textEdit = QTextEdit()

        self.properties_grid.addWidget(self.text_label, 0, 0)
        self.properties_grid.addWidget(self.text_textEdit, 0, 1)

        # Amount property
        self.amount_label = QLabel('Amount:')  # Label
        self.amount_label.setAlignment(Qt.AlignRight)
        self.amount_spinBox = QSpinBox()  # SpinBox
        self.amount_spinBox.setMinimum(1)

        self.properties_grid.addWidget(self.amount_label, 1, 0)
        self.properties_grid.addWidget(self.amount_spinBox, 1, 1)
