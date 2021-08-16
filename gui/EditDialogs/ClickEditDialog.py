from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox

from gui.EditDialogs.EditDialog import EditDialog


class ClickEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.action_comboBox.setCurrentText(self.action.action)
        self.check_action()
        self.button_comboBox.setCurrentText(self.action.button)
        self.move_type_comboBox.setCurrentText(self.action.move_type)
        self.set_spinBoxes_ranges()
        self.position_x_spinBox.setValue(self.action.position_x)
        self.position_y_spinBox.setValue(self.action.position_y)
        self.restore_checkBox.setChecked(self.action.restore_cursor)
        self.amount_spinBox.setValue(self.action.amount)
        self.interval_doubleSpinBox.setValue(self.action.interval)

        self.check_interval()

        self.action_comboBox.currentTextChanged.connect(self.check_action)
        self.move_type_comboBox.currentTextChanged.connect(self.set_spinBoxes_ranges)
        self.amount_spinBox.valueChanged.connect(self.check_interval)

    def check_action(self):
        if self.action_comboBox.currentText() != 'Press and release':
            self.amount_spinBox.setDisabled(True)
        else:
            self.amount_spinBox.setDisabled(False)
        self.check_interval()

    def set_spinBoxes_ranges(self):
        if self.move_type_comboBox.currentText() == 'Absolute':
            self.position_x_spinBox.setRange(0, 9999)
            self.position_y_spinBox.setRange(0, 9999)
        else:
            self.position_x_spinBox.setRange(-9999, 9999)
            self.position_y_spinBox.setRange(-9999, 9999)

    def check_interval(self):
        if any((self.amount_spinBox.value() == 1, not self.amount_spinBox.isEnabled())):
            self.interval_doubleSpinBox.setDisabled(True)
        else:
            self.interval_doubleSpinBox.setDisabled(False)

    def properties(self):
        return (self.comment_lineEdit.text(), self.action_comboBox.currentText(), self.button_comboBox.currentText(),
                self.amount_spinBox.value(), self.interval_doubleSpinBox.value(), self.move_type_comboBox.currentText(),
                self.position_x_spinBox.value(), self.position_y_spinBox.value(), int(self.restore_checkBox.isChecked()))

    def init_ui(self):
        super().init_ui()
        self.resize(400, 515)
        self.setMinimumSize(400, 515)

        # Action
        self.action_label = QLabel('Action:')  # Label
        self.action_label.setAlignment(Qt.AlignRight)
        self.action_comboBox = QComboBox()  # ComboBox
        self.action_comboBox.addItems(['Press and release', 'Press', 'Release'])

        self.properties_grid.addWidget(self.action_label, 0, 0)
        self.properties_grid.addWidget(self.action_comboBox, 0, 1)

        # Button
        self.button_label = QLabel('Button:')  # Label
        self.button_label.setAlignment(Qt.AlignRight)
        self.button_comboBox = QComboBox()  # ComboBox
        self.button_comboBox.addItems(['Left', 'Right', 'Middle'])

        self.properties_grid.addWidget(self.button_label, 1, 0)  # Add label
        self.properties_grid.addWidget(self.button_comboBox, 1, 1)  # Add comboBox

        # Amount
        self.amount_label = QLabel('Amount:')  # Label
        self.amount_label.setAlignment(Qt.AlignRight)
        self.amount_spinBox = QSpinBox()  # SpinBox
        self.amount_spinBox.setMinimum(1)

        self.properties_grid.addWidget(self.amount_label, 2, 0)
        self.properties_grid.addWidget(self.amount_spinBox, 2, 1)

        # Interval
        self.interval_label = QLabel("Interval:")  # Label
        self.interval_label.setAlignment(Qt.AlignRight)
        self.interval_doubleSpinBox = QDoubleSpinBox()  # DoubleSpinBox

        self.properties_grid.addWidget(self.interval_label, 3, 0)
        self.properties_grid.addWidget(self.interval_doubleSpinBox, 3, 1)

        # Move type
        self.move_type_label = QLabel('Move type:')  # Label
        self.move_type_label.setAlignment(Qt.AlignRight)
        self.move_type_comboBox = QComboBox()  # ComboBox
        self.move_type_comboBox.addItems(['Absolute', 'Relative'])

        self.properties_grid.addWidget(self.move_type_label, 4, 0)
        self.properties_grid.addWidget(self.move_type_comboBox, 4, 1)

        # Position X
        self.position_x_label = QLabel('Position X:')  # Label
        self.position_x_label.setAlignment(Qt.AlignRight)
        self.position_x_spinBox = QSpinBox()  # SpinBox

        self.properties_grid.addWidget(self.position_x_label, 5, 0)
        self.properties_grid.addWidget(self.position_x_spinBox, 5, 1)

        # Position Y
        self.position_y_label = QLabel('Position Y:')  # Label
        self.position_y_label.setAlignment(Qt.AlignRight)
        self.position_y_spinBox = QSpinBox()  # SpinBox

        self.properties_grid.addWidget(self.position_y_label, 6, 0)
        self.properties_grid.addWidget(self.position_y_spinBox, 6, 1)

        # Restore cursor position
        self.restore_label = QLabel('Restore cursor position:')  # Label
        self.restore_label.setAlignment(Qt.AlignRight)
        self.restore_checkBox = QCheckBox()  # CheckBox

        self.properties_grid.addWidget(self.restore_label, 7, 0)
        self.properties_grid.addWidget(self.restore_checkBox, 7, 1)