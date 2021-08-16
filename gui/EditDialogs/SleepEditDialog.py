from PyQt5.QtWidgets import QLabel, QDoubleSpinBox
from PyQt5.QtCore import Qt

from gui.EditDialogs.EditDialog import EditDialog


class SleepEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.duration_doubleSpinBox.setValue(self.action.duration)

    def init_ui(self):
        super().init_ui()

        # Duration property
        self.duration_label = QLabel("Duration:")
        self.duration_label.setAlignment(Qt.AlignRight)
        self.duration_doubleSpinBox = QDoubleSpinBox()

        self.properties_grid.addWidget(self.duration_label, 0, 0)
        self.properties_grid.addWidget(self.duration_doubleSpinBox, 0, 1)