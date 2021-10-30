from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QComboBox

from gui.EditDialogs.EditDialog import EditDialog


class GotoEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)
        self.row_count = self.parent().actions_table.model().rowCount()

        self.set_loop_start_comboBox_values()
        self.set_loop_start_value()

    @property
    def properties(self) -> tuple:
        try:
            loop_start = int(self.loop_start_comboBox.currentText())
        except ValueError:
            loop_start = self.line_number
        return self.comment_lineEdit.text(), loop_start

    def set_loop_start_comboBox_values(self):
        for i in range(1, self.row_count + 1):
            self.loop_start_comboBox.addItem(str(i))

    def set_loop_start_value(self):
        old_loop_start = self.action.loop_start
        if old_loop_start > self.row_count:
            self.loop_start_comboBox.setCurrentIndex(self.row_count - 1)
        else:
            self.loop_start_comboBox.setCurrentIndex(old_loop_start - 1)

    def init_ui(self):
        super().init_ui()

        # Loop start
        self.loop_start_label = QLabel("Loop start:")  # Label
        self.loop_start_label.setAlignment(Qt.AlignRight)
        self.loop_start_comboBox = QComboBox()  # ComboBox
        self.loop_start_comboBox.setEditable(True)

        self.properties_grid.addWidget(self.loop_start_label, 0, 0)
        self.properties_grid.addWidget(self.loop_start_comboBox, 0, 1)
