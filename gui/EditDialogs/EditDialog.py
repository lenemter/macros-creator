from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QSpacerItem, \
    QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt
from abc import abstractmethod, ABC

from gui.Widgets import HorizontalLine


class EditDialog(QDialog):
    """Base EditDialog class"""

    def __init__(self, parent, action):
        super().__init__(parent)
        self.action = action
        self.init_ui()
        self.user_clicked_ok = False  # Variable for detecting if user clicked Ok or Cancel

        self.button_box.accepted.connect(self.accepted)
        self.button_box.rejected.connect(self.rejected)

    def accepted(self):
        self.user_clicked_ok = True
        self.close()

    def rejected(self):
        self.user_clicked_ok = False
        self.close()

    def properties(self):
        raise NotImplementedError

    def init_ui(self):
        self.setWindowTitle('Edit action')
        self.resize(400, 400)
        self.setMinimumSize(400, 400)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)
        self.setLayout(self.layout)

        # Title
        self.title = QLabel(self.action.name)
        self.title.setAlignment(Qt.AlignHCenter)
        font = self.title.font()
        font.setBold(True)
        font.setPointSize(18)
        self.title.setFont(font)
        self.layout.addWidget(self.title)

        self.line_number = QLabel(f'Line: {self.parent().table.actions_list.index(self.action) + 1}')
        self.line_number.setAlignment(Qt.AlignHCenter)
        font = self.line_number.font()
        font.setPointSize(9)
        self.line_number.setFont(font)
        self.layout.addWidget(self.line_number)

        # Comment
        self.comment_layout = QHBoxLayout()
        self.layout.addLayout(self.comment_layout)

        self.comment_lineEdit = QLineEdit(self.action.comment)  # lineEdit
        self.comment_lineEdit.setPlaceholderText('Comment')
        self.comment_layout.addWidget(self.comment_lineEdit)  # Add comboBox

        # Horizontal line
        self.line = HorizontalLine(self)
        self.layout.addWidget(self.line)

        # Properties grid
        self.properties_grid = QGridLayout()
        self.properties_grid.setContentsMargins(18, 6, 18, 6)
        self.properties_grid.setSpacing(12)
        self.properties_grid.setColumnStretch(0, 0)
        self.properties_grid.setColumnStretch(1, 1)
        self.layout.addLayout(self.properties_grid)

        # Spacer
        self.spacer = QSpacerItem(0, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addSpacerItem(self.spacer)

        # Ok Cancel buttons
        self.buttons_line = HorizontalLine()
        self.layout.addWidget(self.buttons_line)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.button_box)


class MousePathEditDialog(EditDialog):
    pass


class PressKeyEditDialog(EditDialog):
    pass


class WriteTextEditDialog(EditDialog):
    pass


class SleepDialog(EditDialog):
    pass


class LoopEditDialog(EditDialog):
    pass
