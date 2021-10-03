from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSizePolicy, QPushButton
from PyQt5.QtCore import QThread, Qt


class StopWindow(QDialog):
    def __init__(self, runner_class, actions_list: list):
        super().__init__()
        self.init_ui()
        self.actions_list = actions_list

        self.stop_button.clicked.connect(self.close_thread)

        self.runner_thread = QThread()
        self.runner = runner_class(self.actions_list)
        self.runner.moveToThread(self.runner_thread)
        self.runner_thread.started.connect(self.runner.run)
        self.runner.finished.connect(self.close_thread)

    def exec_(self):
        self.runner_thread.start()
        return super().exec_()

    def close_thread(self):
        self.runner.stop()
        self.runner_thread.quit()
        self.runner_thread.wait()
        self.close()

    def init_ui(self):
        self.setGeometry(0, 0, 200, 200)
        self.setMinimumSize(200, 200)
        self.setWindowTitle("Stop")
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stop_button = QPushButton('Stop (Ctrl+Esc)')
        self.stop_button.setShortcut('Ctrl+Esc')
        self.stop_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addWidget(self.stop_button)
