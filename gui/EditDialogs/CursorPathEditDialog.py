from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QComboBox, QHBoxLayout, QPushButton, QSpacerItem, QTableWidget, QSpinBox, QSizePolicy, \
    QHeaderView, QAbstractItemView, QMessageBox

from gui.EditDialogs.EditDialog import EditDialog


class PointSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(0, 9999)


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

    def get_selected_rows(self):
        return list(set(item.row() for item in self.selectedIndexes()))

    def update_ranges(self):
        if self.range_state == 'Absolute':
            spinbox_min = 0
        else:
            spinbox_min = -9999

        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                spin_box = self.cellWidget(i, j)
                spin_box.setMinimum(spinbox_min)

    def fill_table(self, points):
        for x, y in points:
            self.add_point()
            self.cellWidget(self.rowCount() - 1, 0).setValue(x)
            self.cellWidget(self.rowCount() - 1, 1).setValue(y)

    def add_point(self):
        self.setRowCount(self.rowCount() + 1)

        for i in range(self.columnCount()):
            spin_box = PointSpinBox()
            spin_box.setValue(-1)
            self.setCellWidget(self.rowCount() - 1, i, spin_box)

        if self.range_state == 'Absolute':
            spinbox_min = 0
        else:
            spinbox_min = -9999

        for j in range(self.columnCount()):
            spin_box = self.cellWidget(self.rowCount() - 1, j)
            spin_box.setMinimum(spinbox_min)

    def remove_point(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.information(self, 'No rows', 'No rows selected', QMessageBox.Ok)
        else:
            for i, row in enumerate(selected_rows):
                self.removeRow(row - i)

    def clear_points(self):
        self.setRowCount(0)

    def get_points_list(self):
        points = []
        for i in range(self.rowCount()):
            value1 = int(self.cellWidget(i, 0).text())
            value2 = int(self.cellWidget(i, 1).text())
            points.append((value1, value2))
        return points


class CursorPathEditDialog(EditDialog):
    def __init__(self, parent, action):
        super().__init__(parent, action)

        self.move_type_comboBox.setCurrentText(self.action.move_type)
        self.set_table_state()
        self.table.fill_table(self.action.path)

        self.button_add_point.pressed.connect(self.table.add_point)
        self.button_remove_point.pressed.connect(self.table.remove_point)
        self.button_clear_points.pressed.connect(self.table.clear_points)

        self.move_type_comboBox.currentTextChanged.connect(self.set_table_state)

    def set_table_state(self):
        self.table.range_state = self.move_type_comboBox.currentText()
        self.table.update_ranges()

    def init_ui(self):
        super().init_ui()

        # Type property
        self.move_type_label = QLabel('Type:')  # Label
        self.move_type_label.setAlignment(Qt.AlignRight)
        self.move_type_comboBox = QComboBox()  # ComboBox
        self.move_type_comboBox.addItems(['Absolute', 'Relative'])

        self.properties_grid.addWidget(self.move_type_label, 0, 0)
        self.properties_grid.addWidget(self.move_type_comboBox, 0, 1)

        # Buttons
        self.buttons_layout = QHBoxLayout()
        self.layout.insertLayout(5, self.buttons_layout)
        self.button_add_point = QPushButton('Add point')
        self.button_remove_point = QPushButton('Remove')
        self.button_clear_points = QPushButton('Clear')

        self.buttons_layout.addWidget(self.button_add_point)
        self.buttons_layout.addWidget(self.button_remove_point)
        self.buttons_layout.addWidget(self.button_clear_points)
        self.spacer = QSpacerItem(1000, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.buttons_layout.addSpacerItem(self.spacer)

        # Table
        self.table = PointsTable()
        self.layout.insertWidget(6, self.table)
        # Remove last spacer
        self.layout.removeItem(self.layout.itemAt(7))