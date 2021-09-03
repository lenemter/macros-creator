from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSizePolicy, QPushButton
from PyQt5.QtCore import QThread


class StopWindow(QDialog):
    def __init__(self, runner, actions: list):
        super().__init__()
        self.init_ui()
        self.actions_list = actions

        self.stop_button.pressed.connect(self.close_thread)

        self.runner_thread = QThread()
        self.runner = runner(self.actions_list)
        self.runner.moveToThread(self.runner_thread)
        self.runner_thread.started.connect(self.runner.run)
        self.runner.finished.connect(self.finish)

    def exec_(self) -> int:
        self.runner_thread.start()
        return super().exec_()

    def close_thread(self):
        self.runner.close()
        self.runner_thread.quit()

    def finish(self):
        self.runner_thread.quit()
        self.close()

    def init_ui(self):
        self.resize(200, 200)
        self.setMinimumSize(200, 200)
        self.move(0, 0)
        self.setWindowTitle("Stop")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stop_button = QPushButton('Stop (Ctrl+Esc)')
        self.stop_button.setShortcut('Ctrl+Esc')
        self.stop_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addWidget(self.stop_button)
