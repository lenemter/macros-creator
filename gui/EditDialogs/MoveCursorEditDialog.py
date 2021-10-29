from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QComboBox, QSpinBox, QDoubleSpinBox

from gui.EditDialogs.EditDialog import EditDialog


class MoveCursorEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.move_type_comboBox.setCurrentText(self.action.move_type)
        self.set_spinBoxes_ranges()
        self.position_x_spinBox.setValue(self.action.position_x)
        self.position_y_spinBox.setValue(self.action.position_y)
        self.duration_doubleSpinBox.setValue(self.action.duration)
        self.button_comboBox.setCurrentText(self.action.button)

        self.move_type_comboBox.currentTextChanged.connect(self.set_spinBoxes_ranges)

    @property
    def properties(self) -> tuple:
        return (self.comment_lineEdit.text(), self.move_type_comboBox.currentText(), self.position_x_spinBox.value(),
                self.position_y_spinBox.value(), self.duration_doubleSpinBox.value(),
                self.button_comboBox.currentText())

    def set_spinBoxes_ranges(self) -> None:
        if self.move_type_comboBox.currentText() == 'Absolute':
            self.position_x_spinBox.setRange(0, 9999)
            self.position_y_spinBox.setRange(0, 9999)
        else:
            self.position_x_spinBox.setRange(-9999, 9999)
            self.position_y_spinBox.setRange(-9999, 9999)

    def init_ui(self):
        super().init_ui()

        # Move type
        self.move_type_label = QLabel('Move type:')  # Label
        self.move_type_label.setAlignment(Qt.AlignRight)
        self.move_type_comboBox = QComboBox()  # ComboBox
        self.move_type_comboBox.addItems(['Absolute', 'Relative'])

        self.properties_grid.addWidget(self.move_type_label, 0, 0)
        self.properties_grid.addWidget(self.move_type_comboBox, 0, 1)

        # Position X
        self.position_x_label = QLabel('X:')  # Label
        self.position_x_label.setAlignment(Qt.AlignRight)
        self.position_x_spinBox = QSpinBox()  # SpinBox

        self.properties_grid.addWidget(self.position_x_label, 1, 0)
        self.properties_grid.addWidget(self.position_x_spinBox, 1, 1)

        # Position Y
        self.position_y_label = QLabel('Y:')  # Label
        self.position_y_label.setAlignment(Qt.AlignRight)
        self.position_y_spinBox = QSpinBox()  # SpinBox

        self.properties_grid.addWidget(self.position_y_label, 2, 0)
        self.properties_grid.addWidget(self.position_y_spinBox, 2, 1)

        # Duration
        self.duration_label = QLabel('Duration:')  # Label
        self.duration_label.setAlignment(Qt.AlignRight)
        self.duration_doubleSpinBox = QDoubleSpinBox()  # DoubleSpinBox

        self.properties_grid.addWidget(self.duration_label, 3, 0)
        self.properties_grid.addWidget(self.duration_doubleSpinBox, 3, 1)

        # Button
        self.button_label = QLabel('Button:')  # Label
        self.button_label.setAlignment(Qt.AlignRight)
        self.button_comboBox = QComboBox()  # ComboBox
        self.button_comboBox.addItems(['None', 'Left', 'Right', 'Middle'])

        self.properties_grid.addWidget(self.button_label, 4, 0)
        self.properties_grid.addWidget(self.button_comboBox, 4, 1)
