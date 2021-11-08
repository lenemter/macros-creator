from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QGridLayout, \
    QDoubleSpinBox

from gui.widgets import HorizontalLine


class SettingsDialog(QDialog):
    def __init__(self, parent, settings: dict):
        super().__init__(parent)
        self.settings = settings
        self.init_ui()

    def get_settings(self):
        self.settings['time_between'] = self.time_between_doubleSpinBox.value()
        return self.settings

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.resize(400, 400)
        self.setMinimumSize(400, 400)

        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(6)
        self.setLayout(self.layout)

        # Title
        self.title = QLabel('Settings')
        self.title.setAlignment(Qt.AlignHCenter)
        font = self.title.font()
        font.setBold(True)
        font.setPointSize(18)
        self.title.setFont(font)
        self.layout.addWidget(self.title)

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

        # Time between actions
        self.time_between_label = QLabel('Time between actions:')
        self.time_between_doubleSpinBox = QDoubleSpinBox()
        self.time_between_doubleSpinBox.setRange(0, 9999)
        self.time_between_doubleSpinBox.setValue(self.settings.get('time_between', 0.0))
        self.properties_grid.addWidget(self.time_between_label, 0, 0)
        self.properties_grid.addWidget(self.time_between_doubleSpinBox, 0, 1)
        # Spacer
        self.spacer = QSpacerItem(0, 1000, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addSpacerItem(self.spacer)
