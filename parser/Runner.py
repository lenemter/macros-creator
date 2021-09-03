from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSizePolicy
import pyautogui
from time import sleep
import sys


def run(actions):
    window = StopWindow(actions)
    window.exec_()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions):
        super().__init__()
        self.actions = actions

    def close(self):
        pyautogui.FAILSAFE = True
        stderr = sys.stderr
        position = pyautogui.position()
        while True:
            try:
                pyautogui.moveTo(x=0, y=0, duration=0)
            except pyautogui.FailSafeException:
                sys.stderr = object
                break
        # sys.stderr stuff for suppressing exception
        sys.stderr = stderr
        pyautogui.FAILSAFE = False
        # move cursor to previous location
        if (position.x, position.y) != (0, 0):
            pyautogui.moveTo(x=position.x, y=position.y, duration=0)

    def run(self):
        sleep(1)
        i = 0
        while i < len(self.actions):
            try:
                next_line = self.actions[i].run()
            except pyautogui.FailSafeException:
                # it will be closed in close()
                break
            if next_line is None:
                next_line = i + 1
            else:
                next_line -= 1  # Convert line to index
            i = next_line
        self.finished.emit()


class StopWindow(QDialog):
    def __init__(self, actions):
        super().__init__()
        self.init_ui()
        self.actions_list = actions

        self.stop_button.pressed.connect(self.close_everything)

        self.runner_thread = QThread()
        self.runner = Runner(self.actions_list)
        self.runner.moveToThread(self.runner_thread)
        self.runner_thread.started.connect(self.runner.run)
        self.runner.finished.connect(self.close_everything)

        self.runner_thread.start()

    def close_everything(self):
        self.runner.close()
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
