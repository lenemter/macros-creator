from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSizePolicy, QPushButton


class StopDialog(QDialog):
    def __init__(self, runner_cls, actions_list: list, settings):
        super().__init__()
        self.init_ui()
        self.actions_list = actions_list

        self.stop_button.clicked.connect(self.close_thread)

        self.runner_thread = QThread()
        self.runner = runner_cls(self.actions_list, settings)
        self.runner.moveToThread(self.runner_thread)
        self.runner_thread.started.connect(self.runner.run)
        self.runner.finished.connect(self.close_thread)

    def exec(self):
        self.runner_thread.start()
        return super().exec()

    def close_thread(self):
        self.runner.stop()
        self.runner_thread.quit()
        self.runner_thread.wait()
        self.close()

    def keyPressEvent(self, event):
        # Ignore Esc key press
        if event.key() == Qt.Key_Escape:
            pass

    def init_ui(self):
        self.setGeometry(0, 0, 200, 200)
        self.setMinimumSize(200, 200)
        self.setWindowTitle("Stop")
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stop_button = QPushButton('Stop (Ctrl+Q)')
        self.stop_button.setShortcut('Ctrl+Q')
        self.stop_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addWidget(self.stop_button)
