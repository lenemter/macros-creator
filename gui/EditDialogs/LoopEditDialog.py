from PyQt5.QtWidgets import QLabel, QComboBox, QSpinBox
from PyQt5.QtCore import Qt

from gui.EditDialogs.EditDialog import EditDialog


class LoopEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.set_loop_start_comboBox_values()
        self.set_loop_start_value()
        self.count_spinBox.setValue(self.action.count)

    def set_loop_start_comboBox_values(self):
        row_count = self.parent().table.rowCount()
        for i in range(1, row_count + 1):
            self.loop_start_comboBox.addItem(str(i))

    def set_loop_start_value(self):
        old_loop_start = self.action.loop_start
        row_count = self.parent().table.rowCount()
        if old_loop_start > row_count:
            self.loop_start_comboBox.setCurrentIndex(row_count - 1)
        else:
            self.loop_start_comboBox.setCurrentIndex(old_loop_start - 1)

    def init_ui(self):
        super().init_ui()

        # Loop start property
        self.loop_start_label = QLabel("Loop start:")
        self.loop_start_label.setAlignment(Qt.AlignRight)
        self.loop_start_comboBox = QComboBox()
        self.loop_start_comboBox.setEditable(True)

        self.properties_grid.addWidget(self.loop_start_label, 0, 0)
        self.properties_grid.addWidget(self.loop_start_comboBox, 0, 1)

        # Amount property
        self.count_label = QLabel('Count:')  # Label
        self.count_label.setAlignment(Qt.AlignRight)
        self.count_spinBox = QSpinBox()  # SpinBox
        self.count_spinBox.setMinimum(1)

        self.properties_grid.addWidget(self.count_label, 1, 0)
        self.properties_grid.addWidget(self.count_spinBox, 1, 1)
