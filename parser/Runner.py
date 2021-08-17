from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from functools import partial

from parser.FileRead import read_file


def run(filepath):
    window = StopWindow(filepath)
    window.exec_()


# Step 1: Create a worker class
class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, filepath):
        super().__init__()
        self.stop_flag = False
        self.filepath = filepath

    def run(self):
        """Long-running task."""
        QThread.msleep(1000)
        actions = read_file(self.filepath)
        i = 0
        while i < len(actions) and not self.stop_flag:
            next_line = actions[i].run()
            if next_line is None:
                next_line = i + 1
            else:
                next_line -= 1  # Convert line to index
            i = next_line
        self.finished.emit()
        self.thread().quit()


class StopWindow(QDialog):
    def __init__(self, filepath):
        super().__init__()
        self.init_ui()
        self.filepath = filepath

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.runner = Runner(self.filepath)
        # Step 4: Move worker to the thread
        self.runner.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(partial(self.runner.run))
        self.runner.finished.connect(self.close_everything)
        self.stop_button.pressed.connect(self.close_everything)
        # Step 6: Start the thread
        self.thread.start()

    def close_everything(self):
        self.stop_button.setText('Quiting...')
        self.runner.stop_flag = True
        self.thread.wait()
        self.close()

    def init_ui(self):
        self.resize(200, 200)
        self.setMinimumSize(200, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.stop_button = QPushButton('Stop (Ctrl+Esc)')
        self.stop_button.setShortcut('Ctrl+Esc')
        self.layout.addWidget(self.stop_button)
