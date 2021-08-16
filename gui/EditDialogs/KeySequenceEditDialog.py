from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QComboBox
from PyQt5.QtCore import Qt

from gui.EditDialogs.EditDialog import EditDialog


class KeySequenceEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.key_sequence_lineEdit.setText(self.action.key_sequence)
        self.action_comboBox.setCurrentIndex(self.action.action)
        self.amount_spinBox.setValue(self.action.amount)

        self.check_action()
        self.action_comboBox.currentTextChanged.connect(self.check_action)

    def check_action(self):
        current_action = self.action_comboBox.currentText()
        if current_action != 'Press and release':
            self.amount_spinBox.setDisabled(True)
        else:
            self.amount_spinBox.setDisabled(False)

    def init_ui(self):
        super().init_ui()

        # Key sequence property
        self.key_sequence_label = QLabel('Key sequence:')  # Label
        self.key_sequence_label.setAlignment(Qt.AlignRight)
        self.key_sequence_lineEdit = QLineEdit()

        self.properties_grid.addWidget(self.key_sequence_label, 0, 0)
        self.properties_grid.addWidget(self.key_sequence_lineEdit, 0, 1)

        # Action property
        self.action_label = QLabel('Action:')  # Label
        self.action_label.setAlignment(Qt.AlignRight)
        self.action_comboBox = QComboBox()  # ComboBox
        self.action_comboBox.addItems(['Press and release', 'Press', 'Release'])

        self.properties_grid.addWidget(self.action_label, 1, 0)
        self.properties_grid.addWidget(self.action_comboBox, 1, 1)

        # Amount property
        self.amount_label = QLabel('Amount:')  # Label
        self.amount_label.setAlignment(Qt.AlignRight)
        self.amount_spinBox = QSpinBox()  # SpinBox
        self.amount_spinBox.setMinimum(1)

        self.properties_grid.addWidget(self.amount_label, 2, 0)
        self.properties_grid.addWidget(self.amount_spinBox, 2, 1)
