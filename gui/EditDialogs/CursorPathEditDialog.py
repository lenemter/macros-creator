from PyQt5.QtWidgets import QLabel, QComboBox, QHBoxLayout, QPushButton, QTableWidget, QSpinBox, QHeaderView, \
    QAbstractItemView, QMessageBox, QDoubleSpinBox
from PyQt5.QtCore import Qt

from gui.EditDialogs.EditDialog import EditDialog


class PointsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(['X', 'Y'])

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.range_state = 'Absolute'
        self.update_ranges()

    def get_selected_rows(self) -> list:
        return list(set(item.row() for item in self.selectedIndexes()))

    def update_ranges(self) -> None:
        if self.range_state == 'Absolute':
            spinbox_min = 0
        else:
            spinbox_min = -9999

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                spin_box = self.cellWidget(i, j)
                spin_box.setMinimum(spinbox_min)

    def fill_table(self, points) -> None:
        for x, y in points:
            self.add_point()
            self.cellWidget(self.rowCount() - 1, 0).setValue(x)
            self.cellWidget(self.rowCount() - 1, 1).setValue(y)

    def add_point(self) -> None:
        self.setRowCount(self.rowCount() + 1)

        for i in range(self.columnCount()):
            spin_box = QSpinBox()
            spin_box.setMaximum(9999)
            self.setCellWidget(self.rowCount() - 1, i, spin_box)

        if self.range_state == 'Absolute':
            spinbox_min = 0
        else:
            spinbox_min = -9999

        for j in range(self.columnCount()):
            spin_box = self.cellWidget(self.rowCount() - 1, j)
            spin_box.setMinimum(spinbox_min)

    def remove_point(self) -> None:
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.information(self, 'No rows', 'No rows selected', QMessageBox.Ok)
        else:
            for i, row in enumerate(selected_rows):
                self.removeRow(row - i)

    def clear_points(self):
        self.setRowCount(0)

    def get_points_list(self) -> list:
        points = []
        for i in range(self.rowCount()):
            value1 = int(self.cellWidget(i, 0).text())
            value2 = int(self.cellWidget(i, 1).text())
            points.append((value1, value2))
        return points


class CursorPathEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)
        self.resize(400, 500)
        self.setMinimumSize(400, 500)

        self.move_type_comboBox.setCurrentText(self.action.move_type)
        self.set_table_state()
        self.duration_doubleSpinBox.setValue(self.action.duration)
        self.button_comboBox.setCurrentText(self.action.button)
        self.table.fill_table(self.action.path)

        self.add_point_button.pressed.connect(self.table.add_point)
        self.remove_point_button.pressed.connect(self.table.remove_point)
        self.clear_points_button.pressed.connect(self.table.clear_points)

        self.move_type_comboBox.currentTextChanged.connect(self.set_table_state)

    def set_table_state(self) -> None:
        self.table.range_state = self.move_type_comboBox.currentText()
        self.table.update_ranges()

    def properties(self) -> tuple:
        return (self.comment_lineEdit.text(), self.move_type_comboBox.currentText(),
                self.duration_doubleSpinBox.value(), self.button_comboBox.currentText(), self.table.get_points_list())

    def init_ui(self):
        super().init_ui()

        # Move type
        self.move_type_label = QLabel('Type:')  # Label
        self.move_type_label.setAlignment(Qt.AlignRight)
        self.move_type_comboBox = QComboBox()  # ComboBox
        self.move_type_comboBox.addItems(['Absolute', 'Relative'])

        self.properties_grid.addWidget(self.move_type_label, 0, 0)
        self.properties_grid.addWidget(self.move_type_comboBox, 0, 1)

        # Duration
        self.duration_label = QLabel('Duration:')  # Label
        self.duration_label.setAlignment(Qt.AlignRight)
        self.duration_doubleSpinBox = QDoubleSpinBox()  # DoubleSpinBox

        self.properties_grid.addWidget(self.duration_label, 1, 0)
        self.properties_grid.addWidget(self.duration_doubleSpinBox, 1, 1)

        # Button
        self.button_label = QLabel('Button:')  # Label
        self.button_label.setAlignment(Qt.AlignRight)
        self.button_comboBox = QComboBox()  # ComboBox
        self.button_comboBox.addItems(['None', 'Left', 'Right', 'Middle'])

        self.properties_grid.addWidget(self.button_label, 2, 0)
        self.properties_grid.addWidget(self.button_comboBox, 2, 1)

        # Table buttons
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.layout.insertLayout(5, self.buttons_layout)
        self.add_point_button = QPushButton('Add point')
        self.remove_point_button = QPushButton('Remove')
        self.clear_points_button = QPushButton('Clear')

        self.buttons_layout.addWidget(self.add_point_button)
        self.buttons_layout.addWidget(self.remove_point_button)
        self.buttons_layout.addWidget(self.clear_points_button)

        # Table
        self.table = PointsTable()
        self.layout.insertWidget(6, self.table)
        # Remove last spacer
        self.layout.removeItem(self.layout.itemAt(7))
