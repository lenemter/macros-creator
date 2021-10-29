from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QComboBox, QDoubleSpinBox

from gui.EditDialogs.EditDialog import EditDialog


class PressKeyEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.key_lineEdit.setText(self.action.key)
        self.action_comboBox.setCurrentText(self.action.action)
        self.amount_spinBox.setValue(self.action.amount)
        self.interval_doubleSpinBox.setValue(self.action.interval)

        self.check_action()
        self.action_comboBox.currentTextChanged.connect(self.check_action)
        self.amount_spinBox.valueChanged.connect(self.check_interval)

    @property
    def properties(self) -> tuple:
        return (self.comment_lineEdit.text(), self.key_lineEdit.text(), self.action_comboBox.currentText(),
                self.amount_spinBox.value(), self.interval_doubleSpinBox.value())

    def check_action(self) -> None:
        if self.action_comboBox.currentText() != 'Press and release':
            self.amount_spinBox.setDisabled(True)
        else:
            self.amount_spinBox.setDisabled(False)
        self.check_interval()

    def check_interval(self) -> None:
        if any((self.amount_spinBox.value() == 1, not self.amount_spinBox.isEnabled())):
            self.interval_doubleSpinBox.setDisabled(True)
        else:
            self.interval_doubleSpinBox.setDisabled(False)

    def init_ui(self):
        super().init_ui()

        # Key
        self.key_label = QLabel('Key:')  # Label
        self.key_label.setAlignment(Qt.AlignRight)
        self.key_lineEdit = QLineEdit()  # LineEdit

        self.properties_grid.addWidget(self.key_label, 0, 0)
        self.properties_grid.addWidget(self.key_lineEdit, 0, 1)

        # Action
        self.action_label = QLabel('Action:')  # Label
        self.action_label.setAlignment(Qt.AlignRight)
        self.action_comboBox = QComboBox()  # ComboBox
        self.action_comboBox.addItems(['Press and release', 'Press', 'Release'])

        self.properties_grid.addWidget(self.action_label, 1, 0)
        self.properties_grid.addWidget(self.action_comboBox, 1, 1)

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
