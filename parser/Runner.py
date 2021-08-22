from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSizePolicy
from functools import partial


def run(actions):
    window = StopWindow(actions)
    window.exec_()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions):
        super().__init__()
        self.stop_flag = False
        self.actions = actions

    def run(self):
        QThread.msleep(1000)
        i = 0
        while i < len(self.actions) and not self.stop_flag:
            next_line = self.actions[i].run()
            if next_line is None:
                next_line = i + 1
            else:
                next_line -= 1  # Convert line to index
            i = next_line
        self.finished.emit()
        self.thread().quit()


class StopWindow(QDialog):
    def __init__(self, actions):
        super().__init__()
        self.init_ui()
        self.actions_list = actions

        self.thread = QThread()
        self.runner = Runner(self.actions_list)
        self.runner.moveToThread(self.thread)
        self.thread.started.connect(partial(self.runner.run))
        self.runner.finished.connect(self.close_everything)
        self.stop_button.pressed.connect(self.close_everything)

        self.thread.start()

    def close_everything(self):
        self.runner.stop_flag = True
        self.thread.wait()
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
